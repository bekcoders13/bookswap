import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from app.db import get_db
from app.models.users import User
from app.schemas.auth import TokenData

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Tokenni olish uchun URL — login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict, secret_key: str, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta \
        if expires_delta else datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, ALGORITHM)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(User).where(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user=Depends(get_current_user)):
    return current_user


def verify_token(token_data: str, secret_key: str):
    try:
        payload = jwt.decode(token_data, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def is_token_expired(token_data: str, secret_key: str) -> bool:
    payload = verify_token(token_data, secret_key)
    if not payload:
        return True
    return datetime.utcnow() > datetime.fromtimestamp(payload.get("exp", 0))