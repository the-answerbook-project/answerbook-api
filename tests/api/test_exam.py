import pytest


def test_can_get_summary_for_exam(client):
    res = client("simple").get("/summary")
    assert res.status_code == 200
    summary = res.json()
    assert summary["course_code"] == "11111"
    assert summary["course_name"] == "The course name"
    assert summary["duration"] == 120
    assert (
        summary["rubric"]["instructions"] == "Some general instructions for this exam."
    )
    assert summary["rubric"]["questions_to_answer"] == 3
    assert summary["begins"] == "2019-01-01T08:00:00+00:00"


@pytest.mark.parametrize(
    "exam_id, expected_questions", [("simple", 1), ("multiple_questions", 2)]
)
def test_can_get_questions_for_exam(client, exam_id, expected_questions):
    res = client(exam_id).get("/questions")
    assert res.status_code == 200
    assert len(res.json()) == expected_questions


def test_questions_for_exam_have_expected_fields(client):
    res = client("simple").get("/questions")
    assert res.status_code == 200
    questions = res.json()
    assert questions["1"]["title"] == "Title of the question"
    assert questions["1"]["instructions"] == "Some instructions for this question."
    assert questions["1"]["show_part_weights"] is False
    assert len(questions["1"]["parts"]) == 1
