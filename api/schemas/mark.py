from datetime import datetime, timezone

from sqlmodel import SQLModel

from api.schemas import BaseSchema


class MarkHistoryRead(BaseSchema):
    mark: float | None
    feedback: str | None
    marker: str
    timestamp: datetime


class MarkRead(BaseSchema):
    question: int
    part: int
    section: int
    mark: float | None
    feedback: str | None
    marker: str
    timestamp: datetime
    history: list[MarkHistoryRead]


class MarkWrite(SQLModel):
    question: int
    part: int
    section: int
    mark: float | None = None
    feedback: str | None = None
