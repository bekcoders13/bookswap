from datetime import datetime, timedelta
import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate


def get_or_create_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    user = User(email=email, created_at=datetime.today())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def generate_and_store_otp(db: Session, user: User):
    code = f"{random.randint(100000, 999999)}"
    user.otp_code = code
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
    db.commit()
    return code


def verify_otp(db: Session, email: str, otp: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or user.otp_code != otp:
        return None
    if user.otp_expires_at < datetime.utcnow():
        return None
    return user


def create_user(db: Session, user: UserCreate):
    current_user = get_user_by_email(db, user.email)
    if current_user is None:
        raise HTTPException(400, "Email tasdiqlanmagan.")
    db.query(User).filter(User.id == current_user.id).update({
        User.fullname: user.fullname,
        User.birth_date: user.birth_date,
        User.region: user.region,
        User.role: 'user',
        User.password: get_password_hash(user.password),
    })
    db.commit()
    return current_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, updates: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
