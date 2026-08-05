


# from datetime import datetime, timezone
# from uuid import UUID

# from fastapi import (
#     APIRouter,
#     Depends,
#     HTTPException,
#     Query,
#     status,
# )
# from fastapi.responses import HTMLResponse, RedirectResponse
# from sqlalchemy import select
# from sqlalchemy.orm import Session

# from backend.core.database import get_db
# from backend.core.security import (
#     encrypt_token,
#     hash_invitation_token,
# )
# from backend.modules.representatives.google_calendar import (
#     create_google_flow,
#     get_representative_or_404,
# )
# from backend.modules.representatives.models import (
#     CalendarConnection,
#     Representative,
# )
# from backend.modules.representatives.schemas import (
#     RepresentativeCreate,
#     RepresentativeResponse,
# )
# from backend.modules.representatives.service import (
#     create_representative,
#     delete_representative,
#     get_representative,
#     get_representatives,
# )


# router = APIRouter(
#     prefix="/representatives",
#     tags=["Representatives"],
# )


# # ---------------------------------------------------------
# # Create representative
# # ---------------------------------------------------------

# @router.post(
#     "",
#     response_model=RepresentativeResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def add_representative(
#     payload: RepresentativeCreate,
#     db: Session = Depends(get_db),
# ):
#     return create_representative(
#         db=db,
#         payload=payload,
#     )


# # ---------------------------------------------------------
# # Get all representatives
# # ---------------------------------------------------------

# @router.get(
#     "",
#     response_model=list[RepresentativeResponse],
# )
# def list_representatives(
#     organization_id: UUID | None = Query(default=None),
#     db: Session = Depends(get_db),
# ):
#     return get_representatives(
#         db=db,
#         organization_id=organization_id,
#     )


# # ---------------------------------------------------------
# # Google OAuth callback
# #
# # Keep this route above "/{representative_id}" so FastAPI
# # does not try to interpret "google" as a UUID.
# # ---------------------------------------------------------

# @router.get(
#     "/google/callback",
#     response_class=HTMLResponse,
# )
# def google_oauth_callback(
#     code: str,
#     state: str,
#     db: Session = Depends(get_db),
# ):
#     try:
#         representative_id = UUID(state)

#     except ValueError as error:
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid OAuth state.",
#         ) from error

#     representative = get_representative_or_404(
#         db=db,
#         representative_id=representative_id,
#     )

#     flow = create_google_flow(
#         state=state,
#     )

#     try:
#         flow.fetch_token(
#             code=code,
#         )

#     except Exception as error:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Google OAuth failed: {error}",
#         ) from error

#     credentials = flow.credentials

#     connection = db.scalar(
#         select(CalendarConnection).where(
#             CalendarConnection.representative_id
#             == representative.representative_id
#         )
#     )

#     if connection is None:
#         connection = CalendarConnection(
#             representative_id=(
#                 representative.representative_id
#             ),
#         )

#         db.add(connection)

#     if not credentials.token:
#         raise HTTPException(
#             status_code=400,
#             detail="Google did not return an access token.",
#         )

#     connection.encrypted_access_token = encrypt_token(
#         credentials.token
#     )

#     # Google may not return a new refresh token every time.
#     # Keep the existing one if it already exists.
#     if credentials.refresh_token:
#         connection.encrypted_refresh_token = encrypt_token(
#             credentials.refresh_token
#         )

#     if not connection.encrypted_refresh_token:
#         raise HTTPException(
#             status_code=400,
#             detail=(
#                 "Google did not return a refresh token. "
#                 "Remove the app from your Google Account permissions "
#                 "and connect again."
#             ),
#         )

#     connection.token_expiry = credentials.expiry
#     connection.google_calendar_id = "primary"
#     connection.connection_status = "Connected"

#     representative.calendar_connected = True
#     representative.invitation_status = "Accepted"

#     db.commit()
#     db.refresh(representative)
#     db.refresh(connection)

#     return """
#     <!DOCTYPE html>
#     <html>
#         <head>
#             <title>Google Calendar Connected</title>
#             <meta charset="UTF-8">
#         </head>

#         <body style="
#             font-family: Arial, sans-serif;
#             max-width: 650px;
#             margin: 100px auto;
#             padding: 30px;
#             text-align: center;
#             border: 1px solid #dddddd;
#             border-radius: 10px;
#         ">
#             <h2 style="color: green;">
#                 Calendar accessed successfully.
#             </h2>

#             <p>
#                 Your Google Calendar is now connected.
#             </p>

