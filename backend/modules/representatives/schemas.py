# from datetime import datetime
# from uuid import UUID

# from pydantic import BaseModel, ConfigDict, EmailStr


# class RepresentativeCreate(BaseModel):
#     organization_id: UUID
#     representative_name: str
#     service: str
#     company_email: EmailStr


# class RepresentativeResponse(BaseModel):
#     representative_id: UUID
#     organization_id: UUID
#     representative_name: str
#     service: str
#     company_email: EmailStr

#     invitation_status: str
#     calendar_connected: bool
#     status: str

#     created_at: datetime
#     updated_at: datetime

#     model_config = ConfigDict(from_attributes=True)
    
    
from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)



class RepresentativeCreate(BaseModel):

    organization_id: UUID

    representative_name: str

    service: str

    service_description: str

    company_email: EmailStr





class RepresentativeResponse(BaseModel):

    representative_id: UUID

    organization_id: UUID

    representative_name: str

    service: str

    service_description: str

    company_email: EmailStr


    invitation_status: str

    calendar_connected: bool

    status: str


    created_at: datetime

    updated_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )    