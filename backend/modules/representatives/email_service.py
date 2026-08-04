import resend

from backend.core.config import settings


def send_representative_invitation(
    representative_name: str,
    company_email: str,
    service: str,
    invitation_url: str,
) -> None:

    resend.api_key = settings.resend_api_key


    resend.Emails.send(
        {
            "from": "EngageAI <onboarding@resend.dev>",
            "to": [
                company_email
            ],
            "subject": "Connect your Google Calendar",

            "html": f"""
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
                Connect Google Calendar
            </a>

            <p>
            This invitation expires in 24 hours.
            </p>

            <br>

            Regards,
            <br>
            EngageAI
            """
        }
    )