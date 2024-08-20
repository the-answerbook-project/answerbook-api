from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel


class Mark(SQLModel, table=True):
    id: int = Field(primary_key=True)
    exam_id: str = Field(default=None, index=True)
    assessment_id: int = Field(foreign_key="assessment.id", index=True)
    username: str = Field(nullable=False, foreign_key="student.username")
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
