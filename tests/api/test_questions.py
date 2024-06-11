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


def test_404_in_case_of_missing_question(client):
    res = client("simple").get("/questions/2")
    assert res.status_code == 404
    assert res.json()["detail"] == "Question not found"


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
