from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import date, datetime
        

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    fullname: str
    birth_date: date
    region: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    fullname: str
    birth_date: date
    region: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    fullname: Optional[str]
    birth_date: Optional[date]
    region: Optional[str]


class UserStatusUpdate(BaseModel):
    is_active: bool


class RoleType(str, Enum):
    user = 'user'
    admin = 'admin'
