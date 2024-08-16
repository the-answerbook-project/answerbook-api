import string

import factory
from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from api.factories.marker import MarkerFactory
from api.factories.student import StudentFactory
from api.models.assessment import Assessment, AuthenticationMode
from api.models.internal_credentials import InternalCredentials


class InternalCredentialsFactory(SQLAlchemyModelFactory):
    class Meta:
        model = InternalCredentials
        sqlalchemy_session_persistence = "commit"

    username: str = Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )
    hashed_password: str = Faker("pystr_format")


class AssessmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Assessment
        sqlalchemy_session_persistence = "commit"

    code: str = Faker("pystr_format", string_format="y####_#####_exam")
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
                        exam_id=self.code,
                    )
            if isinstance(students, list):
                for s in students:
                    StudentFactory(assessment_id=self.id, exam_id=self.code, **s)

    @factory.post_generation
    def with_markers(
        self: Assessment, create: bool, markers: int | list[dict], **kwargs
    ) -> None:
        if create and markers:
            if isinstance(markers, int):
                for _ in range(markers):
                    MarkerFactory(
                        assessment_id=self.id,
                    )
            if isinstance(markers, list):
                for m in markers:
                    MarkerFactory(assessment_id=self.id, **m)

    @factory.post_generation
    def with_credentials(
        self: Assessment, create: bool, credentials: list[dict], **kwargs
    ) -> None:
        if create and credentials:
            if isinstance(credentials, list):
                for c in credentials:
                    InternalCredentialsFactory(assessment_id=self.id, **c)
