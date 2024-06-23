from sqlmodel import SQLModel


class AnswerRead(SQLModel):
    question: int
    part: int
    section: int
    task: int
    answer: str
