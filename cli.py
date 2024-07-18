import json
from contextlib import contextmanager

import typer
from sqlalchemy import text
from sqlmodel import SQLModel

from api.dependencies import get_session
from api.factories import (
    AssessmentFactory,
    all_factories,
)

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
def populate_db():
    """
    Populates the database with dummy data.
    """
    with dynamic_session():
        AssessmentFactory(
            code="y2023_12345_exam",
            with_students=[
                dict(
                    username="hgranger",
                    with_answers=[
                        dict(question=1, part=1, section=1, task=1, answer="c,d"),
                        dict(question=1, part=1, section=1, task=2),
                        dict(question=1, part=2, section=1, task=1, answer="a"),
                        dict(
                            question=1,
                            part=3,
                            section=1,
                            task=1,
                            answer=json.dumps({"latex": r"\frac{1}{3}x^{3}+C"}),
                        ),
                        dict(
                            question=1,
                            part=3,
                            section=1,
                            task=2,
                            answer=json.dumps({"latex": r"2x"}),
                        ),
                        dict(question=2, part=1, section=1, task=1),
                    ],
                ),
                dict(
                    username="hpotter",
                    with_answers=[
                        dict(question=1, part=1, section=1, task=1, answer="c,e"),
                        dict(question=1, part=1, section=1, task=2),
                        dict(question=1, part=2, section=1, task=1, answer="b"),
                        dict(
                            question=1,
                            part=3,
                            section=1,
                            task=1,
                            answer=json.dumps({"latex": r"\int x^2"}),
                        ),
                        dict(
                            question=1,
                            part=3,
                            section=1,
                            task=2,
                            answer=json.dumps({"latex": r"2x"}),
                        ),
                        dict(question=2, part=1, section=1, task=1),
                    ],
                ),
            ],
        )
    print("Database populated successfully.")


@cli.command(name="populate_demo")
def populate_demo_data():
    """
    Populates the database with demo data.
    """

    with dynamic_session():
        AssessmentFactory(
            code="y2023_12345_exam",
            with_students=[
                dict(username="hgranger"),
                dict(username="hpotter"),
                dict(username="rweasley"),
            ],
        )
    print("Demo data populated Database populated successfully.")


if __name__ == "__main__":
    cli()
