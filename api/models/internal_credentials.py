from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class InternalCredentials(SQLModel, table=True):
    __tablename__ = "internal_credentials"
    __table_args__ = (UniqueConstraint("assessment_id", "username"),)
    id: int = Field(primary_key=True)
    assessment_id: int = Field(default=None, foreign_key="assessment.id", index=True)
    username: str = Field(
        nullable=False,
    )
    hashed_password: str
