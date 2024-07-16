from sqlmodel import Field, Relationship, SQLModel

from api.models.answer import Answer
from api.models.mark import Mark


class Student(SQLModel, table=True):
    id: int = Field(primary_key=True)
    exam_id: str = Field(default=None, index=True)
    assessment_id: int = Field(default=None, foreign_key="assessment.id", index=True)
    username: str = Field(nullable=False, unique=True)
    firstname: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    cid: str = Field(nullable=False)
    degree_code: str = Field(nullable=False)

    answers: list[Answer] = Relationship(
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    marks: list[Mark] = Relationship(
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
