import string
from datetime import datetime

import factory
from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from api.dependencies import get_session
from api.schemas.mark import Mark, MarkHistory


class MarkFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Mark
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    exam_id: str = Faker("pystr_format", string_format="y####_#####_exam")
    username: str = Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )
    question: int = Faker("pyint")
    part: int = Faker("pyint")
    section: int = Faker("pyint")
    task: int = Faker("pyint")
    mark: int = Faker("pyint")
    feedback: str = Faker("text", max_nb_chars=277)
    timestamp: datetime = Faker("date_this_year", before_today=True, after_today=False)
    marker: str = Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )

    @factory.post_generation
    def with_history(
        self: Mark, create: bool, history: int | list[dict], **kwargs
    ) -> None:
        if create and history:
            if isinstance(history, int):
                for _ in range(history):
                    MarkHistoryFactory(
                        mark_id=self.id,
                    )
            if isinstance(history, list):
                for h in history:
                    MarkHistoryFactory(mark_id=self.id, **h)


class MarkHistoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = MarkHistory
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    mark: int = Faker("pyint")
    feedback: str = Faker("text", max_nb_chars=277)
    timestamp: datetime = Faker("date_this_year", before_today=True, after_today=False)
    marker: str = Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )
