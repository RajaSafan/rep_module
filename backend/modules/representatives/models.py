import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


class Representative(Base):
    __tablename__ = "representatives"

    representative_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    representative_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    service: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    company_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    invitation_token_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    invitation_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    invitation_status: Mapped[str] = mapped_column(
        String(30),
        default="Pending",
        nullable=False,
    )

    calendar_connected: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Active",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    calendar_connection: Mapped["CalendarConnection | None"] = relationship(
        back_populates="representative",
        cascade="all, delete-orphan",
        uselist=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "company_email",
            name="uq_representative_email_per_organization",
        ),
    )


class CalendarConnection(Base):
    __tablename__ = "calendar_connections"

    calendar_connection_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    representative_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "representatives.representative_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    encrypted_access_token: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    encrypted_refresh_token: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    token_expiry: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    google_calendar_id: Mapped[str] = mapped_column(
        String(255),
        default="primary",
        nullable=False,
    )

    connection_status: Mapped[str] = mapped_column(
        String(30),
        default="Not Connected",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    representative: Mapped["Representative"] = relationship(
        back_populates="calendar_connection",
    )
    
    