import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_email(receiver, subject, body):

    if not SENDER_EMAIL or not APP_PASSWORD:
        raise ValueError(
            "Email credentials are not configured"
        )

    msg = MIMEText(body)

    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver
    msg["Subject"] = subject

    try:

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                SENDER_EMAIL,
                APP_PASSWORD
            )

            server.send_message(msg)

        return {
            "status": "success",
            "message": "Email sent successfully"
        }

    except Exception as e:

        raise Exception(
            f"Email sending failed: {str(e)}"
        )