#             <p>
#                 You may close this page.
#             </p>
#         </body>
#     </html>
#     """


# # ---------------------------------------------------------
# # Validate invitation and show Connect Calendar page
# # ---------------------------------------------------------

# @router.get(
#     "/invitation/{token}",
#     response_class=HTMLResponse,
# )
# def open_invitation(
#     token: str,
#     db: Session = Depends(get_db),
# ):
#     token_hash = hash_invitation_token(token)

#     representative = db.scalar(
#         select(Representative).where(
#             Representative.invitation_token_hash
#             == token_hash
#         )
#     )

#     if representative is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Invalid invitation link.",
#         )

#     if representative.invitation_status == "Accepted":
#         return """
#         <!DOCTYPE html>
#         <html>
#             <head>
#                 <title>Invitation Already Used</title>
#                 <meta charset="UTF-8">
#             </head>

#             <body style="
#                 font-family: Arial, sans-serif;
#                 max-width: 650px;
#                 margin: 100px auto;
#                 padding: 30px;
#                 text-align: center;
#             ">
#                 <h2>
#                     Google Calendar is already connected.
#                 </h2>
#             </body>
#         </html>
#         """

#     if (
#         representative.invitation_expires_at is None
#         or representative.invitation_expires_at
#         < datetime.now(timezone.utc)
#     ):
#         representative.invitation_status = "Expired"
#         db.commit()

#         raise HTTPException(
#             status_code=400,
#             detail="Invitation link has expired.",
#         )

#     connect_url = (
#         f"/representatives/"
#         f"{representative.representative_id}"
#         f"/google/connect"
#     )

#     return f"""
#     <!DOCTYPE html>
#     <html>
#         <head>
#             <title>Connect Google Calendar</title>
#             <meta charset="UTF-8">
#         </head>

#         <body style="
#             font-family: Arial, sans-serif;
#             max-width: 650px;
#             margin: 80px auto;
#             padding: 30px;
#             text-align: center;
#             border: 1px solid #dddddd;
#             border-radius: 10px;
#         ">
#             <h2>
#                 Hello {representative.representative_name}
#             </h2>

#             <p>
#                 You have been added as a representative.
#             </p>

#             <p>
#                 <strong>Service:</strong>
#                 {representative.service}
#             </p>

#             <p>
#                 <strong>Company Email:</strong>
#                 {representative.company_email}
#             </p>

#             <a
#                 href="{connect_url}"
#                 style="
#                     display: inline-block;
#                     margin-top: 20px;
#                     padding: 12px 22px;
#                     background-color: #2563eb;
#                     color: white;
#                     text-decoration: none;
#                     border-radius: 6px;
#                 "
#             >
#                 Connect Google Calendar
#             </a>
#         </body>
#     </html>
#     """


# # ---------------------------------------------------------
# # Start Google OAuth
# # ---------------------------------------------------------

# @router.get(
#     "/{representative_id}/google/connect",
# )
# def connect_google_calendar(
#     representative_id: UUID,
#     db: Session = Depends(get_db),
# ):
#     representative = get_representative_or_404(
#         db=db,
#         representative_id=representative_id,
#     )

#     if representative.calendar_connected:
#         return HTMLResponse(
#             content="""
#             <!DOCTYPE html>
#             <html>
#                 <head>
#                     <title>Calendar Connected</title>
#                     <meta charset="UTF-8">
#                 </head>

#                 <body style="
#                     font-family: Arial, sans-serif;
#                     max-width: 650px;
#                     margin: 100px auto;
#                     text-align: center;
#                 ">
#                     <h2 style="color: green;">
#                         Google Calendar is already connected.
#                     </h2>
#                 </body>
#             </html>
#             """
#         )

#     flow = create_google_flow(
#         state=str(representative.representative_id),
#     )

#     authorization_url, _ = flow.authorization_url(
#         access_type="offline",
#         prompt="consent",
#         include_granted_scopes="true",
#         login_hint=representative.company_email,
#     )

#     return RedirectResponse(
#         url=authorization_url,
#         status_code=status.HTTP_302_FOUND,
#     )


# # ---------------------------------------------------------
# # Get one representative
# # ---------------------------------------------------------

# @router.get(
#     "/{representative_id}",
#     response_model=RepresentativeResponse,
# )
# def retrieve_representative(
#     representative_id: UUID,
#     db: Session = Depends(get_db),
# ):
#     return get_representative(
#         db=db,
#         representative_id=representative_id,
#     )


# # ---------------------------------------------------------
# # Delete representative
# # ---------------------------------------------------------

