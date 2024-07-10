import string
from datetime import datetime

import factory
from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from api.dependencies import get_session
from api.factories import AnswerFactory, MarkFactory
from api.models.student import Student


class StudentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Student
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    exam_id: str = Faker("pystr_format", string_format="y####_#####_exam")
    username: str = Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )

    firstname: str = Faker("first_name")
    lastname: str = Faker("last_name")
    cid: str = Faker("pystr_format", string_format="########")
    degree_code: str = Faker("pystr_format", string_format="???#")

    @factory.post_generation
    def with_answers(self, create: bool, answers: int | list[dict], **kwargs) -> None:
        if create and answers:
            if isinstance(answers, int):
                for _ in range(answers):
                    AnswerFactory(exam_id=self.exam_id, username=self.username)
            if isinstance(answers, list):
                for a in answers:
                    AnswerFactory(exam_id=self.exam_id, username=self.username, **a)

    @factory.post_generation
    def with_marks(self, create: bool, marks: int | list[dict], **kwargs) -> None:
        if create and marks:
            if isinstance(marks, int):
                for _ in range(marks):
                    MarkFactory(exam_id=self.exam_id, username=self.username)
            if isinstance(marks, list):
                for m in marks:
                    MarkFactory(exam_id=self.exam_id, username=self.username, **m)
