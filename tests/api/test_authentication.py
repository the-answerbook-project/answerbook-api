from datetime import timedelta
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlmodel import select

from api.authentication.internal_authentication import pwd_context
from api.authentication.ldap_authentication import LdapAuthenticator
from api.dependencies import get_ldap_authenticator
from api.models.assessment import AuthenticationMode
from api.models.revoked_token import RevokedToken
from api.router.authentication import calculate_token_expiration, create_access_token


def test_logging_in_to_assessment_with_no_configuration_gives_404(client_):
    res = client_.post(
        "/not_exists/auth/login", json=dict(username="hpotter", password="password")
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Assessment not found."


def test_logging_in_to_assessment_with_no_specification_gives_404(
    client_, assessment_factory
):
    assessment_factory(code="y1234_4321_exam")
    res = client_.post(
        "/y1234_4321_exam/auth/login",
        json=dict(username="hpotter", password="password"),
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Assessment not found."


def test_cannot_login_to_assessment_if_not_candidate_or_marker(
    client_, assessment_factory
):
    assessment_factory(code="y2023_12345_exam")
    res = client_.post(
        "/y2023_12345_exam/auth/login",
        json=dict(username="hpotter", password="password"),
    )
    assert res.status_code == 401
    assert res.json()["detail"] == "Username not registered for assessment."


def test_internal_authentication_login_fails_for_missing_credentials(
    client_, assessment_factory
):
    assessment_factory(
        code="y2023_12345_exam",
        authentication_mode=AuthenticationMode.INTERNAL,
        with_students=[dict(username="hpotter")],
    )
    res = client_.post(
        "/y2023_12345_exam/auth/login",
        json=dict(username="hpotter", password="password"),
    )

    assert res.status_code == 401
    assert res.json()["detail"] == "User credentials not found for the given username."


def test_internal_authentication_login_fails_for_invalid_credentials(
    client_, assessment_factory
):
    assessment_factory(
        code="y2023_12345_exam",
        authentication_mode=AuthenticationMode.INTERNAL,
        with_students=[dict(username="hpotter")],
        with_credentials=[
            dict(
                username="hpotter", hashed_password=pwd_context.hash("another password")
            )
        ],
    )
    res = client_.post(
        "/y2023_12345_exam/auth/login",
        json=dict(username="hpotter", password="password"),
    )

    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid credentials."


def test_internal_authentication_login_with_valid_credentials_returns_token(
    client_, assessment_factory
):
    pwd = "password"
    assessment_factory(
        code="y2023_12345_exam",
        authentication_mode=AuthenticationMode.INTERNAL,
        with_students=[dict(username="hpotter")],
        with_credentials=[
            dict(username="hpotter", hashed_password=pwd_context.hash(pwd))
        ],
    )
    res = client_.post(
        "/y2023_12345_exam/auth/login",
        json=dict(username="hpotter", password=pwd),
    )

    assert res.status_code == 200
    assert "access_token" in res.json()
    assert len(res.json()["access_token"]) > 0
    assert res.json()["token_type"] == "bearer"


def test_ldap_authentication_login_with_valid_credentials_returns_token(
    app, assessment_factory
):
    assessment_factory(
        code="y2023_12345_exam",
        authentication_mode=AuthenticationMode.LDAP,
        with_students=[dict(username="hpotter")],
    )

    authenticator = LdapAuthenticator("", "")
    mock_ldap_authentication = Mock(return_value=True)
    setattr(authenticator, "authenticate", mock_ldap_authentication)
    app.dependency_overrides[get_ldap_authenticator] = lambda: authenticator

    res = TestClient(app).post(
        "/y2023_12345_exam/auth/login",
        json=dict(username="hpotter", password="password"),
    )
    assert res.status_code == 200
    mock_ldap_authentication.assert_called_once_with("hpotter", "password")
    assert "access_token" in res.json()
    assert len(res.json()["access_token"]) > 0
    assert res.json()["token_type"] == "bearer"


def test_logout_revokes_token(client_, session, assessment_factory):
    assessment = assessment_factory()
    token = create_access_token(subject={}, expires_delta=timedelta(hours=1))
    response = client_.delete(
        f"/{assessment.code}/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204
    query = select(RevokedToken).where(RevokedToken.token == token)
    revoked_token = session.exec(query).first()
    assert revoked_token is not None


@pytest.mark.parametrize(
    "duration, extensions, expected_minutes",
    [
        (120, {}, 240),
        (120, {"hpotter": "32 minutes"}, 272),
        (120, {"hpotter": "32 minutes", "rweasley": "40"}, 280),
    ],
)
def test_calculation_of_token_expiration(duration, extensions, expected_minutes):
    assert calculate_token_expiration(duration, extensions) == timedelta(
        minutes=expected_minutes
    )
