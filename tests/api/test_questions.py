from api.schemas.exam import TaskType


def test_can_get_question_for_exam(client_):
    res = client_.get("/simple/questions/1")
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
    assert len(tasks) == 2
    [task1, task2] = tasks
    assert task1["type"] == TaskType.ESSAY
    assert task1["lines"] == 5
    assert task2["instructions"] == "Some instructions for this task."
    assert task2["type"] == TaskType.MULTIPLE_CHOICE_SELECT_ONE
    assert task2["choices"] == [
        {"value": "a", "label": "Red pill"},
        {"value": "b", "label": "Blue pill"},
    ]


def test_404_in_case_of_missing_question(client_):
    res = client_.get("/simple/questions/2")
    assert res.status_code == 404
    assert res.json()["detail"] == "Question not found"
