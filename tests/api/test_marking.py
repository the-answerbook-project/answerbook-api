# ----------------- tests for /{student_username}/marks


def test_can_get_student_marks_for_question(client, mark_factory):
    mark_factory.create_batch(
        size=3, exam_id="y2023_12345_exam", question=1, username="hpotter"
    )

    res = client("y2023_12345_exam").get("/hpotter/marks")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_response_mark_has_expected_fields(client, mark_factory):
    mark = mark_factory(exam_id="y2023_12345_exam", username="hpotter")

    res = client("y2023_12345_exam").get(f"/hpotter/marks")
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


def test_student_marks_include_mark_history(client, mark_factory):
    mark_factory(
        exam_id="y2023_12345_exam", question=1, username="hpotter", with_history=5
    )

    res = client("y2023_12345_exam").get("/hpotter/marks")
    assert res.status_code == 200

    [mark_] = res.json()
    assert len(mark_["history"]) == 5


def test_mark_history_has_expected_fields(client, mark_factory):
    mark = mark_factory(
        exam_id="y2023_12345_exam", question=1, username="hpotter", with_history=1
    )

    [history] = mark.history

    res = client("y2023_12345_exam").get("/hpotter/marks")
    assert res.status_code == 200

    [history_] = res.json()[0]["history"]

    assert history_["mark"] == history.mark
    assert history_["feedback"] == history.feedback
    assert history_["marker"] == history.marker


# ----------------- tests for /{student_username}/answers


def test_can_get_all_student_answers_for_exam(client, answer_factory):
    answer_factory.create_batch(
        size=5, exam_id="y2023_12345_exam", question=1, username="hpotter"
    )

    res = client("y2023_12345_exam").get("/hpotter/answers")
    assert res.status_code == 200
    assert len(res.json()) == 5


def test_gets_empty_list_response_if_no_answers_exist_for_assessment(client):
    res = client("y2023_12345_exam").get("/hpotter/answers")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_response_answer_has_expected_fields(client, answer_factory):
    answer = answer_factory(exam_id="y2023_12345_exam", username="hpotter")

    res = client("y2023_12345_exam").get(f"/hpotter/answers")
    assert res.status_code == 200
    [answer_] = res.json()
    assert answer_["question"] == answer.question
    assert answer_["part"] == answer.part
    assert answer_["section"] == answer.section
    assert answer_["task"] == answer.task
    assert answer_["answer"] == answer.answer
