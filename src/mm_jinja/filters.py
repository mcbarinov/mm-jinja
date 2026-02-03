"""Jinja2 filter functions for common template formatting operations."""

import json
from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal

from markupsafe import Markup


def timestamp(value: datetime | int | None, format_: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a datetime or unix timestamp to a string.

    Args:
        value: A datetime object, unix timestamp (int), or None.
        format_: strftime format string.

    Returns:
        Formatted date string, or empty string if value is None.

    """
    if isinstance(value, datetime):
        return value.strftime(format_)
    if isinstance(value, int):
        # Naive datetime intentional - this is for simple display formatting
        return datetime.fromtimestamp(value).strftime(format_)  # noqa: DTZ006
    return ""


def empty(value: object) -> object:
    """Return empty string for None or empty sequences, otherwise return value unchanged."""
    if value is None:
        return ""
    if isinstance(value, Sequence) and len(value) == 0:
        return ""
    return value


def yes_no(
    value: object, is_colored: bool = True, hide_no: bool = False, none_is_false: bool = False, on_off: bool = False
) -> Markup:
    """Format a boolean value as colored yes/no (or on/off) HTML span."""
    clr = "black"
    if none_is_false and value is None:
        value = False

    if value is True:
        value = "on" if on_off else "yes"
        clr = "green"
    elif value is False:
        value = "" if hide_no else "off" if on_off else "no"
        clr = "red"
    elif value is None:
        value = ""
    if not is_colored:
        clr = "black"
    # HTML constructed from controlled internal values, not user input
    return Markup(f"<span style='color: {clr};'>{value}</span>")  # nosec  # noqa: S704


def nformat(
    value: str | float | Decimal | None,
    prefix: str = "",
    suffix: str = "",
    separator: str = "",
    hide_zero: bool = False,
    digits: int = 2,
) -> str:
    """Format a number with optional prefix, suffix, and thousand separators.

    Args:
        value: Number to format. Accepts str, float, Decimal, or None.
        prefix: String prepended to result.
        suffix: String appended to result.
        separator: Thousand separator (only applied when value > 1000).
        hide_zero: Return empty string if value is zero.
        digits: Decimal places (only applied when value <= 1000).

    Returns:
        Formatted string, or empty string if value is None/empty.

    Note:
        For values > 1000, decimals are truncated and separator is applied.
        For values <= 1000, decimal rounding is applied without separator.

    """
    if value is None or value == "":
        return ""

    num = float(value)

    if num == 0:
        if hide_zero:
            return ""
        return f"{prefix}0{suffix}"

    if num > 1000:
        formatted = "".join(
            reversed([x + (separator if i and not i % 3 else "") for i, x in enumerate(reversed(str(int(num))))]),
        )
    else:
        formatted = str(round(num, digits))

    return f"{prefix}{formatted}{suffix}"


def to_json(data: dict[str, object]) -> str:
    """Encode a dictionary as JSON string."""
    return json.dumps(data)


MM_JINJA_FILTERS = {
    "timestamp": timestamp,
    "dt": timestamp,
    "empty": empty,
    "yes_no": yes_no,
    "nformat": nformat,
    "n": nformat,
    "to_json": to_json,
}
