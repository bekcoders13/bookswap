from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.auth import VerifyOTPRequest, TokenResponse
from app.core.email import send_otp_email
from app.core.security import create_access_token
from app.utils import user as crud_user
from app.db import get_db

auth_router = APIRouter(
    prefix="/auth",
    tags=["authentication endpoint"])


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


@auth_router.post("/verify-code", response_model=TokenResponse)
def verify_login_code(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    user = crud_user.verify_otp(db, request.email, request.otp_code)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}
