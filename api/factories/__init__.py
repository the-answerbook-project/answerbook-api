from typing import Sequence, Type

from factory.alchemy import SQLAlchemyModelFactory

from api.factories.exam import AnswerFactory

all_factories: Sequence[Type[SQLAlchemyModelFactory]] = [AnswerFactory]
