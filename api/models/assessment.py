from enum import StrEnum, auto
from operator import attrgetter

from sqlalchemy import Column
from sqlmodel import Enum, Field, Relationship, SQLModel

from api.models.student import Student


class AuthenticationMode(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    LDAP = auto()
    INTERNAL = auto()


class UserRole(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    CANDIDATE = auto()
    MARKER = auto()


class Assessment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    exam_code: str = Field(default=None, index=True)
    authentication_mode: AuthenticationMode = Field(
        sa_column=Column(
            Enum(AuthenticationMode, name="authentication_mode"),
            nullable=False,
        )
    )

    candidates: list[Student] = Relationship(
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )

    def get_role(self, username: str) -> UserRole | None:
        if username in set(map(attrgetter("username"), self.candidates)):
            return UserRole.CANDIDATE
        return None
