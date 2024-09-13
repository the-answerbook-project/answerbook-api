from datetime import datetime, timezone

from pydantic import field_serializer
from sqlmodel import SQLModel

from api.schemas import BaseSchema


class MarkHistoryRead(BaseSchema):
    id: int
    mark: float | None
    feedback: str | None
    marker: str
    timestamp: datetime

    @field_serializer("timestamp")
    def serialize_timestamp(self, timestamp: datetime, _info):
        return timestamp.replace(tzinfo=timezone.utc).isoformat()


class MarkRead(BaseSchema):
    id: int
    username: str
    question: int
    part: int
    section: int
    mark: float | None
    feedback: str | None
    marker: str
    timestamp: datetime
    history: list[MarkHistoryRead]

    @field_serializer("timestamp")
    def serialize_timestamp(self, timestamp: datetime, _info):
        return timestamp.replace(tzinfo=timezone.utc).isoformat()


class MarkWrite(SQLModel):
    username: str
    question: int
    part: int
    section: int
    mark: float | None = None
    feedback: str | None = None
