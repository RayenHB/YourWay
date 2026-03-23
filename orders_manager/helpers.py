import os
import smtplib
import threading
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import redis








EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
VERIFICATION_CODE_EXPIRY = 300  
RATE_LIMIT_EXPIRY = 60



redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)




def send_code(recipient_email: str, code: str):
        subject = "Case order"
        body = f"Your verification code is: {code}. This code expires in 5 minutes."
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient_email, msg.as_string())
            server.quit()
        except Exception as e:
            print(f"Error sending email: {e}")


def send_email_structure(recipient_email: str, code: str):
        subject = "Print order"
        body = f"Your order code is: {code}"
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient_email, msg.as_string())
            server.quit()
        except Exception as e:
            print(f"Error sending email: {e}")

def send_email(order_payload):

    recipient = order_payload.get('orderer_email')
    order_number = order_payload.get('order_number')

    if not recipient or not order_number:
        print("send_email: missing 'orderer_email' or 'order_number' in payload")
        return

    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print("send_email: missing email credentials")
        return

    def _send():
        try:
            send_email_structure(recipient, order_number)
        except Exception as e:
            print(f"Error sending email in background thread: {e}")

    threading.Thread(target=_send, daemon=True).start()

def is_valid_uae_postal_code(code: str) -> bool:
    if code is None:
        return True
    # UAE uses 5-digit postal codes; accept only exactly 5 digits
    return bool(re.fullmatch(r"\d{5}", str(code).strip()))

# Validate UAE phone number if provided
def is_valid_uae_phone_number(code: str) -> bool:
    if code is None:
        return True
    s = str(code).strip()
    # remove common separators but keep leading + if present
    s_clean = re.sub(r"[\s\-()]+", "", s)
    patterns = [
                r"^05\d{8}$",            # local mobile e.g. 0501234567
                r"^\+9715\d{8}$",       # intl mobile with +971 e.g. +971501234567
                r"^9715\d{8}$",          # intl mobile without +
                r"^0[2346]\d{7}$",       # local landline e.g. 021234567, 041234567
                r"^\+971[2346]\d{7}$",   # intl landline with +971
                r"^971[2346]\d{7}$",      # intl landline without +
            ]

    for p in patterns:
        if re.fullmatch(p, s_clean):
            return True

    return False


