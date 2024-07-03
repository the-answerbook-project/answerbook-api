from typing import Callable

import typer
from ai_automarker import make_prompt_automarker, make_value_explanation_automarker
from apply_automarker import mark_students
from typer import Argument, Option

cli = typer.Typer()


@cli.command(name="automark")
def automark(
    automarker_name: str = Argument(help="Name of the automarker to run."),
    question: int = Option(help="Question number."),
    part: int = Option(help="Part number."),
    section: int = Option(help="Section number."),
    exam_id: str = Option(default="y2023_12345_exam", help="Question number."),
):
    match automarker_name:
        case "keyword":
            keyword = typer.prompt("Enter the keyword")
            automarker = make_keyword_automarker(keyword)
        case "description":
            prompt = typer.prompt("Enter the prompt")
            automarker = make_prompt_automarker(prompt, 10)
        case "val-explain":
            prompt = typer.prompt("Enter the prompt")
            # prompt = "Describe what type of flow given your Re value"
            model_ans = float(typer.prompt("Enter the model answer"))
            automarker = make_value_explanation_automarker(prompt, model_ans)
        case _:
            if automarker_name not in AUTOMARKERS:
                typer.echo(f"Automarker '{automarker_name}' not found.")
                raise typer.Exit(code=1)
            automarker = AUTOMARKERS[automarker_name]

    mark_students(
        question,
        part,
        section,
        exam_id,
        automarker,
    )


def zero_automarker(tasks) -> tuple[int, str] | None:
    if not tasks:
        return (0, "Not attempted. Your paper shall be burned in the next class.")
    return None


def rainbow_automarker(tasks) -> tuple[int, str] | None:
    RAINBOW_COLOURS = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    if len(tasks) != 3:
        return (0, "Enter 3 colours next time.")
    for task in tasks:
        if task["answer"].strip().lower() not in RAINBOW_COLOURS:
            return (0, "These are not 3 distinct rainbow colours.")
        RAINBOW_COLOURS.remove(task["answer"].strip().lower())
    return (20, "Good job! You have entered 3 distinct rainbow colours.")


def make_keyword_automarker(keyword) -> Callable[[dict], tuple[int, str] | None]:
    def keyword_automarker(tasks) -> tuple[int, str] | None:
        if not tasks:
            return None
        if keyword.lower() not in tasks[0]["answer"].strip().lower():
            return (0, f"Keyword '{keyword}' not found.")
        return (20, "Good job! You have entered the keyword.")

    return keyword_automarker


# 3ai) Enter a prime number between 1 and 10. Explain why it is a prime number.
def prime_number_automarker(tasks) -> tuple[int, str] | None:
    if not tasks:
        return None

    mark = 0
    feedback = ""

    try:
        answer = int(tasks[0]["answer"].strip())
    except ValueError:
        feedback = "Not a number."
        answer = 0

    if answer not in [2, 3, 5, 7]:
        feedback += " Not a prime number."
    else:
        mark += 10

    if "divisible" not in tasks[1]["answer"].strip().lower():
        feedback += " Keyword 'divisible' not found."
    else:
        mark += 10

    return (mark, feedback.strip() or "Good job! You have entered a prime number.")


# combining automarkers


def combination_automarker(tasks):
    sum = 0
    feedback = ""

    prompt_automarker = make_prompt_automarker(
        "Explain what two things cause a rainbow to form.", 5
    )
    res1 = prompt_automarker(tasks)
    if res1 is not None:
        (sum1, feedback1) = res1
        sum += sum1
        feedback += feedback1

    res2 = rainbow_automarker(tasks[1:])
    if res2 is not None:
        (sum2, feedback2) = res2
        sum += sum2
        feedback += feedback2

    return (sum, feedback)


AUTOMARKERS = {
    "zero": zero_automarker,
    "rainbow": rainbow_automarker,
    "prime_number": prime_number_automarker,
    "combination": combination_automarker,
}

if __name__ == "__main__":
    cli()