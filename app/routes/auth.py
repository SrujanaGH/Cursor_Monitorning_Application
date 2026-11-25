"""Login / logout routes."""

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, url_for

from app.auth_utils import is_authenticated, login_user, logout_user
from app.forms import LoginForm, LogoutForm
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if is_authenticated():
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        username = (form.username.data or "").strip()
        password = form.password.data or ""
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash("Invalid credentials.", "error")
            return render_template("login.html", form=form), 401

        login_user(user.id, user.username)
        return redirect(url_for("main.dashboard"))

    return render_template("login.html", form=form)


@auth_bp.post("/logout")
def logout():
    form = LogoutForm()
    if not form.validate_on_submit():
        flash("Could not verify logout request.", "error")
        return redirect(url_for("main.dashboard"))

    logout_user()
    flash("Signed out.", "info")
    return redirect(url_for("auth.login"))
