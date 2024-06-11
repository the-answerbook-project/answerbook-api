def test_can_get_answer_for_question_by_user(web_client, answer_factory):
    answer = answer_factory.create_batch(
        size=3, exam_id="y2023_12345_exam", question=1, username="hpotter"
    )

    res = web_client.get("/questions/1/answer")
    assert res.status_code == 200
    assert len(res.json()) == 3

    assert all(answer["question"] == 1 for answer in res.json())


def test_can_get_empty_list_for_no_answers_to_known_exam(web_client):
    res = web_client.get("/questions/1/answer")
    assert res.status_code == 200
    assert len(res.json()) == 0
