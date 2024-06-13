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
