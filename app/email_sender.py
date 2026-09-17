from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.config import (
    SENDGRID_API_KEY,
    SENDER_EMAIL
)


def send_email(
    recipient: str,
    subject: str,
    body: str
):

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=recipient,
        subject=subject,
        plain_text_content=body
    )

    client = SendGridAPIClient(
        SENDGRID_API_KEY
    )

    response = client.send(message)

    if response.status_code >= 400:
        raise Exception(
            f"SendGrid error: "
            f"{response.status_code}"
        )

    return response