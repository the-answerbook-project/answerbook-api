from typing import Sequence, Type

from factory.alchemy import SQLAlchemyModelFactory

from api.factories.answer import AnswerFactory
from api.factories.assessment import AssessmentFactory, InternalCredentialsFactory
from api.factories.mark import MarkFactory, MarkHistoryFactory
from api.factories.marker import MarkerFactory
from api.factories.student import StudentFactory

all_factories: Sequence[Type[SQLAlchemyModelFactory]] = [
    AssessmentFactory,
    AnswerFactory,
    InternalCredentialsFactory,
    MarkFactory,
    MarkHistoryFactory,
    StudentFactory,
    MarkerFactory,
]
