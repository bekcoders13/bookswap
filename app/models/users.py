from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from datetime import datetime
from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)   # online yoki offline shu uchun
    otp_code = Column(String, nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    fullname = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=True, default=datetime.today())
    region = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)

    role = Column(String(255), nullable=True)
    token = Column(String(255), nullable=True, default='')
    refresh_token = Column(String(255), nullable=True, default='')
    
