from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_token, pwd_context, SECRET_KEY, is_token_expired
from app.models.users import User
from app.schemas.auth import VerifyOTPRequest, Token
from app.core.email import send_otp_email
from app.utils import user as crud_user
from app.db import get_db

auth_router = APIRouter(tags=["authentication endpoint"])


@auth_router.post("/send-email/")
async def send_email_endpoint(to_email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = crud_user.get_or_create_user_by_email(db, to_email)
    code = crud_user.generate_and_store_otp(db, user)
    background_tasks.add_task(
        send_otp_email,
        to_email,
        "Welcome to our app!",
        "<p>Thank you for registering!</p>"
        f"<b>Your password: {code}</b>"
    )
    return {"message": "Email yuborildi (background)"}


@auth_router.post("/verify-code")
def verify_login_code(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    user = crud_user.verify_otp(db, request.email, request.otp_code)
    if not user:
        raise HTTPException(status_code=400, detail="Kod noto'g'ri yoki muddati tugagan")
    raise HTTPException(status_code=200, detail="Email va kod tasdiqlandi")


@auth_router.post("/token", summary="Token yaratish, login")
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username
    password = form_data.password

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Foydalanuvchi topilmadi")

    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Parol xato")

    access_token = create_token(
        data={"sub": user.email, "type": "access"},
        secret_key=SECRET_KEY,
        expires_delta=timedelta(hours=1),
    )

    refresh_token = create_token(
        data={"sub": user.email, "type": "refresh"},
        secret_key=SECRET_KEY,
        expires_delta=timedelta(days=3),
    )

    db.query(User).filter(User.id == user.id).update({
        User.token: access_token,
        User.refresh_token: refresh_token,
    })
    db.commit()

    return {
        "id": user.id,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@auth_router.post("/refresh_token", summary="Tokenni yangilash refresh token orqali",
                  response_model=Token)
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.refresh_token == refresh_token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Refresh token yaroqsiz")

    if is_token_expired(refresh_token, SECRET_KEY):
        raise HTTPException(status_code=400, detail="Refresh token muddati tugagan")

    access_token = create_token(
        data={"sub": user.email, "type": "access"},
        secret_key=SECRET_KEY,
        expires_delta=timedelta(hours=1),
    )

    db.query(User).filter(User.id == user.id).update({
        User.token: access_token,
    })
    db.commit()

    return {
        "id": user.id,
        "access_token": access_token,
        "token_type": "bearer"
    }
