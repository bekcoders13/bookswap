from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.role_verification import role_verification
from app.core.security import get_current_active_user
from app.schemas import users as schemas
from app.utils import user as crud
from app.db import get_db

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/", summary="Foydalanuvchi ma'lumotlarini kiritish. Foydalanuvchi emailini tadiqlagandan so'ng, "
                               "bu endpoint orqali ma'lumotlarini bazaga yuboradi", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@user_router.get("/me", summary="Foydalanuvchi o'z ma'lumotlarini ko'rish", response_model=schemas.UserOut)
def get_current_user(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    user = crud.get_user(db, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("/{user_id}", summary="Foydalanuvchini id orqali olish", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db),
              current_user=Depends(get_current_active_user)):
    role_verification(current_user, 'read_user')
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("/", summary="Foydalanuvchilar ro'yhatini ko'rish", response_model=list[schemas.UserOut])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
               current_user=Depends(get_current_active_user)):
    role_verification(current_user, 'list_users')
    return crud.get_users(db, skip=skip, limit=limit)


@user_router.put("/{user_id}", summary="Foydalanuvchi ma'lumotlarini tahrirlash", response_model=schemas.UserOut)
def update_user(user_id: int, updates: schemas.UserUpdate, db: Session = Depends(get_db),
                current_user=Depends(get_current_active_user)):
    role_verification(current_user, 'update_user')
    updated = crud.update_user(db, user_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@user_router.delete("/{user_id}", summary="Foydalanuvchini id orqali o'chirish")
def delete_user(user_id: int, db: Session = Depends(get_db),
                current_user=Depends(get_current_active_user)):
    role_verification(current_user, 'delete_user')
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


@user_router.put('/change-role/{user_id}', summary="Foydalanuvchi vazifasini o'zgartirish, "
                                                   "admin yoki bossga ruxsat beriladi", response_model=schemas.UserOut)
def change_user_role(user_id: int, role: schemas.RoleType, db: Session = Depends(get_db),
                     current_user=Depends(get_current_active_user)):
    role_verification(current_user, 'change_user_role')
    if role not in schemas.RoleType:
        raise HTTPException(status_code=400, detail="Invalid role")
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role
    db.commit()
    db.refresh(user)
    return user
