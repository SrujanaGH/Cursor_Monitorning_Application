"""Application factory for the monitoring demo."""

from __future__ import annotations

import logging
import secrets
import warnings

from flask import Flask
from flask_wtf import CSRFProtect

from app.config import Config, load_config
from app.db import db

csrf = CSRFProtect()


def create_app(config: Config | None = None) -> Flask:
    """Create and configure the Flask application."""
    cfg = config or load_config()
    _configure_secret_key(cfg)

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        instance_relative_config=True,
    )
    app.config.from_mapping(
        SECRET_KEY=cfg.secret_key,
        DEMO_MODE=cfg.demo_mode,
        DEBUG=cfg.debug,
        TESTING=cfg.testing,
        SQLALCHEMY_DATABASE_URI=cfg.database_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        ADMIN_USERNAME=cfg.admin_username,
        ADMIN_PASSWORD=cfg.admin_password,
        METRICS_REFRESH_SECONDS=cfg.metrics_refresh_seconds,
        CPU_WARNING_THRESHOLD=cfg.cpu_warning_threshold,
        MEMORY_WARNING_THRESHOLD=cfg.memory_warning_threshold,
        WTF_CSRF_ENABLED=cfg.wtf_csrf_enabled and not cfg.testing,
        WTF_CSRF_TIME_LIMIT=None,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    db.init_app(app)
    csrf.init_app(app)

    from app.routes.api import api_bp
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.servers import servers_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(servers_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        # Import submodule without rebinding local name `app` (import app.X would).
        from app import models as _models  # noqa: F401

        db.create_all()
        from app.auth_utils import seed_admin_user

        seed_admin_user()

    @app.context_processor
    def inject_globals():
        from app.auth_utils import current_username, is_authenticated
        from app.forms import LogoutForm

        return {
            "is_authenticated": is_authenticated(),
            "current_username": current_username(),
            "logout_form": LogoutForm(),
        }

    @app.errorhandler(404)
    def not_found(_error):
        from flask import render_template

        return render_template("error.html", code=404, message="Page not found."), 404

    @app.errorhandler(500)
    def server_error(_error):
        from flask import render_template

        if app.debug:
            raise
        return (
            render_template(
                "error.html",
                code=500,
                message="Something went wrong. Try again or restart the demo app.",
            ),
            500,
        )

    return app


def _configure_secret_key(cfg: Config) -> None:
    """Resolve SECRET_KEY: env value, ephemeral demo fallback, or hard fail."""
    if cfg.secret_key:
        return

    if cfg.demo_mode:
        cfg.secret_key = secrets.token_hex(32)
        message = (
            "SECRET_KEY is not set; generated an ephemeral key for local demo. "
            "Sessions will reset on restart. Set SECRET_KEY in .env for stable sessions."
        )
        warnings.warn(message, UserWarning, stacklevel=2)
        logging.getLogger(__name__).warning(message)
        return

    raise RuntimeError(
        "SECRET_KEY is required when DEMO_MODE is disabled. "
        "Set SECRET_KEY in the environment or .env file."
    )
