"""Jinja2 global functions available in all templates."""

from datetime import UTC, datetime
from typing import Any, NoReturn


def utc() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(UTC)


def raise_(msg: str) -> NoReturn:
    """Raise a RuntimeError from within a Jinja2 template."""
    raise RuntimeError(msg)


MM_JINJA_GLOBALS: dict[str, Any] = {
    "raise": raise_,
    "utc": utc,
}
