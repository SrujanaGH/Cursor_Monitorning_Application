"""Public shell routes for Phase 0."""

from __future__ import annotations

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home() -> str:
    """Home / dashboard placeholder shell."""
    return render_template("home.html")
