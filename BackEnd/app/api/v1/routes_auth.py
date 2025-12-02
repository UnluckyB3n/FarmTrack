from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from app.db.session import get_db
from app.db.models import User
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.dependencies import get_current_user
from app.core.config import settings
import secrets
from datetime import datetime, timedelta
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from sqlalchemy.orm import Session

router = APIRouter()


class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str  # farmer, processor, regulator
    email: Optional[str] = None
    full_name: Optional[str] = None
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not v.isalnum() and '_' not in v:
            raise ValueError("Username must be alphanumeric (underscores allowed)")
        return v.lower().strip()
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        allowed_roles = ['farmer', 'processor', 'regulator']
        if v.lower() not in allowed_roles:
            raise ValueError(f"Role must be one of: {', '.join(allowed_roles)}")
        return v.lower()


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login. Get an access token for future requests.
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token = create_access_token({"sub": user.username, "role": user.role})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "email": user.email,
            "full_name": user.full_name,
            "auth_provider": user.auth_provider or "credentials"
        }
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user account.
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists (if provided)
    if payload.email:
        existing_email = db.query(User).filter(User.email == payload.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Create new user
    hashed_password = get_password_hash(payload.password)
    new_user = User(
        username=payload.username,
        password_hash=hashed_password,
        role=payload.role,
        email=payload.email,
        full_name=payload.full_name,
        auth_provider='credentials'
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate token for immediate login
    token = create_access_token({"sub": new_user.username, "role": new_user.role})
    
    return {
        "message": "User registered successfully",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "role": new_user.role,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "auth_provider": new_user.auth_provider or "credentials"
        }
    }


@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "bio": current_user.bio
    }


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


# In-memory store for reset tokens (for production, use Redis or database)
reset_tokens = {}


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Request a password reset token. Sends an email with reset instructions.
    For development (EMAIL_DEV_MODE=true), the token is also returned in response.
    """
    from app.utils.email_service import email_service
    import os
    
    user = db.query(User).filter(User.email == payload.email).first()
    
    if not user:
        # Return success even if email doesn't exist (security best practice)
        return {
            "message": "If the email exists, a reset token has been sent",
            "dev_mode": False
        }
    
    # Generate secure reset token
    reset_token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=1)
    
    # Store token with expiry
    reset_tokens[reset_token] = {
        "user_id": user.id,
        "email": user.email,
        "expiry": expiry
    }
    
    # Send password reset email
    email_sent = email_service.send_password_reset_email(
        to_email=user.email,
        reset_token=reset_token,
        username=user.username
    )
    
    # Check if in dev mode
    dev_mode = os.getenv('EMAIL_DEV_MODE', 'true').lower() == 'true'
    
    response = {
        "message": "Password reset email sent" if email_sent else "Password reset token generated",
        "dev_mode": dev_mode
    }
    
    # For development, return token in response
    if dev_mode:
        response.update({
            "reset_token": reset_token,
            "expires_in": "1 hour",
            "user_email": user.email
        })
    
    return response


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Reset password using a valid reset token.
    """
    # Validate token
    token_data = reset_tokens.get(payload.token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Check if token is expired
    if datetime.utcnow() > token_data["expiry"]:
        # Clean up expired token
        del reset_tokens[payload.token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )
    
    # Get user
    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update password
    user.password_hash = get_password_hash(payload.new_password)
    db.commit()
    
    # Invalidate token
    del reset_tokens[payload.token]
    
    return {
        "message": "Password reset successfully",
        "username": user.username
    }


class GoogleAuthRequest(BaseModel):
    token: str  # Google ID token from frontend
    role: Optional[str] = "farmer"  # Default role for new users


@router.post("/google-auth", response_model=LoginResponse)
def google_auth(payload: GoogleAuthRequest, db: Session = Depends(get_db)):
    """
    Authenticate or register user with Google OAuth token.
    """
    try:
        # Verify the Google token
        idinfo = id_token.verify_oauth2_token(
            payload.token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
        
        # Verify the token is for our app
        if idinfo['aud'] != settings.GOOGLE_CLIENT_ID:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token audience"
            )
        
        # Extract user information from Google
        google_user_id = idinfo['sub']
        email = idinfo.get('email')
        name = idinfo.get('name', '')
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by Google"
            )
        
        # Check if user exists by email
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Create new user from Google account
            # Generate username from email
            username_base = email.split('@')[0]
            username = username_base
            
            # Ensure username is unique
            counter = 1
            while db.query(User).filter(User.username == username).first():
                username = f"{username_base}{counter}"
                counter += 1
            
            # Create user with a random password hash (won't be used for Google auth)
            random_password = secrets.token_urlsafe(32)
            user = User(
                username=username,
                password_hash=get_password_hash(random_password),
                email=email,
                full_name=name,
                role=payload.role if payload.role in ['farmer', 'processor', 'regulator'] else 'farmer',
                auth_provider='google'
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Generate JWT token for our app
        token = create_access_token({"sub": user.username, "role": user.role})
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "email": user.email,
                "full_name": user.full_name,
                "auth_provider": user.auth_provider or "google"
            }
        }
        
    except ValueError as e:
        # Invalid token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )
