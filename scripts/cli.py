from typing import List

import click
import typer
from ai_automarker import make_prompt_automarker, make_value_explanation_automarker
from apply_automarker import mark_students
from automarker_types import Automarker
from automarkers import (
    blank_automarker,
    cli,
    combination_automarker,
    make_keyword_automarker,
    make_mcq_automarker,
    prime_number_automarker,
    rainbow_automarker,
)
from typer import Option

AUTOMARKERS = {
    "blank": blank_automarker,
    "rainbow": rainbow_automarker,
    "prime_number": prime_number_automarker,
    "combination": combination_automarker,
}

CHOICES = click.Choice(
    [
        "rainbow",
        "blank",
        "prime_number",
        "combination",
        "keyword",
        "mcq",
        "prompt",
        "value_explanation",
        "quit",
    ]
)


@cli.command(name="automark")
def automark(
    question: int = Option(help="Question number."),
    part: int = Option(help="Part number."),
    section: int = Option(help="Section number."),
    max_mark: int = Option(help="Maximum marks allocated to the question section."),
    exam_id: str = Option(default="y2023_12345_exam", help="Question number."),
):
    automarkers: List[Automarker] = [blank_automarker]

    automarker_name = typer.prompt(
        f"What should automarker {len(automarkers)} be?",
        default="quit",
        show_default=False,
        show_choices=True,
        type=CHOICES,
    )
    while automarker_name != "quit":
        match automarker_name:
            case "keyword":
                keyword = typer.prompt("Enter the keyword")
                automarkers.append(make_keyword_automarker(keyword))
            case "mcq":
                choices = typer.prompt("Enter the correct choices (e.g. a,d,b)")
                automarkers.append(make_mcq_automarker(choices.split(",")))
            case "description":
                prompt = typer.prompt("Enter the prompt")
                automarkers.append(make_prompt_automarker(prompt))
            case "val-explain":
                prompt = typer.prompt("Enter the prompt")
                # prompt = "Describe what type of flow given your Re value"
                model_ans = float(typer.prompt("Enter the model answer"))
                automarkers.append(make_value_explanation_automarker(prompt, model_ans))
            case _:
                if automarker_name not in AUTOMARKERS:
                    typer.echo(f"Automarker '{automarker_name}' not found.")
                    raise typer.Exit(code=1)
                automarkers.append(AUTOMARKERS[automarker_name])

        automarker_name = typer.prompt(
            f"What should automarker {len(automarkers)} be?",
            default="quit",
            show_default=False,
            show_choices=True,
            type=CHOICES,
        )

    mark_students(
        question,
        part,
        section,
        exam_id,
        automarkers,
        max_mark,
    )


if __name__ == "__main__":
    cli()
