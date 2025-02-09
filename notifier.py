from twilio.rest import Client
from config import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE, TARGET_PHONE

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_sms(message):
    """Wysyła SMS z ofertą"""
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=TARGET_PHONE
    )
    print(f"📲 Wysłano SMS: {message}")
