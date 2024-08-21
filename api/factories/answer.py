import string
from datetime import datetime

import factory
from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from api.models.answer import Answer, AnswerHistory


class AnswerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Answer
        sqlalchemy_session_persistence = "commit"

    username: str = Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )
    question: int = Faker("pyint", min_value=1, max_value=10)
    part: int = Faker("pyint", min_value=1, max_value=10)
    section: int = Faker("pyint", min_value=1, max_value=20)
    task: int = Faker("pyint", min_value=1, max_value=20)
    answer: str = Faker("text", max_nb_chars=277)
    ip: str = Faker("ipv4")

    @factory.post_generation
    def with_history(
        self: Answer, create: bool, history: int | list[dict], **kwargs
    ) -> None:
        if create and history:
            if isinstance(history, int):
                for _ in range(history):
                    AnswerHistoryFactory(answer_id=self.id)
            if isinstance(history, list):
                for h in history:
                    AnswerHistoryFactory(answer_id=self.id, **h)


class AnswerHistoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = AnswerHistory
        sqlalchemy_session_persistence = "commit"

    answer: str = Faker("text", max_nb_chars=277)
    timestamp: datetime = Faker("date_this_year", before_today=True, after_today=False)
