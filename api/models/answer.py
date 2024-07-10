from datetime import datetime
from ipaddress import IPv4Address

import sqlmodel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INET
from sqlmodel import Field, SQLModel


class Answer(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    exam_id: str = Field(default=None, index=True)
    username: str = Field(nullable=False, foreign_key="student.username")
    question: int = Field(default=None)
    part: int = Field(default=None)
    section: int = Field(default=None)
    task: int = Field(default=None)
    answer: str = Field(nullable=True)
    timestamp: datetime = Field(
        sa_column=sqlmodel.Column(
            sqlmodel.DateTime(timezone=False),
        )
    )

    ip: IPv4Address = Field(sa_column=Column(INET))
