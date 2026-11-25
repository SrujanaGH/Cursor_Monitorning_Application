"""Simulated metrics for registered Linux servers (no SSH / subprocess)."""

from __future__ import annotations

import hashlib
import math
import time
from typing import Any


def _seed_float(server_id: int, label: str, bucket: int) -> float:
    digest = hashlib.sha256(f"{server_id}:{label}:{bucket}".encode()).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


def generate_metrics(
    server_id: int,
    *,
    now: float | None = None,
    cpu_warning: float = 80.0,
    memory_warning: float = 80.0,
) -> dict[str, Any]:
    """Return mock CPU, memory, network, and ports that vary over time."""
    ts = now if now is not None else time.time()
    bucket = int(ts // 7)

    wave = math.sin((ts / 11.0) + server_id) * 0.5 + 0.5
    cpu = round(25 + _seed_float(server_id, "cpu", bucket) * 55 + wave * 20, 1)
    cpu = min(99.5, max(5.0, cpu))

    mem_total_gb = 8 + (server_id % 4) * 8
    mem_used_ratio = 0.35 + _seed_float(server_id, "mem", bucket) * 0.5 + wave * 0.1
    mem_used_ratio = min(0.97, max(0.15, mem_used_ratio))
    mem_used_gb = round(mem_total_gb * mem_used_ratio, 2)
    mem_percent = round(mem_used_ratio * 100, 1)

    net_in = round(5 + _seed_float(server_id, "net_in", bucket) * 80 + wave * 15, 2)
    net_out = round(3 + _seed_float(server_id, "net_out", bucket) * 60 + wave * 10, 2)

    base_ports = [22, 80, 443, 5432, 6379, 8080, 9100]
    count = 3 + int(_seed_float(server_id, "ports", bucket) * 4)
    open_ports = sorted(base_ports[:count])

    status = "OK"
    if cpu >= cpu_warning or mem_percent >= memory_warning:
        status = "Warning"

    return {
        "server_id": server_id,
        "status": status,
        "cpu_percent": cpu,
        "memory": {
            "used_gb": mem_used_gb,
            "total_gb": mem_total_gb,
            "percent": mem_percent,
        },
        "network": {
            "in_mbps": net_in,
            "out_mbps": net_out,
        },
        "open_ports": open_ports,
        "generated_at": int(ts),
        "source": "mock",
    }


def status_for_metrics(metrics: dict[str, Any]) -> str:
    return str(metrics.get("status", "OK"))
