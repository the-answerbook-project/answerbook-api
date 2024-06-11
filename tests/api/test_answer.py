def test_can_get_user_answers_for_question(client, answer_factory):
    answer_factory.create_batch(
        size=3, exam_id="y2023_12345_exam", question=1, username="hpotter"
    )

    res = client("y2023_12345_exam").get("/questions/1/answer")
    assert res.status_code == 200
    assert len(res.json()) == 3

    assert all(answer["question"] == 1 for answer in res.json())


def test_gets_empty_list_response_if_no_answers_exist_for_assessment(client):
    res = client("y2023_12345_exam").get("/questions/1/answer")
    assert res.status_code == 200
    assert len(res.json()) == 0
