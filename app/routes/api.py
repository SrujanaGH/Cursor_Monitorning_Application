"""Authenticated JSON APIs for metrics polling."""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify

from app.auth_utils import is_authenticated
from app.db import db
from app.metrics import generate_metrics
from app.models import Server

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.before_request
def require_api_auth():
    if not is_authenticated():
        return jsonify({"error": "authentication required"}), 401
    return None


@api_bp.get("/metrics")
def metrics_list():
    cpu_warn = current_app.config["CPU_WARNING_THRESHOLD"]
    mem_warn = current_app.config["MEMORY_WARNING_THRESHOLD"]
    servers = Server.query.order_by(Server.id.asc()).all()
    payload = []
    for server in servers:
        metrics = generate_metrics(
            server.id,
            cpu_warning=cpu_warn,
            memory_warning=mem_warn,
        )
        payload.append({"server": server.to_dict(), "metrics": metrics})
    return jsonify({"items": payload, "source": "mock"})


@api_bp.get("/servers/<int:server_id>/metrics")
def metrics_one(server_id: int):
    server = db.get_or_404(Server, server_id)
    metrics = generate_metrics(
        server.id,
        cpu_warning=current_app.config["CPU_WARNING_THRESHOLD"],
        memory_warning=current_app.config["MEMORY_WARNING_THRESHOLD"],
    )
    return jsonify({"server": server.to_dict(), "metrics": metrics, "source": "mock"})
