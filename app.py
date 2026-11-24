"""Entry point: run the monitoring demo on 0.0.0.0:5777."""

from __future__ import annotations

from app import create_app
from app.config import load_config

config = load_config()
app = create_app(config)

if __name__ == "__main__":
    # Bound to all interfaces for the lab demo. Use only on trusted networks;
    # keep authentication enabled once Phase 1 lands.
    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug,
    )
