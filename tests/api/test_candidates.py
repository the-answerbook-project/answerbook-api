def test_candidate_cannot_get_summary_for_non_existing_spec(client_):
    res = client_.get("/non-existing/candidates/me/heading")
    assert res.status_code == 404
    assert res.json()["detail"] == "Assessment not found."


def test_candidate_with_extension_gets_summary_with_adjusted_duration(
    client_with_token,
):
    clt = client_with_token(username="hpotter", assessment_code="simple")
    res = clt.get("/simple/candidates/me/heading")
    assert res.status_code == 200
    assert res.json()["duration"] == 140


def test_candidate_without_extension_gets_summary_with_standard_duration(
    client_with_token,
):
    clt = client_with_token(username="rweasley", assessment_code="simple")
    res = clt.get("/simple/candidates/me/heading")
    assert res.status_code == 200
    assert res.json()["duration"] == 120


def test_candidate_can_get_own_answers(client_with_token, assessment_factory):
    assessment_factory(
        code="simple",
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
    clt = client_with_token(username="hpotter", assessment_code="simple")
    res = clt.get("/simple/candidates/me/answers")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_candidate_answers_have_expected_fields(client_with_token, assessment_factory):
    assessment_factory(
        code="simple",
        with_students=[
            dict(username="hpotter", with_answers=[dict(question=1, part=1, section=1)])
        ],
    )
    clt = client_with_token(username="hpotter", assessment_code="simple")
    res = clt.get("/simple/candidates/me/answers")
    assert res.status_code == 200
    [answer] = res.json()
    assert "question" in answer
    assert "part" in answer
    assert "section" in answer
    assert "task" in answer
    assert "answer" in answer
