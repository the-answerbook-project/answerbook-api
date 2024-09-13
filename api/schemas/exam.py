from datetime import datetime, timedelta
from enum import StrEnum, auto

from pydantic import field_validator, model_validator
from sqlmodel import SQLModel

from api.schemas import BaseSchema
from api.utils import (
    is_lowercase_roman_numeral,
    is_single_lowercase_alpha,
    lowercase_alpha_to_int,
    lowercase_roman_to_int,
    parse_interval,
)


class TaskType(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    ESSAY = auto()
    INTEGER = auto()
    FLAG = auto()
    CODE = auto()
    MULTIPLE_CHOICE_SELECT_ONE = auto()
    MULTIPLE_CHOICE_SELECT_SEVERAL = auto()
    PROCESSED_HANDWRITING = auto()
    RAW_HANDWRITING = auto()


class MCQOption(SQLModel):
    value: str
    label: str


class Task(SQLModel):
    type: TaskType
    instructions: str | None = None
    lines: int | None = None
    choices: list[MCQOption] | None = None

    @field_validator("type", mode="before")
    def translate_type(cls, v):
        v = v.upper().replace(" ", "_")
        if v in TaskType:
            return TaskType[v]
        raise ValueError(f"Invalid task type: {v}")

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
    title: str | None = None
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


class AssessmentSpec(SQLModel):
    course_code: str
    course_name: str
    alternative_codes: list[str]
    begins: datetime
    duration: int
    delayed_starts: dict[str, str] = {}
    extensions: dict[str, str] = {}
    labelled_subparts: bool = True
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

    def computed_beginning_for_candidate(self, username):
        delay = parse_interval(self.delayed_starts.get(username, "0"))
        return self.begins + timedelta(minutes=delay)

    def computed_duration_for_candidate(self, username):
        ext = parse_interval(self.extensions.get(username, "0"))
        return self.duration + ext

    def computed_end_time_for_candidate(self, username):
        duration = self.computed_duration_for_candidate(username)
        duration_td = timedelta(minutes=duration)
        return self.computed_beginning_for_candidate(username) + duration_td


class AssessmentHeading(BaseSchema):
    course_code: str
    course_name: str
    begins: datetime
    duration: int
    rubric: Rubric
