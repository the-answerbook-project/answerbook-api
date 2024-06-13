def test_can_get_all_student_answers_for_exam(client, answer_factory):
    answer_factory.create_batch(
        size=5, exam_id="y2023_12345_exam", question=1, username="hpotter"
    )

    res = client("y2023_12345_exam").get("/answers/hpotter")
    assert res.status_code == 200
    assert len(res.json()) == 5
