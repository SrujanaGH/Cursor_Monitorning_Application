"""Environment-backed configuration for the monitoring demo."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_DB = _PROJECT_ROOT / "instance" / "monitorlab.db"


@dataclass
class Config:
    secret_key: str | None
    demo_mode: bool
    debug: bool
    admin_username: str = "admin"
    admin_password: str = "admin123"
    database_uri: str = field(default_factory=lambda: f"sqlite:///{_DEFAULT_DB}")
    host: str = "0.0.0.0"
    port: int = 5777
    metrics_refresh_seconds: int = 7
    cpu_warning_threshold: float = 80.0
    memory_warning_threshold: float = 80.0
    wtf_csrf_enabled: bool = True
    testing: bool = False


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

    db_path = os.environ.get("DATABASE_URL")
    if db_path:
        database_uri = db_path
    else:
        _DEFAULT_DB.parent.mkdir(parents=True, exist_ok=True)
        database_uri = f"sqlite:///{_DEFAULT_DB}"

    return Config(
        secret_key=secret_key,
        demo_mode=_as_bool(os.environ.get("DEMO_MODE"), default=True),
        debug=_as_bool(os.environ.get("FLASK_DEBUG"), default=False),
        admin_username=os.environ.get("ADMIN_USERNAME", "admin").strip() or "admin",
        admin_password=os.environ.get("ADMIN_PASSWORD", "admin123"),
        database_uri=database_uri,
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5777")),
        metrics_refresh_seconds=int(os.environ.get("METRICS_REFRESH_SECONDS", "7")),
        testing=_as_bool(os.environ.get("TESTING"), default=False),
    )
