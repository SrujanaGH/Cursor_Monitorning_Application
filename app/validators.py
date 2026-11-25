"""Input validation for server registry fields."""

from __future__ import annotations

import ipaddress
import re

_HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
)
_DANGEROUS_CHARS = re.compile(r"[;`|$&<>\\\n\r\0]")


def validate_server_name(name: str | None) -> str | None:
    if name is None:
        return "Name is required."
    cleaned = name.strip()
    if not cleaned:
        return "Name is required."
    if len(cleaned) > 120:
        return "Name must be 120 characters or fewer."
    if _DANGEROUS_CHARS.search(cleaned):
        return "Name contains invalid characters."
    return None


def validate_hostname_or_ip(value: str | None) -> str | None:
    if value is None:
        return "Hostname or IP is required."
    cleaned = value.strip()
    if not cleaned:
        return "Hostname or IP is required."
    if len(cleaned) > 255:
        return "Hostname or IP must be 255 characters or fewer."
    if _DANGEROUS_CHARS.search(cleaned) or " " in cleaned:
        return "Hostname or IP contains invalid characters."

    try:
        ipaddress.ip_address(cleaned)
        return None
    except ValueError:
        pass

    if cleaned.lower() in {"localhost"} or _HOSTNAME_RE.match(cleaned):
        return None

    return "Enter a valid hostname or IP address."


def validate_notes(notes: str | None) -> str | None:
    if notes is None or notes.strip() == "":
        return None
    if len(notes) > 2000:
        return "Notes must be 2000 characters or fewer."
    if _DANGEROUS_CHARS.search(notes):
        return "Notes contain invalid characters."
    return None
