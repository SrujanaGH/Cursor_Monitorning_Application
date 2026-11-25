"""Dashboard and server detail (read-only monitoring views)."""

from __future__ import annotations

from flask import Blueprint, current_app, render_template

from app.auth_utils import current_username, login_required
from app.db import db
from app.forms import DeleteServerForm, LogoutForm, ServerForm
from app.metrics import generate_metrics
from app.models import Server

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
@login_required
def dashboard():
    servers = Server.query.order_by(Server.name.asc()).all()
    cpu_warn = current_app.config["CPU_WARNING_THRESHOLD"]
    mem_warn = current_app.config["MEMORY_WARNING_THRESHOLD"]
    refresh = current_app.config["METRICS_REFRESH_SECONDS"]

    cards = []
    for server in servers:
        metrics = generate_metrics(
            server.id,
            cpu_warning=cpu_warn,
            memory_warning=mem_warn,
        )
        cards.append({"server": server, "metrics": metrics})

    return render_template(
        "dashboard.html",
        cards=cards,
        server_form=ServerForm(),
        delete_form=DeleteServerForm(),
        logout_form=LogoutForm(),
        username=current_username(),
        refresh_seconds=refresh,
    )


@main_bp.get("/servers/<int:server_id>")
@login_required
def server_detail(server_id: int):
    server = db.get_or_404(Server, server_id)
    metrics = generate_metrics(
        server.id,
        cpu_warning=current_app.config["CPU_WARNING_THRESHOLD"],
        memory_warning=current_app.config["MEMORY_WARNING_THRESHOLD"],
    )
    return render_template(
        "server_detail.html",
        server=server,
        metrics=metrics,
        logout_form=LogoutForm(),
        username=current_username(),
        refresh_seconds=current_app.config["METRICS_REFRESH_SECONDS"],
    )
