from uuid import UUID

from fastapi import HTTPException
from google_auth_oauthlib.flow import Flow
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.modules.representatives.models import Representative


GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.freebusy",
]


def create_google_flow(
    state: str | None = None,
) -> Flow:
    client_config = {
        "web": {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [
                settings.google_redirect_uri,
            ],
        }
    }

    flow = Flow.from_client_config(
        client_config=client_config,
        scopes=GOOGLE_SCOPES,
        state=state,
        autogenerate_code_verifier=False,
    )

    flow.redirect_uri = settings.google_redirect_uri

    return flow


def get_representative_or_404(
    db: Session,
    representative_id: UUID,
) -> Representative:
    representative = db.get(
        Representative,
        representative_id,
    )

    if not representative:
        raise HTTPException(
            status_code=404,
            detail="Representative not found.",
        )

    return representative

