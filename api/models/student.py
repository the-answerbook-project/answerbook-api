from sqlmodel import Field, SQLModel


class Student(SQLModel, table=True):
    id: int = Field(primary_key=True)
    exam_id: str = Field(default=None)
    username: str = Field(nullable=False)
    firstname: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    cid: str = Field(nullable=False)
    degree_code: str = Field(nullable=False)
