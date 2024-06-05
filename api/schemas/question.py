from datetime import datetime
from enum import StrEnum, auto

from pydantic import field_validator, model_validator
from sqlmodel import SQLModel

from api.utils import (
    is_lowercase_roman_numeral,
    is_single_lowercase_alpha,
    lowercase_alpha_to_int,
    lowercase_roman_to_int,
)


class TaskType(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower().replace("_", " ")

    ESSAY = auto()
    INTEGER = auto()
    FLAG = auto()
    CODE = auto()
    MULTIPLE_CHOICE_SELECT_ONE = auto()
    MULTIPLE_CHOICE_SELECT_SEVERAL = auto()


class MCQOption(SQLModel):
    value: str
    label: str


class Task(SQLModel):
    type: TaskType
    instructions: str | None = None
    lines: int | None = None
    choices: list[MCQOption] | None = None

    @model_validator(mode="before")
    def parse_choices(cls, value):
        if "choices" in value:
            value["choices"] = [
                {"value": v, "label": l} for c in value["choices"] for v, l in c.items()
            ]
        return value


class Section(SQLModel):
    instructions: str | None = None
    maximum_mark: int
    tasks: list[Task]


class Part(SQLModel):
    instructions: str | None = None
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
    show_part_weights: bool = True
    instructions: str | None = None
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
    instructions: str | None = None
    questions_to_answer: int


class Assessment(SQLModel):
    course_code: str
    course_name: str
    alternative_codes: list[str]
    begins: datetime
    duration: int
    extensions: dict[str, str]
    labelled_subparts: bool
    rubric: Rubric
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


class AssessmentSummary(SQLModel):
    course_code: str
    course_name: str
    begins: datetime
    duration: int
    rubric: Rubric
