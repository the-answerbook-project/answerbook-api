from typing import List

import typer
from ai_automarker import make_prompt_automarker
from automarker_types import Automarker

cli = typer.Typer()


def make_mcq_automarker(correct_values: List[str]) -> Automarker:
    def mcq_automarker(tasks, max_mark) -> tuple[int, str] | None:
        correct_values_ = correct_values[:]
        for selection in tasks[0]["answer"].split(","):
            if selection not in correct_values_:
                return 0, f"Incorrect selection {selection}"
            correct_values_.remove(selection)

        if correct_values_:
            return 0, f"Missing correct answers: {", ".join(correct_values_)}"

        return max_mark, "Well done"

    return mcq_automarker


def blank_automarker(tasks, _) -> tuple[int, str] | None:
    if not tasks:
        return 0, "Not attempted. Your paper shall be burned in the next class."
    return None


def rainbow_automarker(tasks, max_mark) -> tuple[int, str] | None:
    rainbow_colours = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    if len(tasks) != 3:
        return 0, "Enter 3 colours next time."
    for task in tasks:
        if task["answer"].strip().lower() not in rainbow_colours:
            return 0, "These are not 3 distinct rainbow colours."
        rainbow_colours.remove(task["answer"].strip().lower())
    return max_mark, "Good job! You have entered 3 distinct rainbow colours."


def make_keyword_automarker(keyword) -> Automarker:
    def keyword_automarker(tasks, max_mark) -> tuple[int, str] | None:
        if keyword.lower() not in tasks[0]["answer"].strip().lower():
            return 0, f"Keyword '{keyword}' not found."
        return max_mark, "Good job! You have entered the keyword."

    return keyword_automarker


# 3ai) Enter a prime number between 1 and 10. Explain why it is a prime number.
def prime_number_automarker(tasks, max_mark) -> tuple[int, str] | None:
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
        mark += 1

    if "divisible" not in tasks[1]["answer"].strip().lower():
        feedback += " Keyword 'divisible' not found."
    else:
        mark += max_mark - 1

    return mark, feedback.strip() or "Good job! You have entered a prime number."


# combining automarkers


def combination_automarker(tasks, max_mark):
    mark = 0
    feedback = ""

    prompt_automarker = make_prompt_automarker(
        "Explain what two things cause a rainbow to form."
    )
    partial_mark = max_mark / 2
    res1 = prompt_automarker(tasks, partial_mark)
    if res1 is not None:
        (sum1, feedback1) = res1
        mark += sum1
        feedback += feedback1

    res2 = rainbow_automarker(tasks[1:], max_mark - partial_mark)
    if res2 is not None:
        (sum2, feedback2) = res2
        mark += sum2
        feedback += feedback2

    return mark, feedback
