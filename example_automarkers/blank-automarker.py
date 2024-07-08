import json
from collections import defaultdict
from operator import itemgetter

import requests
import typer

students_url = "/students"
questions_url = "/questions"


def build_lookup_key(*tokens):
    return "-".join(map(str, tokens))


def build_lookup_table(items):
    table = defaultdict(lambda: None)
    for item in items:
        keys = ["question", "part", "section"]
        if "task" in item:
            keys.append("task")
        key = build_lookup_key(*itemgetter(*keys)(item))
        table[key] = item
    return table


def make_request(url, method="get", params=None, data=None):
    res = getattr(requests, method)(url, params=params, data=data)
    if res.status_code == requests.codes.ok:
        return res.json()
    raise Exception(
        f"Request for '{url}' failed with status code {res.status_code}: {res.text}"
    )


def generate_mark(
    username: str, task: dict, current_mark: dict | None, answer: str | None
) -> dict | None:
    if current_mark is None and answer is None:
        return {"mark": 0, "feedback": "No answer submitted"}
    return None


def main(
    root_url: str = typer.Argument(
        ...,
        help="Root URL of your answerbook exam e.g. http://answerbook.doc.ic.ac.uk/2024/60005/exam",
    ),
):
    questions = make_request(root_url + questions_url)
    students = make_request(root_url + students_url)
    for student in students:
        username = student["username"]
        marks_url = root_url + f"/{username}/marks"
        mark_lookup = build_lookup_table(make_request(marks_url))
        ans_lookup = build_lookup_table(make_request(root_url + f"/{username}/answers"))
        for q, question in questions.items():
            for p, parts in question["parts"].items():
                for s, section in parts["sections"].items():
                    for t, task in enumerate(section["tasks"]):
                        current_mark = mark_lookup[build_lookup_key(q, p, s)]
                        answer = ans_lookup.get(build_lookup_key(q, p, s, t), {})
                        answer = answer.get("answer")
                        payload = generate_mark(username, task, current_mark, answer)
                        if payload is not None:
                            payload = {
                                **payload,
                                "question": q,
                                "part": p,
                                "section": s,
                            }
                            make_request(marks_url, "post", data=json.dumps(payload))


if __name__ == "__main__":
    typer.run(main)
