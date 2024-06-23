from datetime import datetime, timezone

import sqlmodel
from sqlalchemy import func
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel


class Mark(SQLModel, table=True):
    id: int = Field(primary_key=True)
    exam_id: str = Field(default=None)
    username: str = Field(nullable=False)
    question: int = Field(default=None)
    part: int = Field(default=None)
    section: int = Field(default=None)
    mark: float = Field(nullable=True)
    feedback: str = Field(nullable=True)
    timestamp: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.timezone("UTC", func.current_timestamp()),
            nullable=False,
        )
    )
    marker: str = Field(nullable=False)

    history: list["MarkHistory"] = Relationship(back_populates="current_mark")


class MarkHistory(SQLModel, table=True):
    __tablename__ = "mark_history"
    id: int | None = Field(primary_key=True, default=None)
    mark_id: int = Field(foreign_key="mark.id")

    mark: float = Field(nullable=True)
    feedback: str = Field(nullable=True)
    timestamp: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.timezone("UTC", func.current_timestamp()),
            nullable=False,
        )
    )
    marker: str = Field(nullable=False)
    current_mark: Mark = Relationship(back_populates="history")


class MarkHistoryRead(SQLModel):
    mark: float | None
    feedback: str | None
    marker: str
    timestamp: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: (
                dt.replace(tzinfo=timezone.utc).isoformat() if dt else None
            ),
        }


class MarkRead(SQLModel):
    question: int
    part: int
    section: int
    mark: float | None
    feedback: str | None
    marker: str
    timestamp: datetime
    history: list[MarkHistoryRead]

    class Config:
        json_encoders = {
            datetime: lambda dt: (
                dt.replace(tzinfo=timezone.utc).isoformat() if dt else None
            ),
        }


class MarkWrite(SQLModel):
    question: int
    part: int
    section: int
    mark: float | None = None
    feedback: str | None = None
