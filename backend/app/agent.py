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

Requirements:

- Address the recipient by name.
- Personalize the email based on their company and role.
- Clearly explain the purpose of the outreach.
- Keep the tone professional but conversational.
- Avoid generic spam-like language.
- Keep the email under 150 words.
- Do not use excessive marketing language.
- Do not make claims that are not supported by the input.
- Do not include a sign-off such as "Best", "Regards", "Thanks", etc.
- Do not include a sender name, title, company, contact information, or placeholders such as "[Your Name]".
- End the email naturally after the final sentence.

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