import string
from datetime import datetime

import factory
from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from api.dependencies import get_session
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
