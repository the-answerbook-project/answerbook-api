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

    exam_id: int = Faker("pystr_format", string_format="y####_#####_exam")
    username: str = Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )
    question: int = Faker("pyint", min_value=1, max_value=10)
    part: int = Faker("pyint", min_value=1, max_value=10)
    section: int = Faker("pyint", min_value=1, max_value=20)
    task: int = Faker("pyint", min_value=1, max_value=20)
    answer: str = Faker("text", max_nb_chars=277)
    timestamp: datetime = Faker("date_this_year", before_today=True, after_today=False)
    ip: str = Faker("ipv4")
