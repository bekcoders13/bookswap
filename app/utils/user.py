from sqlalchemy.orm import Session
from app.models.users import User
from datetime import datetime, timedelta
import random


def get_or_create_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    user = User(email=email)
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
