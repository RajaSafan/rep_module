from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
)

from backend.core.config import settings


def send_representative_invitation(
    representative_name: str,
    company_email: str,
    service: str,
    invitation_url: str,
) -> None:

    message = Mail(
        from_email="raja.safan007@gmail.com",
        to_emails=company_email,
        subject="Connect your Google Calendar",
        html_content=f"""
        <h2>Hello {representative_name}</h2>

        <p>
        You have been added as a representative.
        </p>

        <p>
        Service:
        <b>{service}</b>
        </p>

        <p>
        Click below to connect your Google Calendar:
        </p>

        <a href="{invitation_url}">
            Connect Calendar
        </a>

        <p>
        This invitation expires in 24 hours.
        </p>

        Regards,
        <br>
        EngageAI
        """,
    )

    client = SendGridAPIClient(
        settings.sendgrid_api_key
    )

    response = client.send(message)

    if response.status_code not in [200, 201, 202]:
        raise Exception(
            f"SendGrid failed: {response.status_code}"
        )