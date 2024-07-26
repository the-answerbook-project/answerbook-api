from sqlmodel import SQLModel


class AnswerRead(SQLModel):
    username: str
    question: int
    part: int
    section: int
    task: int
    answer: str


class AnswerWrite(SQLModel):
    question: int
    part: int
    section: int
    task: int
    answer: str
