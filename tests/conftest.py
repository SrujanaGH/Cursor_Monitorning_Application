"""Shared pytest fixtures with isolated temp DB (no real secrets)."""

from __future__ import annotations

import pytest

from app import create_app
from app.config import Config
from app.db import db
from app.models import User


@pytest.fixture()
def app(tmp_path):
    db_path = tmp_path / "test.db"
    application = create_app(
        Config(
            secret_key="test-secret-key-not-for-production",
            demo_mode=True,
            debug=False,
            admin_username="admin",
            admin_password="admin123",
            database_uri=f"sqlite:///{db_path}",
            testing=True,
            wtf_csrf_enabled=False,
        )
    )
    yield application

    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_client(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    return client


def get_admin(app) -> User:
    with app.app_context():
        return User.query.filter_by(username="admin").one()
