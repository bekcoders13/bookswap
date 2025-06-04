import smtplib
from email.message import EmailMessage

SMTP_SENDER = "a48468908@gmail.com"
SMTP_PASSWORD = "lslz fktl ewif ildn"


def send_otp_email(to_email: str, code: str):
    msg = EmailMessage()
    msg["Subject"] = "Your BookSwap Login Code"
    msg["From"] = SMTP_SENDER
    msg["To"] = to_email
    msg.set_content(f"Your login code: {code}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_SENDER, SMTP_PASSWORD)
        server.send_message(msg)
