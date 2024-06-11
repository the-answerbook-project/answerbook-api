from typing import Sequence, Type

from factory.alchemy import SQLAlchemyModelFactory

from api.factories.answer import AnswerFactory
from api.factories.mark_feedback import MarkFeedbackFactory

all_factories: Sequence[Type[SQLAlchemyModelFactory]] = [
    AnswerFactory,
    MarkFeedbackFactory,
]
