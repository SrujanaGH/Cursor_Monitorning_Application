"""Auth flow and password hashing tests."""

from __future__ import annotations

from app.models import User


def test_admin_password_is_hashed(app) -> None:
    with app.app_context():
        admin = User.query.filter_by(username="admin").one()
        assert admin.password_hash
        assert admin.password_hash != "admin123"
        assert not admin.password_hash.startswith("admin123")
        assert admin.check_password("admin123")


def test_login_success(client) -> None:
    response = client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    assert "/login" not in (response.headers.get("Location") or "")


def test_login_failure(client) -> None:
    response = client.post(
        "/login",
        data={"username": "admin", "password": "wrong-password"},
        follow_redirects=True,
    )
    assert response.status_code == 401
    assert b"Invalid credentials" in response.data


def test_logout(auth_client) -> None:
    response = auth_client.post("/logout", follow_redirects=False)
    assert response.status_code in {302, 303}
    assert "/login" in (response.headers.get("Location") or "")


def test_protected_route_redirects_when_logged_out(client) -> None:
    response = client.get("/", follow_redirects=False)
    assert response.status_code in {302, 303}
    assert "/login" in (response.headers.get("Location") or "")
