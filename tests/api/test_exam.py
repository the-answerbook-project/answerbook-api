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
    assert summary["begins"] == "2019-01-01T08:00:00Z"
