from datetime import datetime
from ipaddress import IPv4Address

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import INET
from sqlmodel import Field, SQLModel


class Answer(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    assessment_id: int = Field(foreign_key="assessment.id", index=True)
    username: str = Field(nullable=False, foreign_key="student.username")
    question: int = Field(default=None)
    part: int = Field(default=None)
    section: int = Field(default=None)
    task: int = Field(default=None)
    answer: str = Field(nullable=True)
    timestamp: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.timezone("UTC", func.current_timestamp()),
            nullable=False,
        )
    )
    ip: IPv4Address = Field(sa_column=Column(INET))
