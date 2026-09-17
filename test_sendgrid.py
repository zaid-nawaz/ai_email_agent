from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.config import (
    SENDGRID_API_KEY,
    SENDER_EMAIL
)


message = Mail(
    from_email=SENDER_EMAIL,
    to_emails=SENDER_EMAIL,
    subject="AI Email Agent - Test",
    plain_text_content=(
        "This is a test email from the AI Email Agent."
    )
)


client = SendGridAPIClient(
    SENDGRID_API_KEY
)


response = client.send(message)


print("Status:", response.status_code)
print("Email sent successfully!")