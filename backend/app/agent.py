import json

from openai import OpenAI

from app.config import (
    OPENROUTER_API_KEY,
    OPENAI_MODEL
)

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
)


SYSTEM_PROMPT = """
You are an AI email outreach assistant.

Your job is to write a short, natural,
personalized professional email.

Use ONLY the information provided about the recipient
and their company.

Do not invent facts.

The email should:
- Be personalized to the recipient.
- Mention something relevant about their company.
- Clearly explain why we are reaching out.
- Sound human and conversational.
- Avoid generic spam-like language.
- Be concise.
- Be under 150 words.

Return ONLY valid JSON in this format:

{
    "subject": "email subject",
    "body": "email body"
}
"""


def generate_email(lead: dict) -> dict:

    user_prompt = f"""
Create a personalized outreach email for:

Name: {lead["name"]}
Role: {lead["role"]}
Company: {lead["company"]}

Company description:
{lead["company_description"]}
"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        response_format={'type': 'json_object'},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content

    return json.loads(content)