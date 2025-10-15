from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User
from app.core.security import get_password_hash

router = APIRouter()


@router.post("/", status_code=201)
def create_user(payload: dict, db: Session = Depends(get_db)):
    """Create a new user. Expects keys: username, password, role"""
    username = payload.get("username")
    password = payload.get("password")
    role = payload.get("role", "farmer")

    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password are required")

    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="username already exists")

    pwd_hash = get_password_hash(password)
    user = User(username=username, password_hash=pwd_hash, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"status": "success", "user": {"id": user.id, "username": user.username, "role": user.role}}


@router.get("/")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    result = [{"id": u.id, "username": u.username, "role": u.role} for u in users]
    return {"users": result}


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "role": user.role}


@router.put("/{user_id}")
def update_user(user_id: int, payload: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if "username" in payload:
        user.username = payload.get("username")
    if "role" in payload:
        user.role = payload.get("role")
    if "password" in payload:
        user.password_hash = get_password_hash(payload.get("password"))

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"status": "success", "user": {"id": user.id, "username": user.username, "role": user.role}}


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"status": "deleted"}
