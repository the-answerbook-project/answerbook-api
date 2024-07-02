from enum import auto
from typing import Callable

import requests


def zero_automarker(tasks) -> tuple[int, str] | None:
    if not tasks:
        return (0, "Not attempted. Your paper shall be burned in the next class.")
    return None


def main():
    mark_students(
        question_no=1,
        part_no=1,
        section_no=2,
        exam_id="y2023_12345_exam",
        automarker=zero_automarker,
    )


def mark_students(
    question_no: int,
    part_no: int,
    section_no: int,
    exam_id: str,
    automarker: Callable[[dict], tuple[int, str] | None],
):
    res = get_students()
    students = res.json()
    for student in students:
        tasks = get_student_answer(student, question_no, part_no, section_no, exam_id)

        mark_res = automarker(tasks)

        if mark_res is not None:
            (mark, feedback) = mark_res
            post_feedback(student, mark, feedback, question_no, part_no, section_no)


def get_student_answer(student, question_no, part_no, section_no, exam_id):
    res = requests.get(
        f"http://localhost:5004/answers/{student['username']}/question/{question_no}/part/{part_no}/section/{section_no}"
    )
    tasks = res.json()
    return tasks


def post_feedback(student, mark, feedback, question_no, part_no, section_no):
    requests.post(
        f"http://localhost:5004/{student['username']}/marks",
        json={
            "question": question_no,
            "part": part_no,
            "section": section_no,
            "mark": mark,
            "feedback": feedback,
        },
    )


def get_students():
    res = requests.get("http://localhost:5004/students")
    return res


if __name__ == "__main__":
    main()
