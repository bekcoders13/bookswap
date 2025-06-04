from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
