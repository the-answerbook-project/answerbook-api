from datetime import datetime
from ipaddress import IPv4Address

from sqlalchemy import Column, DateTime, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import INET
from sqlmodel import Field, Relationship, SQLModel


class Answer(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "assessment_id", "username", "question", "part", "section", "task"
        ),
    )
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
    history: list["AnswerHistory"] = Relationship(back_populates="current_answer")


class AnswerHistory(SQLModel, table=True):
    __tablename__ = "answer_history"
    id: int | None = Field(primary_key=True, default=None)
    answer_id: int = Field(foreign_key="answer.id")
    value: str = Field(nullable=True)
    timestamp: datetime = Field(sa_column=Column(DateTime, nullable=False))
    current_answer: Answer = Relationship(back_populates="history")

    @classmethod
    def from_answer(cls, answer: Answer) -> "AnswerHistory":
        return cls(
            current_answer=answer, timestamp=answer.timestamp, value=answer.answer
        )
