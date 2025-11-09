from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Union

from app.db.session import get_db
from app.db.models import User
from app.core.security import get_password_hash

router = APIRouter()


class ProfileUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[Union[EmailStr, str]] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        # Allow empty string or None
        if v == "" or v is None:
            return None
        # Otherwise, it will be validated as EmailStr by the type hint
        return v


class AccountUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    language: Optional[str] = None


class NotificationSettings(BaseModel):
    marketing_emails: Optional[bool] = None
    social_emails: Optional[bool] = None
    security_emails: Optional[bool] = None
    communication_emails: Optional[bool] = None
    mobile_notifications: Optional[bool] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


@router.get("/profile")
def get_profile(username: str, db: Session = Depends(get_db)):
    """Get user profile settings"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "bio": user.bio,
        "role": user.role,
    }


@router.put("/profile")
def update_profile(username: str, profile: ProfileUpdate, db: Session = Depends(get_db)):
    """Update user profile settings"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if username is being changed and if it's already taken
    if profile.username and profile.username != user.username:
        existing = db.query(User).filter(User.username == profile.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
        user.username = profile.username
    
    # Check if email is being changed and if it's already taken
    if profile.email and profile.email != user.email:
        existing = db.query(User).filter(User.email == profile.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
        user.email = profile.email
    
    if profile.full_name is not None:
        user.full_name = profile.full_name
    if profile.bio is not None:
        user.bio = profile.bio
    
    db.commit()
    db.refresh(user)
    
    return {
        "status": "success",
        "message": "Profile updated successfully",
        "profile": {
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "bio": user.bio,
        }
    }


@router.get("/account")
def get_account(username: str, db: Session = Depends(get_db)):
    """Get user account settings"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "full_name": user.full_name,
        "date_of_birth": user.date_of_birth,
        "language": user.language,
    }


@router.put("/account")
def update_account(username: str, account: AccountUpdate, db: Session = Depends(get_db)):
    """Update user account settings"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if account.full_name is not None:
        user.full_name = account.full_name
    if account.date_of_birth is not None:
        user.date_of_birth = account.date_of_birth
    if account.language is not None:
        user.language = account.language
    
    db.commit()
    db.refresh(user)
    
    return {
        "status": "success",
        "message": "Account settings updated successfully",
        "account": {
            "full_name": user.full_name,
            "date_of_birth": user.date_of_birth,
            "language": user.language,
        }
    }


@router.get("/notifications")
def get_notifications(username: str, db: Session = Depends(get_db)):
    """Get user notification settings"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "marketing_emails": user.marketing_emails,
        "social_emails": user.social_emails,
        "security_emails": user.security_emails,
        "communication_emails": user.communication_emails,
        "mobile_notifications": user.mobile_notifications,
    }


@router.put("/notifications")
def update_notifications(username: str, settings: NotificationSettings, db: Session = Depends(get_db)):
    """Update user notification settings"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if settings.marketing_emails is not None:
        user.marketing_emails = settings.marketing_emails
    if settings.social_emails is not None:
        user.social_emails = settings.social_emails
    if settings.security_emails is not None:
        user.security_emails = settings.security_emails
    if settings.communication_emails is not None:
        user.communication_emails = settings.communication_emails
    if settings.mobile_notifications is not None:
        user.mobile_notifications = settings.mobile_notifications
    
    db.commit()
    db.refresh(user)
    
    return {
        "status": "success",
        "message": "Notification settings updated successfully",
        "notifications": {
            "marketing_emails": user.marketing_emails,
            "social_emails": user.social_emails,
            "security_emails": user.security_emails,
            "communication_emails": user.communication_emails,
            "mobile_notifications": user.mobile_notifications,
        }
    }


@router.post("/password")
def change_password(username: str, password_data: PasswordChange, db: Session = Depends(get_db)):
    """Change user password"""
    from app.core.security import verify_password
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not verify_password(password_data.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update to new password
    user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    
    return {
        "status": "success",
        "message": "Password changed successfully"
    }
