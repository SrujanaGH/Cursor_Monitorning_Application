"""Session auth helpers."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar

from flask import current_app, redirect, session, url_for

F = TypeVar("F", bound=Callable[..., Any])


def login_user(user_id: int, username: str) -> None:
    session.clear()
    session["user_id"] = user_id
    session["username"] = username
    session.permanent = True


def logout_user() -> None:
    session.clear()


def current_username() -> str | None:
    return session.get("username")


def is_authenticated() -> bool:
    return session.get("user_id") is not None


def login_required(view: F) -> F:
    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any):
        if not is_authenticated():
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped  # type: ignore[return-value]


def seed_admin_user() -> None:
    """Create the demo admin account once if missing. Never logs plaintext passwords."""
    from app.db import db
    from app.models import User

    username = current_app.config["ADMIN_USERNAME"]
    password = current_app.config["ADMIN_PASSWORD"]

    existing = User.query.filter_by(username=username).first()
    if existing is not None:
        return

    admin = User(username=username)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
