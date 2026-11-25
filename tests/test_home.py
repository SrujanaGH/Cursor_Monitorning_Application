"""Dashboard shell smoke tests."""

from __future__ import annotations


def test_home_redirects_to_login_when_anonymous(client) -> None:
    response = client.get("/")
    assert response.status_code in {302, 303}
    assert "/login" in (response.headers.get("Location") or "")


def test_dashboard_renders_for_authenticated_user(auth_client) -> None:
    response = auth_client.get("/")
    assert response.status_code == 200
    assert b"Monitoring" in response.data
    assert b"read-only demo" in response.data
    assert b"No servers yet" in response.data or b"Registered servers" in response.data
