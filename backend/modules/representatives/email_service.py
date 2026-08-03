# import smtplib
# from email.message import EmailMessage

# from backend.core.config import settings


# def send_representative_invitation(
#     representative_name: str,
#     company_email: str,
#     service: str,
#     invitation_url: str,
# ) -> None:
#     message = EmailMessage()

#     message["Subject"] = "Connect your Google Calendar"
#     message["From"] = settings.smtp_email
#     message["To"] = company_email

#     message.set_content(
#         f"""
# Hello {representative_name},

# You have been added as a representative.

# Service: {service}

# Please use the link below to connect your Google Calendar:

# {invitation_url}

# This invitation link will expire in 24 hours.

# Regards,
# EngageAI
# """.strip()
#     )

#     with smtplib.SMTP(
#         host=settings.smtp_host,
#         port=settings.smtp_port,
#         timeout=30,
#     ) as smtp:
#         smtp.ehlo()
#         smtp.starttls()
#         smtp.ehlo()

#         smtp.login(
#             settings.smtp_email,
#             settings.smtp_password,
#         )

#         smtp.send_message(message)



import smtplib
from email.message import EmailMessage

from backend.core.config import settings


def send_representative_invitation(
    representative_name: str,
    company_email: str,
    service: str,
    invitation_url: str,
) -> None:
    print(
        f"Connecting SMTP host={settings.smtp_host}, "
        f"port={settings.smtp_port}, "
        f"sender={settings.smtp_email}",
        flush=True,
    )

    message = EmailMessage()
    message["Subject"] = "Connect your Google Calendar"
    message["From"] = settings.smtp_email
    message["To"] = company_email

    message.set_content(
        f"""
Hello {representative_name},

You have been added as a representative.

Service: {service}

Please use the link below to connect your Google Calendar:

{invitation_url}

This invitation link will expire in 24 hours.

Regards,
EngageAI
""".strip()
    )

    with smtplib.SMTP(
        host=settings.smtp_host,
        port=settings.smtp_port,
        timeout=30,
    ) as smtp:
        smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(
            settings.smtp_email,
            settings.smtp_password,
        )

        smtp.send_message(message)