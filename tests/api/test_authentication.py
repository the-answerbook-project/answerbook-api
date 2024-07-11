def test_can_login_to_assessment(client):
    res = client("y2023_12345_exam").post(
        "/y2023_12345_exam/auth/login", json=dict(username="xxx", password="password")
    )
    assert res.status_code == 200


def test_can_logout_from_assessment(client):
    res = client("y2023_12345_exam").delete("/y2023_12345_exam/auth/logout")
    assert res.status_code == 200
