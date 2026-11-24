"""Application factory for the monitoring demo."""

from __future__ import annotations

import logging
import secrets
import warnings

from flask import Flask

from app.config import Config, load_config


def create_app(config: Config | None = None) -> Flask:
    """Create and configure the Flask application."""
    cfg = config or load_config()
    _configure_secret_key(cfg)

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_mapping(
        SECRET_KEY=cfg.secret_key,
        DEMO_MODE=cfg.demo_mode,
        DEBUG=cfg.debug,
    )

    from app.routes.main import main_bp

    app.register_blueprint(main_bp)

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
