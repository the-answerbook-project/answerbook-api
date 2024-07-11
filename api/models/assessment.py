from enum import StrEnum, auto

from sqlmodel import Field, SQLModel


class AuthenticationMode(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    LDAP = auto()
    INTERNAL = auto()


class Assessment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    exam_code: str = Field(default=None, index=True)
    authentication_mode: AuthenticationMode = Field(nullable=False)
