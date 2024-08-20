from datetime import datetime

from sqlmodel import SQLModel


class AnswerRead(SQLModel):
    username: str
    question: int
    part: int
    section: int
    task: int
    answer: str
    timestamp: datetime


class AnswerWrite(SQLModel):
    question: int
    part: int
    section: int
    task: int
    answer: str
