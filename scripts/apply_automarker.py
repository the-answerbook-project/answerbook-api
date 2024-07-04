import requests
from automarker_types import Automarker


def mark_students(
    question_no: int,
    part_no: int,
    section_no: int,
    exam_id: str,
    automarker: Automarker,
    max_mark: int,
):
    students = get_students()

    for student in students:
        tasks = get_student_answer(student, question_no, part_no, section_no, exam_id)

        mark_res = automarker(tasks, max_mark)

        if mark_res is not None:
            (mark, feedback) = mark_res
            post_feedback(student, mark, feedback, question_no, part_no, section_no)


def get_student_answer(student, question_no, part_no, section_no, exam_id):
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


def get_students():
    res = requests.get("http://localhost:5004/students")
    return res.json()
