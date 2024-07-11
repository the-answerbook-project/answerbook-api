# ----------------- tests for /{student_username}/marks
from datetime import datetime, timezone

from freezegun import freeze_time

mark_posting_ts = datetime(2024, 5, 1, 14, 22, tzinfo=timezone.utc)
valid_section = {"question": 1, "part": 1, "section": 1}


def test_can_get_student_marks_for_question(client, assessment_factory):
    assessment_factory(
        exam_code="y2023_12345_exam",
        with_students=[
            dict(
                username="hpotter",
                with_marks=[dict(question=1), dict(question=1), dict(question=1)],
            )
        ],
    )

    res = client("y2023_12345_exam").get("/hpotter/marks")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_response_mark_has_expected_fields(client, assessment_factory):
    assessment = assessment_factory(
        exam_code="y2023_12345_exam",
        with_students=[
            dict(
                username="hpotter",
                with_marks=1,
            )
        ],
    )
    [student] = assessment.candidates
    [mark] = student.marks

    res = client("y2023_12345_exam").get("/hpotter/marks")
    assert res.status_code == 200
    [mark_] = res.json()
    assert mark_["question"] == mark.question
    assert mark_["part"] == mark.part
    assert mark_["section"] == mark.section
    assert mark_["mark"] == mark.mark
    assert mark_["marker"] == mark.marker
    assert mark_["feedback"] == mark.feedback


def test_gets_empty_list_response_if_no_marks_exist_for_assessment(client):
    res = client("y2023_12345_exam").get("/hpotter/marks")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_student_marks_include_mark_history(client, assessment_factory):
    assessment_factory(
        exam_code="y2023_12345_exam",
        with_students=[
            dict(
                username="hpotter",
                with_marks=[dict(question=1, with_history=5)],
            )
        ],
    )

    res = client("y2023_12345_exam").get("/hpotter/marks")
    assert res.status_code == 200

    [mark_] = res.json()
    assert len(mark_["history"]) == 5


def test_mark_history_has_expected_fields(client, assessment_factory):
    assessment = assessment_factory(
        exam_code="y2023_12345_exam",
        with_students=[
            dict(
                username="hpotter",
                with_marks=[dict(question=1, with_history=1)],
            )
        ],
    )
    [student] = assessment.candidates
    [mark] = student.marks
    [history] = mark.history

    res = client("y2023_12345_exam").get("/hpotter/marks")
    assert res.status_code == 200

    [history_] = res.json()[0]["history"]

    assert history_["mark"] == history.mark
    assert history_["feedback"] == history.feedback
    assert history_["marker"] == history.marker


def test_cannot_post_to_marks_with_no_mark_and_no_feedback(client):
    res = client("y2023_12345_exam").post(
        f"/hpotter/marks", json={**valid_section, "feedback": None, "mark": None}
    )

    assert res.status_code == 400
    assert (
        res.json()["detail"]
        == "At least one between 'mark' and 'feedback' is required."
    )


def test_posting_mark_without_feedback_updates_root_mark(client, assessment_factory):
    assessment = assessment_factory(
        exam_code="y2023_12345_exam",
        with_students=[
            dict(
                username="hpotter",
                with_marks=[dict(**valid_section, with_history=1)],
            )
        ],
    )
    [student] = assessment.candidates
    [mark] = student.marks

    with freeze_time(mark_posting_ts):
        res = client("y2023_12345_exam").post(
            f"/{mark.username}/marks", json={**valid_section, "mark": 2.5}
        )

    assert res.status_code == 200
    mark_ = res.json()
    assert mark_["mark"] == 2.5
    assert mark_["marker"] == "adumble"  # Currently implicit
    assert mark_["feedback"] == mark.feedback
    assert mark_["timestamp"] == "2024-05-01T14:22:00+00:00"


