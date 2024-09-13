import string

from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from api.models.student import Marker


class MarkerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Marker
        sqlalchemy_session_persistence = "commit"

    username: str = Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )

    firstname: str = Faker("first_name")
    lastname: str = Faker("last_name")
