import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "joshiraginir06@gmail.com"
APP_PASSWORD = "nuql ispz dxys gwmt"

def send_email(receiver, subject, body):

    msg = MIMEText(body)

    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver
    msg["Subject"] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        server.starttls()

        server.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        server.send_message(msg)