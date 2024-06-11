import string
from datetime import datetime

from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from api.dependencies import get_session
from api.schemas.answer import Answer


class AnswerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Answer
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    exam_id: int = Faker("pystr_format", string_format="y####_#####_exam")
    username: str = Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )
    question: int = Faker("pyint")
    part: int = Faker("pyint")
    section: int = Faker("pyint")
    task: int = Faker("pyint")
    answer: str = Faker("text", max_nb_chars=277)
    timestamp: datetime = Faker("date_this_year", before_today=True, after_today=False)
    ip: str = Faker("ipv4")
