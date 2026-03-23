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


def _get_email_credentials():
  return os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD")










def send_email_structure(recipient_email: str, order_number: str):
    email_sender, email_password = _get_email_credentials()
    subject = f"Your Custom Case Order is Confirmed! (Order #{order_number})"
    
    # Create the multipart message container
    msg = MIMEMultipart("alternative")
    msg["From"] = email_sender
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # 1. Plain-text version (fallback)
    text_body = f"""
    Great news! We've received your order.
    
    Thank you for choosing us for your customized case. We are thrilled to bring your design to life!
    
    Your Order Number is: {order_number}
    
    What happens next?
    Our team is reviewing your design to ensure it prints perfectly. We will send you another email with tracking details as soon as it ships.
    
    If you have any questions, just reply to this email!
    
    Best regards,
    YourWay Team.
    """

    # 2. HTML version (Modern E-commerce Design)
    html_body = f"""
    <html>
      <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f9f9fb; padding: 20px; color: #333; margin: 0;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 16px rgba(0,0,0,0.05);">
          
          <div style="background-color: #111111; padding: 40px 20px; text-align: center; color: #ffffff;">
            <h1 style="margin: 0; font-size: 28px; letter-spacing: 1px;">ORDER CONFIRMED</h1>
            <p style="margin-top: 10px; font-size: 16px; color: #cccccc;">We're bringing your design to life.</p>
          </div>
          
          <div style="padding: 40px 30px;">
            <p style="font-size: 16px; line-height: 1.6; margin-top: 0;">Hi there,</p>
            <p style="font-size: 16px; line-height: 1.6;">Thank you for shopping with us! We've successfully received your customized case order and our production team is getting ready to print your design.</p>
            
            <div style="background-color: #f4f4f5; border-left: 4px solid #8b5cf6; padding: 20px; margin: 30px 0; border-radius: 0 8px 8px 0;">
              <p style="margin: 0; font-size: 14px; color: #666; text-transform: uppercase; letter-spacing: 1px;">Your Order Number</p>
              <p style="margin: 5px 0 0 0; font-size: 24px; font-weight: bold; color: #111;">{order_number}</p>
            </div>
            
            <h3 style="color: #111; font-size: 18px; margin-top: 30px;">What happens next?</h3>
            <ul style="padding-left: 20px; font-size: 15px; line-height: 1.6; color: #555;">
              <li style="margin-bottom: 10px;"><strong>Quality Check:</strong> We review your design to make sure it will print beautifully.</li>
              <li style="margin-bottom: 10px;"><strong>Production:</strong> Your custom case is printed and crafted.</li>
              <li><strong>Shipping:</strong> We'll send you another email with tracking info the moment it leaves our facility!</li>
            </ul>
          </div>
          
          <div style="background-color: #f9f9fb; padding: 20px; text-align: center; border-top: 1px solid #eeeeee;">
            <p style="font-size: 14px; color: #888; margin: 0;">
              Have questions about your order? Just reply to this email.<br><br>
              &copy; YourWay Team
            </p>
          </div>
          
        </div>
      </body>
    </html>
    """

    # Attach both parts
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, recipient_email, msg.as_string())
            print("Order confirmation email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_email(order_payload):
    email_sender, email_password = _get_email_credentials()

    recipient = order_payload.get('orderer_email')
    order_number = order_payload.get('order_number')

    if not recipient or not order_number:
        print("send_email: missing 'orderer_email' or 'order_number' in payload")
        return

    if not email_sender or not email_password:
        print("send_email: missing email credentials")
        return

    def _send():
        try:
            send_email_structure(recipient, order_number)
        except Exception as e:
            print(f"Error sending email in background thread: {e}")

    threading.Thread(target=_send, daemon=True).start()




def send_notification_structure(recipient_email: str, order_payload: dict):
    email_sender, email_password = _get_email_credentials()
    order_number = order_payload.get("order_number", "N/A")
    customer_name = order_payload.get("orderer_name", "N/A")
    recipient_list = [email.strip() for email in str(recipient_email).split(",") if email.strip()]

    if not recipient_list:
        print("send_notification_structure: no valid recipient email(s)")
        return

    subject = f"New Order Alert: #{order_number}"

    msg = MIMEMultipart("alternative")
    msg["From"] = email_sender
    msg["To"] = ", ".join(recipient_list)
    msg["Subject"] = subject

    text_body = (
        "New custom case order received!\n\n"
        f"Order Number: {order_number}\n"
        f"Customer: {customer_name}\n\n"
        "Please check the admin panel for full details."
    )

    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 20px; color: #222;">
        <div style="max-width: 600px; margin: 0 auto; background: #fff; border-radius: 8px; padding: 24px; border-top: 4px solid #10b981;">
          <h2 style="margin: 0 0 12px 0;">New Order Received</h2>
          <p style="margin: 0 0 12px 0;">A new customized case order has been placed.</p>
          <p style="margin: 0 0 8px 0;"><strong>Order Number:</strong> {order_number}</p>
          <p style="margin: 0 0 16px 0;"><strong>Customer:</strong> {customer_name}</p>
          <p style="margin: 0;">Please open the admin panel to review and process this order.</p>
        </div>
      </body>
    </html>
    """

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, recipient_list, msg.as_string())
            print(
                f"Admin notification sent successfully. order={order_number}, recipients={recipient_list}"
            )
    except Exception as e:
        print(f"Error sending notification email. order={order_number}, recipients={recipient_list}, error={e}")

def send_notification(order_payload):
    email_sender, email_password = _get_email_credentials()

    recipient = os.getenv("EMAIL_TO_NOTIFY")

    if not recipient:
        print("send_notification: missing 'EMAIL_TO_NOTIFY' in environment variables")
        return

    if not email_sender or not email_password:
        print("send_notification: missing email credentials")
        return

    def _send():
        try:
            send_notification_structure(recipient, order_payload)
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


