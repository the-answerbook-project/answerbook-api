from datetime import datetime

from sqlalchemy import func
from sqlmodel import Column, DateTime, Field, SQLModel


class RevokedToken(SQLModel, table=True):
    __tablename__ = "revoked_token"
    id: int = Field(default=None, primary_key=True)
    token: str
    timestamp: datetime = Field(
        sa_column=Column(
            DateTime(timezone=False),
            server_default=func.timezone("UTC", func.current_timestamp()),
            nullable=False,
        )
    )
    expiration: datetime = Field(nullable=False)
