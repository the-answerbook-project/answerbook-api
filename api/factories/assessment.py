import string

import factory
from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from api.dependencies import get_session
from api.factories.student import StudentFactory
from api.models.assessment import Assessment, AuthenticationMode


class AssessmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Assessment
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    exam_code: str = Faker("pystr_format", string_format="y####_#####_exam")
    authentication_mode: AuthenticationMode = AuthenticationMode.INTERNAL

    @factory.post_generation
    def with_students(
        self: Assessment, create: bool, students: int | list[dict], **kwargs
    ) -> None:
        if create and students:
            if isinstance(students, int):
                for _ in range(students):
                    StudentFactory(
                        assessment_id=self.id,
                        exam_id=self.exam_code,
                    )
            if isinstance(students, list):
                for s in students:
                    StudentFactory(assessment_id=self.id, exam_id=self.exam_code, **s)
