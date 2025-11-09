from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app.db.models import User
from app.core.security import create_access_token, verify_password

from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"Login attempt - Username: {form_data.username}, Password length: {len(form_data.password)}")
    
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user:
        print(f"User not found: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    password_valid = verify_password(form_data.password, user.password_hash)
    print(f"Password verification result: {password_valid}")
    
    if not password_valid:
        print(f"Password verification failed for user: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.username, "role": user.role})
    print(f"Login successful for user: {user.username}")
    return {"access_token": token, "token_type": "bearer"}
