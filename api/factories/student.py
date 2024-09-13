import string

import factory
from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from api.factories.answer import AnswerFactory
from api.factories.mark import MarkFactory
from api.models.student import Student


class StudentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Student
        sqlalchemy_session_persistence = "commit"

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
                    AnswerFactory(
                        assessment_id=self.assessment_id,
                        username=self.username,
                    )
            if isinstance(answers, list):
                for a in answers:
                    AnswerFactory(
                        assessment_id=self.assessment_id,
                        username=self.username,
                        **a,
                    )

    @factory.post_generation
    def with_marks(self, create: bool, marks: int | list[dict], **kwargs) -> None:
        if create and marks:
            if isinstance(marks, int):
                for _ in range(marks):
                    MarkFactory(
                        assessment_id=self.assessment_id,
                        username=self.username,
                    )
            if isinstance(marks, list):
                for m in marks:
                    MarkFactory(
                        assessment_id=self.assessment_id,
                        username=self.username,
                        **m,
                    )
