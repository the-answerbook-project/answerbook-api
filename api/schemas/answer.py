from datetime import datetime

import sqlmodel
from pydantic import AnyHttpUrl
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INET
from sqlmodel import Field, SQLModel


class Answer(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    exam_id: str = Field(default=None)
    username: str = Field(nullable=False)
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

    ip: AnyHttpUrl = Field(sa_column=Column(INET))


class AnswerRead(SQLModel):
    question: int
    part: int
    section: int
    task: int
    answer: str
