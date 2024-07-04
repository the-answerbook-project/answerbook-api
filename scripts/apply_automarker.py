from typing import List, Optional

import requests
from automarker_types import Automarker


def mark_students(
    question_no: int,
    part_no: int,
    section_no: int,
    exam_id: str,
    automarkers: List[Automarker],
    max_mark: int,
    test_mode: bool,
    limit: Optional[int],
):
    students = get_students(limit)

    for student in students:
        tasks = get_student_answer(student, question_no, part_no, section_no, exam_id)

        for automarker in automarkers:
            mark_res = automarker(tasks, max_mark)

            if mark_res is not None:
                (mark, feedback) = mark_res

                if test_mode:
                    print()
                    print("Student answer:")
                    print(
                        "<No attempt>"
                        if not tasks
                        else "\n".join(
                            [f"Task {task["task"]}: {task["answer"]}" for task in tasks]
                        )
                    )
                    print()
                    print(f"Mark: {mark} / {max_mark}")
                    print(f"Feedback: {feedback}")
                    print()
                else:
                    post_feedback(
                        student, mark, feedback, question_no, part_no, section_no
                    )

                break


def get_student_answer(student, question_no, part_no, section_no, _exam_id):
    res = requests.get(
        f"http://localhost:5004/answers/{student['username']}/question/{question_no}/part/{part_no}/section/{section_no}"
    )
    return res.json()


def post_feedback(student, mark, feedback, question_no, part_no, section_no):
    requests.post(
        f"http://localhost:5004/{student['username']}/marks",
        json={
            "question": question_no,
            "part": part_no,
            "section": section_no,
            "mark": mark,
            "feedback": feedback,
            "marker": "Automark",
        },
    )


def get_students(limit: Optional[int]):
    res = requests.get("http://localhost:5004/students")
    return res.json()[:limit] if limit is not None else res.json()
