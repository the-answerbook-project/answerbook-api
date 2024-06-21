from datetime import datetime

import sqlmodel
from sqlmodel import Field, Relationship, SQLModel


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
        sa_column=sqlmodel.Column(
            sqlmodel.DateTime(timezone=False),
        )
    )
    marker: str = Field(nullable=False)

    history: list["MarkHistory"] = Relationship(back_populates="current_mark")


class MarkHistory(SQLModel, table=True):
    __tablename__ = "mark_history"
    id: int | None = Field(primary_key=True, default=None)
    mark_id: int = Field(foreign_key="mark.id")

    mark: float = Field(nullable=True)  # TODO:: int or float?
    feedback: str = Field(nullable=True)
    timestamp: datetime = Field(
        sa_column=sqlmodel.Column(
            sqlmodel.DateTime(timezone=False),
        )
    )
    marker: str = Field(nullable=False)
    current_mark: Mark = Relationship(back_populates="history")


class MarkHistoryRead(SQLModel):
    mark: float | None
    feedback: str | None
    marker: str
    timestamp: datetime


class MarkRead(SQLModel):
    question: int
    part: int
    section: int
    mark: float | None
    feedback: str | None
    marker: str
    timestamp: datetime
    history: list[MarkHistoryRead]
