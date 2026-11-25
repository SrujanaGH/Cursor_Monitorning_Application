"""WTF forms with CSRF (via Flask-WTF)."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=256)])
    submit = SubmitField("Sign in")


class ServerForm(FlaskForm):
    name = StringField("Display name", validators=[DataRequired(), Length(max=120)])
    hostname_or_ip = StringField(
        "Hostname or IP",
        validators=[DataRequired(), Length(max=255)],
    )
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=2000)])
    submit = SubmitField("Add server")


class DeleteServerForm(FlaskForm):
    submit = SubmitField("Remove")


class LogoutForm(FlaskForm):
    submit = SubmitField("Sign out")
