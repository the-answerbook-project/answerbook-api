from api.schemas.exam import TaskType


def test_can_get_question_for_exam(client):
    res = client("simple").get("/questions/1")
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



def test_can_get_answer_for_question_by_user(web_client):
    res = web_client.get("/questions/1/answer")
    assert res.status_code == 200
    # q = res.json()
    # assert q["title"] == "Title of the question"
    # assert q["instructions"] == "Some instructions for this question."
    # assert len(q["parts"]) == 1
    # assert q["parts"]["1"]["instructions"] == "Some instructions for this part."
    # sections = q["parts"]["1"]["sections"]
    # assert len(sections) == 1
    # assert sections["1"]["instructions"] == "Some instructions for this section."
    # assert sections["1"]["maximum_mark"] == 10
    # tasks = sections["1"]["tasks"]
    # assert len(tasks) == 2
    # [task1, task2] = tasks
    # assert task1["type"] == TaskType.ESSAY
    # assert task1["lines"] == 5
    # assert task2["instructions"] == "Some instructions for this task."
    # assert task2["type"] == TaskType.MULTIPLE_CHOICE_SELECT_ONE
    # assert task2["choices"] == [
    #     {"value": "a", "label": "Red pill"},
    #     {"value": "b", "label": "Blue pill"},
    # ]





def test_404_in_case_of_missing_question(client):
    res = client("simple").get("/questions/2")
    assert res.status_code == 404
    assert res.json()["detail"] == "Question not found"


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
