"""Environment-backed configuration for the monitoring demo."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    secret_key: str | None
    demo_mode: bool
    debug: bool
    host: str = "0.0.0.0"
    port: int = 5777


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_config() -> Config:
    """Load config from environment (.env supported for local demo)."""
    load_dotenv()

    secret_key = os.environ.get("SECRET_KEY")
    if secret_key is not None:
        secret_key = secret_key.strip() or None

    return Config(
        secret_key=secret_key,
        demo_mode=_as_bool(os.environ.get("DEMO_MODE"), default=True),
        debug=_as_bool(os.environ.get("FLASK_DEBUG"), default=False),
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5777")),
    )
