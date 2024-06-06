from datetime import datetime
import sqlmodel
from sqlmodel import SQLModel, Field


class Answer(SQLModel,table=True):
    id: int | None = Field(primary_key=True, default=None)
    exam_id: int = Field(default=None)  # TODO:: FK?
    username: str = Field(nullable=False)
    question: int = Field(default=None)
    part: int = Field(default=None)
    section: int = Field(default=None)
    task: int = Field(default=None)
    answer: str = Field(nullable=True)
    timestamp: datetime = Field(
        sa_column=sqlmodel.Column(
            sqlmodel.DateTime(timezone=False),  # TODO:: True or false?
        )
    )

    ip: str = Field(nullable=True)  # TODO:: inet
