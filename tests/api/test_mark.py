import pytest


def test_can_get_user_marks_for_question(client, mark_feedback_factory):
    mark_feedback_factory.create_batch(
        size=3, exam_id="y2023_12345_exam", question=1, username="hpotter"
    )

    res = client("y2023_12345_exam").get("/questions/1/mark")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_response_mark_has_expected_fields(client, mark_feedback_factory):
    mark = mark_feedback_factory(exam_id="y2023_12345_exam", username="hpotter")

    res = client("y2023_12345_exam").get(f"/questions/{mark.question}/mark")
    assert res.status_code == 200
    [mark_] = res.json()
    assert mark_["question"] == mark.question
    assert mark_["part"] == mark.part
    assert mark_["section"] == mark.section
    assert mark_["task"] == mark.task
    assert mark_["mark"] == mark.mark
    assert mark_["marker"] == mark.marker
    assert mark_["feedback"] == mark.feedback


def test_gets_empty_list_response_if_no_marks_exist_for_assessment(client):
    res = client("y2023_12345_exam").get("/questions/1/mark")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_can_get_user_marks_and_marks_history_for_question(
    client, mark_feedback_factory
):
    mark_feedback_factory(
        exam_id="y2023_12345_exam", question=1, username="hpotter", with_history=5
    )

    res = client("y2023_12345_exam").get("/questions/1/mark")
    assert res.status_code == 200

    [mark_] = res.json()
    assert len(mark_["history"]) == 5
