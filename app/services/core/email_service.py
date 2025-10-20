import os

import httpx

RESEND_API_KEY = os.getenv("RESEND_API_KEY")


async def send_email(to: str, subject: str, body: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
            json={
                "from": "Notifier <onboarding@resend.dev>",
                "to": [to],
                "subject": subject,
                "html": f"<p>{body}</p>",
            },
        )
