from api.models.assessment import AuthenticationMode
from api.router.authentication import pwd_context


def test_logging_in_to_non_existing_exam_gives_404(client):
    res = client("not_exists").post(
        "/not_exists/auth/login", json=dict(username="hpotter", password="password")
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Assessment not found."


def test_cannot_login_to_assessment_if_not_candidate_or_marker(
    client, assessment_factory
):
    assessment_factory(exam_code="y2023_12345_exam")
    res = client("y2023_12345_exam").post(
        "/y2023_12345_exam/auth/login",
        json=dict(username="hpotter", password="password"),
    )
    assert res.status_code == 401
    assert res.json()["detail"] == "Username not registered for assessment."


def test_login_fails_for_missing_credentials(client, assessment_factory):
    assessment_factory(
        exam_code="y2023_12345_exam",
        authentication_mode=AuthenticationMode.INTERNAL,
        with_students=[dict(username="hpotter")],
    )
    res = client("y2023_12345_exam").post(
        "/y2023_12345_exam/auth/login",
        json=dict(username="hpotter", password="password"),
    )

    assert res.status_code == 401
    assert res.json()["detail"] == "User credentials not found for the given username."


def test_login_fails_for_invalid_credentials(client, assessment_factory):
    assessment_factory(
        exam_code="y2023_12345_exam",
        authentication_mode=AuthenticationMode.INTERNAL,
        with_students=[dict(username="hpotter")],
        with_credentials=[
            dict(
                username="hpotter", hashed_password=pwd_context.hash("another password")
            )
        ],
    )
    res = client("y2023_12345_exam").post(
        "/y2023_12345_exam/auth/login",
        json=dict(username="hpotter", password="password"),
    )

    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid credentials."


def test_authentication_with_valid_credentials_returns_token(
    client, assessment_factory
):
    pwd = "password"
    assessment_factory(
        exam_code="y2023_12345_exam",
        authentication_mode=AuthenticationMode.INTERNAL,
        with_students=[dict(username="hpotter")],
        with_credentials=[
            dict(username="hpotter", hashed_password=pwd_context.hash(pwd))
        ],
    )
    res = client("y2023_12345_exam").post(
        "/y2023_12345_exam/auth/login",
        json=dict(username="hpotter", password=pwd),
    )

    assert res.status_code == 200
    assert "access_token" in res.json()
    assert len(res.json()["access_token"]) > 0
    assert res.json()["token_type"] == "bearer"
