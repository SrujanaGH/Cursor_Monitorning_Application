"""Server registry tests."""

from __future__ import annotations

from app.db import db
from app.models import Server


def test_create_list_delete_server(auth_client, app) -> None:
    create = auth_client.post(
        "/servers",
        data={
            "name": "web-01",
            "hostname_or_ip": "10.0.0.21",
            "notes": "lab box",
        },
        follow_redirects=True,
    )
    assert create.status_code == 200
    assert b"web-01" in create.data
    assert b"10.0.0.21" in create.data

    with app.app_context():
        server = Server.query.filter_by(name="web-01").one()
        server_id = server.id

    deleted = auth_client.post(
        f"/servers/{server_id}/delete",
        follow_redirects=True,
    )
    assert deleted.status_code == 200
    assert b"Removed server" in deleted.data

    with app.app_context():
        assert Server.query.filter_by(id=server_id).first() is None


def test_unauthenticated_cannot_create(client, app) -> None:
    response = client.post(
        "/servers",
        data={"name": "evil", "hostname_or_ip": "10.0.0.9"},
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    assert "/login" in (response.headers.get("Location") or "")
    with app.app_context():
        assert Server.query.count() == 0


def test_unauthenticated_cannot_delete(client, app) -> None:
    with app.app_context():
        server = Server(name="keep-me", hostname_or_ip="192.168.1.10")
        db.session.add(server)
        db.session.commit()
        server_id = server.id

    response = client.post(f"/servers/{server_id}/delete", follow_redirects=False)
    assert response.status_code in {302, 303}
    assert "/login" in (response.headers.get("Location") or "")
    with app.app_context():
        assert db.session.get(Server, server_id) is not None


def test_rejects_invalid_hostname(auth_client, app) -> None:
    response = auth_client.post(
        "/servers",
        data={"name": "bad", "hostname_or_ip": "not a host; rm -rf"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"invalid" in response.data.lower() or b"Hostname or IP" in response.data
    with app.app_context():
        assert Server.query.filter_by(name="bad").first() is None
