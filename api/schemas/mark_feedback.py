from datetime import datetime

import sqlmodel
from sqlmodel import Field, Relationship, SQLModel


class MarkFeedback(SQLModel, table=True):
    id: int = Field(primary_key=True)
    exam_id: str = Field(default=None)
    username: str = Field(nullable=False)
    question: int = Field(default=None)
    part: int = Field(default=None)
    section: int = Field(default=None)
    task: int = Field(default=None)
    mark: int = Field(nullable=True)  # TODO:: int or float?
    feedback: str = Field(nullable=True)
    timestamp: datetime = Field(
        sa_column=sqlmodel.Column(
            sqlmodel.DateTime(timezone=False),
        )
    )
    marker: str = Field(nullable=False)

    history: list["MarkFeedbackHistory"] = Relationship(back_populates="mark_feedback")

    # TODO : Mark approved/submitted?


class MarkFeedbackHistory(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    mark_id: int = Field(foreign_key="markfeedback.id")

    mark: int = Field(nullable=True)  # TODO:: int or float?
    feedback: str = Field(nullable=True)
    timestamp: datetime = Field(
        sa_column=sqlmodel.Column(
            sqlmodel.DateTime(timezone=False),
        )
    )
    marker: str = Field(nullable=False)

    mark_feedback: MarkFeedback = Relationship(back_populates="history")


class MarkFeedbackHistoryRead(SQLModel):
    mark: int
    feedback: str
    marker: str
    timestamp: datetime


class MarkFeedbackRead(SQLModel):
    question: int
    part: int
    section: int
    task: int
    mark: int
    feedback: str
    marker: str
    timestamp: datetime
    history: list[MarkFeedbackHistoryRead]
