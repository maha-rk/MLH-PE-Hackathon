import smtplib
from email.mime.text import MIMEText

ALERT_EMAIL = "ellisborewell@gmail.com"
APP_PASSWORD = "evobusrqjhhxtkun"


def send_email_alert(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = ALERT_EMAIL
    msg["To"] = ALERT_EMAIL

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(ALERT_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        print("✅ Alert email sent!")

    except Exception as e:
        print("❌ Failed to send alert:", e)