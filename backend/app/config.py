import os

from dotenv import load_dotenv


load_dotenv()


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENAI_MODEL = "openai/gpt-4o-mini"

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")

SEND_DELAY_SECONDS = int(
    os.getenv("SEND_DELAY_SECONDS", "5")
)