from contextlib import contextmanager

import typer
from sqlalchemy import text
from sqlmodel import SQLModel
from typer import Argument

from api.dependencies import get_session
from api.factories import AnswerFactory, StudentFactory, all_factories

cli = typer.Typer()


@contextmanager
def dynamic_session():
    session = next(get_session())
    for f in all_factories:
        f._meta.sqlalchemy_session = session
    yield


@cli.command(name="erase_data")
def erase_data():
    """
    WARNING: This command will erase all data from the tables without dropping the tables.
    """
    confirm = typer.confirm(
        "Are you sure you want to erase all data from the tables? This action cannot be undone."
    )
    if confirm:
        session = next(get_session())

        # Iterate over all tables and delete data
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.execute(text(f"DELETE FROM {table.name}"))  # nosec
        session.commit()
        typer.echo("All data erased successfully.")
    else:
        typer.echo("Operation cancelled.")


@cli.command(name="populate_db")
def populate_db(
    year: str = Argument(help="Academic year in short form e.g. 2324 for 2023-2024"),
):
    """
    Populates the database with dummy data.
    """
    with dynamic_session():
        StudentFactory(username="hgranger", exam_id="y2023_12345_exam")
        StudentFactory(username="hpotter", exam_id="y2023_12345_exam")
        AnswerFactory(
            exam_id="y2023_12345_exam",
            username="hpotter",
            question=1,
            part=1,
            section=1,
            task=1,
        )
        AnswerFactory(
            exam_id="y2023_12345_exam",
            username="hpotter",
            question=1,
            part=1,
            section=1,
            task=2,
        )
        AnswerFactory(
            exam_id="y2023_12345_exam",
            username="hpotter",
            question=1,
            part=1,
            section=1,
            task=3,
        )
        AnswerFactory(
            exam_id="y2023_12345_exam",
            username="hpotter",
            question=2,
            part=1,
            section=1,
            task=1,
        )
        AnswerFactory(
            exam_id="y2023_12345_exam",
            username="hpotter",
            question=2,
            part=1,
            section=1,
            task=1,
        )
        AnswerFactory(
            exam_id="y2023_12345_exam",
            username="hpotter",
            question=3,
            part=1,
            section=1,
            task=1,
        )

        StudentFactory(username="hgranger", exam_id="y2023_12345_exam")
        AnswerFactory(
            exam_id="y2023_12345_exam",
            username="hgranger",
            question=1,
            part=1,
            section=1,
            task=1,
        )
        AnswerFactory(
            exam_id="y2023_12345_exam",
            username="hgranger",
            question=1,
            part=1,
            section=1,
            task=2,
        )
        AnswerFactory(
            exam_id="y2023_12345_exam",
            username="hgranger",
            question=1,
            part=1,
            section=1,
            task=3,
        )
        AnswerFactory(
            exam_id="y2023_12345_exam",
            username="hgranger",
            question=2,
            part=1,
            section=1,
            task=1,
        )
        AnswerFactory(
            exam_id="y2023_12345_exam",
            username="hgranger",
            question=2,
            part=1,
            section=1,
            task=1,
        )
        AnswerFactory(
            exam_id="y2023_12345_exam",
            username="hgranger",
            question=3,
            part=1,
            section=1,
            task=1,
        )
    print("Database populated successfully.")


@cli.command(name="populate_demo")
def populate_demo_data():
    """
    Populates the database with dummy data.
    """

    with dynamic_session():
        StudentFactory(username="hgranger", exam_id="y2023_12345_exam")
        StudentFactory(username="hpotter", exam_id="y2023_12345_exam")
        StudentFactory(username="rweasley", exam_id="y2023_12345_exam")
        StudentFactory(username="kss22", exam_id="y2023_12345_exam")
        StudentFactory(username="bn322", exam_id="y2023_12345_exam")
        StudentFactory(username="ma4723", exam_id="y2023_12345_exam")
        StudentFactory(username="ab1223", exam_id="y2023_12345_exam")

    print("Demo data populated Database populated successfully.")


if __name__ == "__main__":
    cli()