# @router.delete(
#     "/{representative_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# def remove_representative(
#     representative_id: UUID,
#     db: Session = Depends(get_db),
# ):
#     delete_representative(
#         db=db,
#         representative_id=representative_id,
#     )

#     return None    



from datetime import datetime, timezone
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.responses import RedirectResponse

from sqlalchemy import select
from sqlalchemy.orm import Session

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


from backend.core.database import get_db

from backend.core.security import (
    encrypt_token,
)

from backend.modules.representatives.models import (
    Representative,
    CalendarConnection,
)

from backend.modules.representatives.schemas import (
    RepresentativeCreate,
    RepresentativeResponse,
)

from backend.modules.representatives.service import (
    create_representative,
    get_representatives,
    get_representative,
    delete_representative,
)

from backend.modules.representatives.google_calendar import (
    create_google_flow,
    verify_google_calendar_access,
)



router = APIRouter(
    prefix="/representatives",
    tags=["Representatives"],
)





@router.post(
    "",
    response_model=RepresentativeResponse,
    status_code=201,
)
def add_representative(
    payload: RepresentativeCreate,
    db: Session = Depends(get_db),
):

    return create_representative(
        db=db,
        payload=payload,
    )





@router.get(
    "",
    response_model=list[RepresentativeResponse],
)
def list_representatives(
    organization_id: UUID | None = None,
    db: Session = Depends(get_db),
):

    return get_representatives(
        db=db,
        organization_id=organization_id,
    )





@router.delete(
    "/{representative_id}",
    status_code=204,
)
def remove_representative(
    representative_id: UUID,
    db: Session = Depends(get_db),
):

    delete_representative(
        db=db,
        representative_id=representative_id,
    )





# -----------------------------
# GOOGLE CALENDAR CONNECT
# -----------------------------


@router.get(
    "/{representative_id}/google/connect"
)
def connect_google_calendar(
    representative_id: UUID,
    db: Session = Depends(get_db),
):

    representative = get_representative(
        db=db,
        representative_id=representative_id,
    )


    flow = create_google_flow(
        state=str(
            representative.representative_id
        )
    )


    authorization_url, _ = (
        flow.authorization_url(
            access_type="offline",
            prompt="consent",
        )
    )


    return {
        "authorization_url": authorization_url
    }





@router.get(
    "/google/callback"
)
def google_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):

    representative_id = UUID(state)


    representative = get_representative(
        db=db,
        representative_id=representative_id,
    )


    flow = create_google_flow(
        state=state
    )


    flow.fetch_token(
        code=code
    )


    credentials = flow.credentials


    connection = db.scalar(
        select(CalendarConnection).where(
            CalendarConnection.representative_id
            == representative_id
        )
    )


    if not connection:

        connection = CalendarConnection(
            representative_id=representative_id,
        )


        db.add(connection)



    connection.encrypted_access_token = (
        encrypt_token(
            credentials.token
        )
        if credentials.token
        else None
    )


    connection.encrypted_refresh_token = (
        encrypt_token(
            credentials.refresh_token
        )
        if credentials.refresh_token
        else None
    )


    connection.token_expiry = (
        credentials.expiry
    )


    connection.connection_status = (
        "Connected"
    )


    connection.last_verified_at = (
        datetime.now(timezone.utc)
    )


    representative.calendar_connected = True


    db.commit()


    return {
        "message":
            "Google Calendar connected successfully."
    }





# -----------------------------
# GOOGLE CALENDAR STATUS CHECK
# -----------------------------


@router.get(
    "/{representative_id}/calendar/check"
)
def check_calendar_status(
    representative_id: UUID,
    db: Session = Depends(get_db),
):


    representative = get_representative(
        db=db,
        representative_id=representative_id,
    )


    connection = db.scalar(
        select(CalendarConnection).where(
            CalendarConnection.representative_id
            == representative_id
        )
    )


    if not connection:

        return {
            "calendar_connected": False,
            "connection_status": "Not Connected",
        }



    try:

        verify_google_calendar_access(
            connection
        )


        connection.connection_status = (
            "Connected"
        )


        representative.calendar_connected = True


        connection.last_verified_at = (
            datetime.now(timezone.utc)
        )



    except Exception as error:


        print(
            f"Google calendar revoked: {error}",
            flush=True,
        )


        connection.connection_status = (
            "Revoked"
        )


        representative.calendar_connected = False



    db.commit()


    return {

        "representative_id":
            str(representative_id),

        "calendar_connected":
            representative.calendar_connected,

        "connection_status":
            connection.connection_status,

    }
    
    
    