import pytest


def test_can_get_user_marks_for_question(client, mark_factory):
    mark_factory.create_batch(
        size=3, exam_id="y2023_12345_exam", question=1, username="hpotter"
    )

    res = client("y2023_12345_exam").get("/marks/hpotter")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_response_mark_has_expected_fields(client, mark_factory):
    mark = mark_factory(exam_id="y2023_12345_exam", username="hpotter")

    res = client("y2023_12345_exam").get(f"/marks/hpotter")
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
    res = client("y2023_12345_exam").get("/marks/hpotter")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_can_get_user_marks_and_marks_history_for_question(client, mark_factory):
    mark_factory(
        exam_id="y2023_12345_exam", question=1, username="hpotter", with_history=5
    )

    res = client("y2023_12345_exam").get("/marks/hpotter")
    assert res.status_code == 200

    [mark_] = res.json()
    assert len(mark_["history"]) == 5


def test_can_get_correct_history_mark(client, mark_factory):
    mark = mark_factory(
        exam_id="y2023_12345_exam", question=1, username="hpotter", with_history=1
    )

    [history] = mark.history

    res = client("y2023_12345_exam").get("/marks/hpotter")
    assert res.status_code == 200

    [history_] = res.json()[0]["history"]

    assert history_["mark"] == history.mark
    assert history_["feedback"] == history.feedback
    assert history_["marker"] == history.marker
