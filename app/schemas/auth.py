from pydantic import BaseModel, EmailStr

class SendOTPRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp_code: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
