"""Smoke tests for the Phase 0 UI shell."""

from __future__ import annotations

from app import create_app
from app.config import Config


def test_home_renders_monitoring_placeholder() -> None:
    app = create_app(
        Config(
            secret_key="test-secret-key",
            demo_mode=True,
            debug=False,
        )
    )
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Monitoring" in response.data
    assert b"read-only demo" in response.data
