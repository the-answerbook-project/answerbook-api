from datetime import datetime

from pydantic import field_validator, model_validator
from sqlmodel import SQLModel

from api.utils import (
    is_lowercase_roman_numeral,
    is_single_lowercase_alpha,
    lowercase_alpha_to_int,
    lowercase_roman_to_int,
)


class Task(SQLModel):
    task: str | None
    type: str


class Section(SQLModel):
    instructions: str | None
    maximum_mark: int
    tasks: list[Task]


class Part(SQLModel):
    instructions: str | None
    sections: dict[int, Section]

    @model_validator(mode="before")
    def translate_roman_index_to_number(cls, values):
        values["sections"] = {
            lowercase_roman_to_int(k): Section(**s)
            for k, s in values.items()
            if is_lowercase_roman_numeral(k)
        }
        return values


class Question(SQLModel):
    title: str
    show_part_weights: bool | None
    instructions: str | None
    parts: dict[int, Part]

    @model_validator(mode="before")
    def parse_parts(cls, values):
        values["parts"] = {
            lowercase_alpha_to_int(k): Part(**p)
            for k, p in values.items()
            if is_single_lowercase_alpha(k)
        }
        return values


class Rubric(SQLModel):
    instructions: str | None
    questions_to_answer: int


class Assessment(SQLModel):
    course_code: str
    course_name: str
    alternative_codes: list[str]
    begins: datetime
    duration: int
    extensions: dict[str, str]
    labelled_subparts: bool
    questions: dict[int, Question]

    @field_validator("course_code", mode="before")
    def parse_course_code(cls, value):
        return str(value)

    @field_validator("alternative_codes", mode="before")
    def parse_alternative_codes(cls, values):
        return list(map(str, values))

    @model_validator(mode="before")
    def parse_questions(cls, values):
        values["questions"] = {
            int(k): Question(**q) for k, q in values.items() if k.isnumeric()
        }
        return values
