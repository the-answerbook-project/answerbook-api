from datetime import datetime

from sqlmodel import SQLModel

from api.schemas import BaseSchema


class MarkHistoryRead(BaseSchema):
    id: int
    mark: float | None
    feedback: str | None
    marker: str
    timestamp: datetime


class MarkRead(BaseSchema):
    id: int
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
