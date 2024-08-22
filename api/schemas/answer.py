from datetime import datetime, timezone

from pydantic import field_serializer
from sqlmodel import SQLModel


class AnswerRead(SQLModel):
    id: int
    username: str
    question: int
    part: int
    section: int
    task: int
    answer: str
    timestamp: datetime

    @field_serializer("timestamp")
    def serialize_timestamp(self, timestamp: datetime, _info):
        return timestamp.replace(tzinfo=timezone.utc).isoformat()


class AnswerWrite(SQLModel):
    question: int
    part: int
    section: int
    task: int
    answer: str
