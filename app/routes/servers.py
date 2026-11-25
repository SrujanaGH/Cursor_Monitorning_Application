"""Authenticated server registry CRUD."""

from __future__ import annotations

from flask import Blueprint, flash, redirect, url_for

from app.auth_utils import login_required
from app.db import db
from app.forms import DeleteServerForm, ServerForm
from app.models import Server
from app.validators import validate_hostname_or_ip, validate_notes, validate_server_name

servers_bp = Blueprint("servers", __name__)


@servers_bp.post("/servers")
@login_required
def create_server():
    form = ServerForm()
    if not form.validate_on_submit():
        flash("Could not add server. Check the form and try again.", "error")
        return redirect(url_for("main.dashboard"))

    name = (form.name.data or "").strip()
    host = (form.hostname_or_ip.data or "").strip()
    notes = (form.notes.data or "").strip() or None

    for message in (
        validate_server_name(name),
        validate_hostname_or_ip(host),
        validate_notes(notes),
    ):
        if message:
            flash(message, "error")
            return redirect(url_for("main.dashboard"))

    server = Server(name=name, hostname_or_ip=host, notes=notes)
    db.session.add(server)
    db.session.commit()
    flash(f"Added server “{name}”.", "success")
    return redirect(url_for("main.dashboard"))


@servers_bp.post("/servers/<int:server_id>/delete")
@login_required
def delete_server(server_id: int):
    form = DeleteServerForm()
    if not form.validate_on_submit():
        flash("Could not verify delete request.", "error")
        return redirect(url_for("main.dashboard"))

    server = db.get_or_404(Server, server_id)
    name = server.name
    db.session.delete(server)
    db.session.commit()
    flash(f"Removed server “{name}”.", "success")
    return redirect(url_for("main.dashboard"))
