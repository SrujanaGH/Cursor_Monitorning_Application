"""Mock metrics shape, thresholds, and API auth tests."""

from __future__ import annotations

from app.db import db
from app.metrics import generate_metrics
from app.models import Server


def test_metrics_shape_and_keys() -> None:
    metrics = generate_metrics(1, now=1_700_000_000.0)
    assert metrics["source"] == "mock"
    assert "cpu_percent" in metrics
    assert "memory" in metrics
    assert {"used_gb", "total_gb", "percent"} <= set(metrics["memory"])
    assert {"in_mbps", "out_mbps"} <= set(metrics["network"])
    assert isinstance(metrics["open_ports"], list)
    assert metrics["status"] in {"OK", "Warning"}
    assert "password" not in metrics
    assert "secret" not in metrics
    assert "ADMIN" not in str(metrics)


def test_threshold_status_mapping() -> None:
    ok = generate_metrics(2, now=100.0, cpu_warning=99.9, memory_warning=99.9)
    # Force warning by lowering thresholds below any realistic mock value.
    warn = generate_metrics(2, now=100.0, cpu_warning=1.0, memory_warning=1.0)
    assert ok["status"] in {"OK", "Warning"}
    assert warn["status"] == "Warning"


def test_metrics_api_requires_auth(client) -> None:
    response = client.get("/api/metrics")
    assert response.status_code == 401
    assert response.get_json()["error"] == "authentication required"


def test_metrics_api_authenticated(auth_client, app) -> None:
    with app.app_context():
        db.session.add(Server(name="db-01", hostname_or_ip="db.lab.local"))
        db.session.commit()

    response = auth_client.get("/api/metrics")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["source"] == "mock"
    assert len(payload["items"]) == 1
    metrics = payload["items"][0]["metrics"]
    assert "cpu_percent" in metrics
    blob = str(payload).lower()
    assert "admin123" not in blob
    assert "secret_key" not in blob
