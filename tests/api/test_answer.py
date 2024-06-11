def test_can_get_user_answers_for_question(client, answer_factory):
    answer_factory.create_batch(
        size=3, exam_id="y2023_12345_exam", question=1, username="hpotter"
    )

    res = client("y2023_12345_exam").get("/questions/1/answer")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_response_answer_has_expected_fields(client, answer_factory):
    answer = answer_factory(exam_id="y2023_12345_exam", username="hpotter")

    res = client("y2023_12345_exam").get(f"/questions/{answer.question}/answer")
    assert res.status_code == 200
    [answer_] = res.json()
    assert answer_["question"] == answer.question
    assert answer_["part"] == answer.part
    assert answer_["section"] == answer.section
    assert answer_["task"] == answer.task
    assert answer_["answer"] == answer.answer


def test_gets_empty_list_response_if_no_answers_exist_for_assessment(client):
    res = client("y2023_12345_exam").get("/questions/1/answer")
    assert res.status_code == 200
    assert len(res.json()) == 0
