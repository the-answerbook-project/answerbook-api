###
# NOTE: QPS: Question Part Section
###
from api.factories.student import StudentFactory

username = "hpotter"
PREFIX = f"/answers/{username}"


def test_can_get_a_part_for_student(client, answer_factory):
    answer_factory(
        exam_id="y2023_12345_exam", question=1, part=1, section=1, username="hpotter"
    )
    res = client("y2023_12345_exam").get(f"{PREFIX}/question/1/part/1/section/1")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_can_get_user_answers_for_question(client, answer_factory):
    answer_factory.create_batch(
        size=3, exam_id="y2023_12345_exam", question=1, username="hpotter"
    )

    res = client("y2023_12345_exam").get(f"{PREFIX}/question/1")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_response_answer_has_expected_fields(client, answer_factory):
    answer = answer_factory(exam_id="y2023_12345_exam", username="hpotter")

    res = client("y2023_12345_exam").get(f"{PREFIX}/question/{answer.question}")
    assert res.status_code == 200
    [answer_] = res.json()
    assert answer_["question"] == answer.question
    assert answer_["part"] == answer.part
    assert answer_["section"] == answer.section
    assert answer_["task"] == answer.task
    assert answer_["answer"] == answer.answer


def test_gets_empty_list_response_if_no_answers_exist_for_assessment(client):
    res = client("y2023_12345_exam").get(f"{PREFIX}/question/1")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_can_upload_answers(client):
    res = client("y2023_12345_exam").post(
        f"{PREFIX}/question/1",
        json=[
            {
                "question": 1,
                "part": 1,
                "section": 1,
                "task": 1,
                "answer": "This is an answer",
            }
        ],
    )

    # Check DB
    res_ans = client("y2023_12345_exam").get(f"{PREFIX}/question/1")
    assert res_ans.status_code == 200
    [answer_] = res_ans.json()
    assert res_ans.status_code == 200
    assert answer_["answer"] == "This is an answer"


def test_can_upload_answers_for_multiple_users(client):
    res = client("y2023_12345_exam").post(
        "/answers/hgranger/question/1",
        json=[
            {
                "question": 1,
                "part": 1,
                "section": 1,
                "task": 1,
                "answer": "This is an answer by hgranger",
            }
        ],
    )

    assert res.status_code == 200

    res2 = client("y2023_12345_exam").post(
        "/answers/hpotter/question/1",
        json=[
            {
                "question": 1,
                "part": 1,
                "section": 1,
                "task": 1,
                "answer": "This is an answer by hpotter",
            }
        ],
    )

    assert res2.status_code == 200

    # Check DB
    res_ans = client("y2023_12345_exam").get("/answers/hgranger/question/1")
    assert res_ans.status_code == 200
    [answer_] = res_ans.json()
    assert res_ans.status_code == 200
    assert answer_["answer"] == "This is an answer by hgranger"