def test_posting_feedback_without_mark_updates_root_feedback(
    client, assessment_factory
):
    assessment = assessment_factory(
        exam_code="y2023_12345_exam",
        with_students=[
            dict(
                username="hpotter",
                with_marks=[dict(**valid_section)],
            )
        ],
    )
    [student] = assessment.candidates
    [mark] = student.marks

    with freeze_time(mark_posting_ts):
        res = client("y2023_12345_exam").post(
            f"/{mark.username}/marks",
            json={**valid_section, "feedback": "Some comment"},
        )

    assert res.status_code == 200
    mark_ = res.json()
    assert mark_["mark"] == mark.mark
    assert mark_["marker"] == "adumble"  # Currently implicit
    assert mark_["feedback"] == "Some comment"
    assert mark_["timestamp"] == "2024-05-01T14:22:00+00:00"


def test_posting_mark_and_feedback_for_section(client, assessment_factory):
    assessment_factory(
        exam_code="y2023_12345_exam",
        with_students=[dict(username="hpotter")],
    )
    res = client("y2023_12345_exam").post(
        f"/hpotter/marks",
        json={**valid_section, "mark": 2.5, "feedback": "Some comment"},
    )

    assert res.status_code == 200
    mark_ = res.json()
    assert mark_["mark"] == 2.5
    assert mark_["marker"] == "adumble"  # Currently implicit
    assert mark_["feedback"] == "Some comment"


def test_posting_mark_without_feedback_adds_to_mark_history(client, assessment_factory):
    assessment = assessment_factory(
        exam_code="y2023_12345_exam",
        with_students=[
            dict(
                username="hpotter",
                with_marks=[dict(**valid_section, with_history=1)],
            )
        ],
    )
    [student] = assessment.candidates
    [mark] = student.marks
    with freeze_time(mark_posting_ts):
        res = client("y2023_12345_exam").post(
            f"/{mark.username}/marks", json={**valid_section, "mark": 2.5}
        )

    assert res.status_code == 200
    history = res.json()["history"]
    assert len(history) == 2
    [_, latest_mark] = history
    assert latest_mark["marker"] == "adumble"  # Currently implicit
    assert latest_mark["timestamp"] == "2024-05-01T14:22:00+00:00"
    assert latest_mark["feedback"] == None
    assert latest_mark["mark"] == 2.5


def test_posting_feedback_without_mark_adds_to_mark_history(client, assessment_factory):
    assessment = assessment_factory(
        exam_code="y2023_12345_exam",
        with_students=[
            dict(
                username="hpotter",
                with_marks=[dict(**valid_section, with_history=1)],
            )
        ],
    )
    [student] = assessment.candidates
    [mark] = student.marks
    with freeze_time(mark_posting_ts):
        res = client("y2023_12345_exam").post(
            f"/{mark.username}/marks",
            json={**valid_section, "feedback": "Some comment"},
        )

    assert res.status_code == 200
    history = res.json()["history"]
    assert len(history) == 2
    [_, latest_mark] = history
    assert latest_mark["marker"] == "adumble"  # Currently implicit
    assert latest_mark["timestamp"] == "2024-05-01T14:22:00+00:00"
    assert latest_mark["feedback"] == "Some comment"
    assert latest_mark["mark"] == None


# ----------------- tests for /{student_username}/answers


def test_can_get_all_student_answers_for_exam(client, assessment_factory):
    assessment_factory(
        exam_code="y2023_12345_exam",
        with_students=[
            dict(
                username="hpotter",
                with_answers=[dict(question=1) for _ in range(5)],
            )
        ],
    )
    res = client("y2023_12345_exam").get("/hpotter/answers")
    assert res.status_code == 200
    assert len(res.json()) == 5


def test_gets_empty_list_response_if_no_answers_exist_for_assessment(client):
    res = client("y2023_12345_exam").get("/hpotter/answers")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_response_answer_has_expected_fields(client, assessment_factory):
    assessment = assessment_factory(
        exam_code="y2023_12345_exam",
        with_students=[
            dict(
                username="hpotter",
                with_answers=1,
            )
        ],
    )
    [student] = assessment.candidates
    [answer] = student.answers

    res = client("y2023_12345_exam").get(f"/hpotter/answers")
    assert res.status_code == 200
    [answer_] = res.json()
    assert answer_["question"] == answer.question
    assert answer_["part"] == answer.part
    assert answer_["section"] == answer.section
    assert answer_["task"] == answer.task
    assert answer_["answer"] == answer.answer
