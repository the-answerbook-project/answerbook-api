from datetime import datetime

import sqlmodel
from sqlmodel import Field, SQLModel


class MarkFeedback(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
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

    # TODO : Mark approved/submitted?


class MarkFeedbackRead(SQLModel):
    question: int
    part: int
    section: int
    task: int
    mark: int
    feedback: str
    marker: str
    timestamp: datetime
