from datetime import datetime, timezone

import pytest
from freezegun import freeze_time
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from api.models.answer import AnswerHistory
from api.models.assessment import UserRole

assessment_code = "simple"
valid_answer = {
    "question": 1,
    "part": 1,
    "section": 1,
    "task": 1,
    "answer": "some answer",
}


@pytest.fixture(name="candidate_client")
def candidate_client_fixture(client_with_token):
    return client_with_token(
        role=UserRole.CANDIDATE, username="hpotter", assessment_code=assessment_code
    )


def test_candidate_cannot_get_heading_for_non_existing_spec(client_):
    res = client_.get("/non-existing/candidates/me/heading")
    assert res.status_code == 404
    assert res.json()["detail"] == "Assessment not found."


def test_candidate_with_delayed_start_gets_heading_with_adjusted_begins(
    candidate_client,
):
    res = candidate_client.get("/simple/candidates/me/heading")
    expected_beginning = datetime(2019, 1, 1, 8, 5, tzinfo=timezone.utc)
    assert res.status_code == 200
    assert res.json()["begins"] == expected_beginning.strftime("%Y-%m-%dT%H:%M:%S%:z")


def test_candidate_with_extension_gets_heading_with_adjusted_duration(
    candidate_client,
):
    res = candidate_client.get("/simple/candidates/me/heading")
    assert res.status_code == 200
    assert res.json()["duration"] == 140


def test_candidate_without_extension_gets_heading_with_standard_duration(
    client_with_token,
):
    clt = client_with_token(
        role=UserRole.CANDIDATE, username="rweasley", assessment_code=assessment_code
    )
    res = clt.get("/simple/candidates/me/heading")
    assert res.status_code == 200
    assert res.json()["duration"] == 120


def test_candidate_can_get_own_answers(candidate_client, assessment_factory):
    assessment_factory(
        code=assessment_code,
        with_students=[
            dict(
                username="hpotter",
                with_answers=[
                    dict(question=1, part=1, section=1),
                    dict(question=1, part=2, section=1),
                ],
            ),
            dict(
                username="rweasley",
                with_answers=[dict(question=1, part=1, section=1)],
            ),
        ],
    )

    res = candidate_client.get("/simple/candidates/me/answers")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_candidate_answers_have_expected_fields(candidate_client, assessment_factory):
    assessment_factory(
        code=assessment_code,
        with_students=[
            dict(username="hpotter", with_answers=[dict(question=1, part=1, section=1)])
        ],
    )

    res = candidate_client.get("/simple/candidates/me/answers")
    assert res.status_code == 200
    [answer] = res.json()
    assert "question" in answer
    assert "part" in answer
    assert "section" in answer
    assert "task" in answer
    assert "answer" in answer


def test_candidate_cannot_access_questions_before_start(candidate_client):
    with freeze_time(datetime(2019, 1, 1, 7, 59, tzinfo=timezone.utc)):
        res = candidate_client.get("/simple/candidates/me/questions")
    assert res.status_code == 403
    assert res.json()["detail"] == "The assessment has not started yet."


def test_questions_for_assessment_have_expected_fields(candidate_client):
    with freeze_time(datetime(2019, 1, 1, 8, 6, tzinfo=timezone.utc)):
        res = candidate_client.get("/simple/candidates/me/questions")
    assert res.status_code == 200
    questions = res.json()
    assert questions["1"]["title"] == "Title of the question"
    assert questions["1"]["instructions"] == "Some instructions for this question."
    assert questions["1"]["show_part_weights"] is False
    assert len(questions["1"]["parts"]) == 1


def test_posting_answers_gives_404_if_assessment_does_not_exist(candidate_client):
    res = candidate_client.post(
        "/not-existing/candidates/me/answers", json=valid_answer
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Assessment not found."


def test_candidate_cannot_post_answer_before_start(
    candidate_client, assessment_factory
):
    assessment = assessment_factory(code=assessment_code)
    with freeze_time(datetime(2019, 1, 1, 7, 59, tzinfo=timezone.utc)):
        res = candidate_client.post(
            f"/{assessment.code}/candidates/me/answers", json=valid_answer
        )
    assert res.status_code == 403
    assert res.json()["detail"] == "The assessment has not started yet."


def test_candidate_cannot_post_answer_after_end(candidate_client, assessment_factory):
    assessment = assessment_factory(code=assessment_code)
    with freeze_time(datetime(2019, 1, 1, 10, 26, tzinfo=timezone.utc)):
        res = candidate_client.post(
            f"/{assessment.code}/candidates/me/answers", json=valid_answer
        )
    assert res.status_code == 403
    assert res.json()["detail"] == "The assessment is over."


@pytest.mark.parametrize("seconds_past_deadline", [10, 15, 20, 25, 30])
def test_candidate_can_post_answers_within_grace_period(
    candidate_client, assessment_factory, seconds_past_deadline
):
    assessment = assessment_factory(
        code=assessment_code, with_students=[dict(username="hpotter")]
    )
    with freeze_time(
        datetime(2019, 1, 1, 10, 25, seconds_past_deadline, tzinfo=timezone.utc)
    ):
        res = candidate_client.post(
            f"/{assessment.code}/candidates/me/answers", json=valid_answer
        )
    assert res.status_code == 200


def test_new_answer_response_has_expected_fields(candidate_client, assessment_factory):
    assessment = assessment_factory(
        code=assessment_code, with_students=[dict(username="hpotter")]
    )
    with freeze_time(datetime(2019, 1, 1, 8, 30, tzinfo=timezone.utc)):
        res = candidate_client.post(
            f"/{assessment.code}/candidates/me/answers", json=valid_answer
        )
    assert res.status_code == 200
    answer = res.json()
    assert "id" in answer
    assert "username" in answer
    assert "question" in answer
    assert "part" in answer
    assert "section" in answer
    assert "task" in answer
    assert "answer" in answer
    assert "timestamp" in answer


def test_new_answer_adds_to_answer_history(
    candidate_client, assessment_factory, session
):
    assessment = assessment_factory(
        code=assessment_code,
        with_students=[
            dict(
                username="hpotter", with_answers=[dict(**valid_answer, with_history=1)]
            )
        ],
    )
    with freeze_time(datetime(2019, 1, 1, 8, 30, tzinfo=timezone.utc)):
        res = candidate_client.post(
            f"/{assessment.code}/candidates/me/answers", json=valid_answer
        )
    assert res.status_code == 200
    answer_id = res.json()["id"]
    query = select(func.count(AnswerHistory.id)).where(
        AnswerHistory.answer_id == answer_id
    )
    assert session.exec(query).one() == 2


def test_candidate_cannot_have_two_answers_for_same_question(assessment_factory):
    with pytest.raises(IntegrityError):
        assessment_factory(
            code=assessment_code,
            with_students=[
                dict(
                    username="hpotter",
                    with_answers=[dict(**valid_answer), dict(**valid_answer)],
                )
            ],
        )
