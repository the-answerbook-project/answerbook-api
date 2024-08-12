def test_candidate_cannot_get_summary_for_non_existing_spec(client_):
    res = client_.get("/non-existing/candidates/me/exam-summary")
    assert res.status_code == 404
    assert res.json()["detail"] == "Assessment not found."


def test_candidate_with_extension_gets_summary_with_adjusted_duration(
    client_with_token,
):
    clt = client_with_token(username="hpotter", assessment_code="simple")
    res = clt.get("/simple/candidates/me/exam-summary")
    assert res.status_code == 200
    assert res.json()["duration"] == 140


def test_candidate_without_extension_gets_summary_with_standard_duration(
    client_with_token,
):
    clt = client_with_token(username="rweasley", assessment_code="simple")
    res = clt.get("/simple/candidates/me/exam-summary")
    assert res.status_code == 200
    assert res.json()["duration"] == 120
