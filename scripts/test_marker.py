from sqlmodel import Session

from api.database.connection import engine
from api.factories.answer import AnswerFactory
from api.factories.student import StudentFactory
from scripts.get_answers import main as get_answers

connection = engine.connect()

with Session(connection) as session:
    StudentFactory(username="hpotter")
    AnswerFactory(username="hpotter", question=1, part=1, section=1)
    get_answers()
    connection.close()
