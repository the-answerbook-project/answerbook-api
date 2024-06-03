def test_can_get_question_for_exam(client):
    res = client("simple.yaml").get("/questions/1")
    assert res.status_code == 200
    q = res.json()
    assert q["title"] == "Title of the question"
    assert q["instructions"] == "Some instructions for this question."
    assert len(q["parts"]) == 1
    assert q["parts"]["1"]["instructions"] == "Some instructions for this part."
    sections = q["parts"]["1"]["sections"]
    assert len(sections) == 1
    assert sections["1"]["instructions"] == "Some instructions for this section."
    assert sections["1"]["maximum_mark"] == 10
    tasks = sections["1"]["tasks"]
    assert len(tasks) == 1
    assert tasks[0]["task"] == "Some instructions for this task."
    assert tasks[0]["type"] == "essay with 5 lines"


def test_404_in_case_of_missing_question(client):
    res = client("simple.yaml").get("/questions/2")
    assert res.status_code == 404
    assert res.json()["detail"] == "Question not found"
