def test_logging_in_to_non_existing_exam_gives_404(client):
    res = client("not_exists").post(
        "/not_exists/auth/login", json=dict(username="hpotter", password="password")
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Assessment not found."


def test_cannot_login_to_assessment_if_not_candidate_or_marker(
    client, assessment_factory
):
    assessment_factory(
        exam_code="y2023_12345_exam",
    )

    res = client("y2023_12345_exam").post(
        "/y2023_12345_exam/auth/login",
        json=dict(username="hpotter", password="password"),
    )
    assert res.status_code == 401
    assert res.json()["detail"] == "Username not registered for assessment."


def test_authentication_with_valid_credentials_gives_tokens_in_cookies(
    client, assessment_factory
):
    assessment_factory(
        exam_code="y2023_12345_exam",
        with_students=[
            dict(
                username="hpotter",
            )
        ],
    )
    res = client("y2023_12345_exam").post(
        "/y2023_12345_exam/auth/login",
        json=dict(username="hpotter", password="password"),
    )

    assert res.status_code == 200
    assert len(res.cookies) == 1
    assert "access_token_cookie" in res.cookies.keys()
    assert res.json()["username"] == "hpotter"
    assert res.json()["role"] == "CANDIDATE"
