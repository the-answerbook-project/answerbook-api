from datetime import datetime, timezone

import pytest
from freezegun import freeze_time

from api.models.assessment import UserRole

assessment_code = "simple"


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
