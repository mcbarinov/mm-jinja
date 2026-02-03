"""Tests for mm_jinja.filters module."""

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from markupsafe import Markup

from mm_jinja.filters import empty, nformat, timestamp, to_json, yes_no


class TestEmptyFilter:
    """Tests for the empty filter function."""

    def test_empty(self) -> None:
        """Verify empty returns empty string for None and empty sequences."""
        assert empty(None) == ""
        assert empty("") == ""
        assert empty([]) == ""
        assert empty(0) == 0


class TestTimestampFilter:
    """Tests for the timestamp filter function."""

    def test_datetime_default_format(self) -> None:
        """Datetime with default format."""
        dt = datetime(2024, 1, 15, 10, 30, 45, tzinfo=UTC)
        assert timestamp(dt) == "2024-01-15 10:30:45"

    def test_datetime_custom_format(self) -> None:
        """Datetime with custom format."""
        dt = datetime(2024, 1, 15, 10, 30, 45, tzinfo=UTC)
        assert timestamp(dt, "%Y-%m-%d") == "2024-01-15"
        assert timestamp(dt, "%H:%M") == "10:30"

    def test_unix_timestamp(self) -> None:
        """Unix timestamp integer input."""
        result = timestamp(0, "%Y-%m-%d")
        assert "1970" in result

    def test_none_returns_empty(self) -> None:
        """None input returns empty string."""
        assert timestamp(None) == ""


class TestYesNoFilter:
    """Tests for the yes_no filter function."""

    def test_true_value(self) -> None:
        """True value returns green 'yes'."""
        result = yes_no(True)
        assert isinstance(result, Markup)
        assert "green" in result
        assert "yes" in result

    def test_false_value(self) -> None:
        """False value returns red 'no'."""
        result = yes_no(False)
        assert "red" in result
        assert "no" in result

    def test_none_value(self) -> None:
        """None value returns empty span."""
        result = yes_no(None)
        assert "black" in result
        assert "></span>" in result

    def test_hide_no(self) -> None:
        """hide_no=True returns empty text for False."""
        result = yes_no(False, hide_no=True)
        assert "red" in result
        assert "no" not in result

    def test_on_off_mode(self) -> None:
        """on_off=True uses 'on'/'off' instead of 'yes'/'no'."""
        assert "on" in yes_no(True, on_off=True)
        assert "off" in yes_no(False, on_off=True)

    def test_none_is_false(self) -> None:
        """none_is_false=True treats None as False."""
        result = yes_no(None, none_is_false=True)
        assert "red" in result
        assert "no" in result

    def test_not_colored(self) -> None:
        """is_colored=False uses black for all values."""
        assert "black" in yes_no(True, is_colored=False)
        assert "black" in yes_no(False, is_colored=False)


class TestNformatFilter:
    """Tests for the nformat filter function."""

    def test_none_returns_empty(self) -> None:
        """None input returns empty string."""
        assert nformat(None) == ""

    def test_empty_string_returns_empty(self) -> None:
        """Empty string input returns empty string."""
        assert nformat("") == ""

    def test_zero_value(self) -> None:
        """Zero value returns '0' with prefix/suffix."""
        assert nformat(0) == "0"
        assert nformat(0, prefix="$") == "$0"
        assert nformat(0, suffix=" USD") == "0 USD"

    def test_hide_zero(self) -> None:
        """hide_zero=True returns empty string for zero."""
        assert nformat(0, hide_zero=True) == ""
        assert nformat(0.0, hide_zero=True) == ""

    def test_small_number_rounding(self) -> None:
        """Numbers <= 1000 are rounded to specified digits."""
        assert nformat(123.456, digits=2) == "123.46"
        assert nformat(123.456, digits=1) == "123.5"
        assert nformat(123.456, digits=0) == "123.0"

    def test_small_number_string_input(self) -> None:
        """String input works for numbers <= 1000."""
        assert nformat("500.50", digits=2) == "500.5"
        assert nformat("123.456", digits=1) == "123.5"

    def test_large_number_separator(self) -> None:
        """Numbers > 1000 get thousand separators, decimals truncated."""
        assert nformat(1234, separator=",") == "1,234"
        assert nformat(1234567, separator=",") == "1,234,567"
        assert nformat(1234.56, separator=",") == "1,234"

    def test_large_number_string_input(self) -> None:
        """String input works for numbers > 1000."""
        assert nformat("1234", separator=",") == "1,234"
        assert nformat("1234567", separator=" ") == "1 234 567"

    def test_prefix_suffix(self) -> None:
        """Prefix and suffix are applied correctly."""
        assert nformat(100, prefix="$") == "$100.0"
        assert nformat(100, suffix=" USD") == "100.0 USD"
        assert nformat(100, prefix="$", suffix=" USD") == "$100.0 USD"

    def test_decimal_input(self) -> None:
        """Decimal input works correctly."""
        assert nformat(Decimal("123.45"), digits=2) == "123.45"

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (999.99, "999.99"),
            (1000.01, "1,000"),
            (1000, "1000.0"),  # 1000 is not > 1000, goes to else branch
            (1001, "1,001"),
        ],
    )
    def test_threshold_boundary(self, value: float, expected: str) -> None:
        """Test behavior around 1000 threshold."""
        assert nformat(value, separator=",", digits=2) == expected


class TestToJsonFilter:
    """Tests for the to_json filter function."""

    def test_simple_dict(self) -> None:
        """Simple dict is encoded to JSON."""
        result = to_json({"key": "value"})
        assert result == '{"key": "value"}'

    def test_nested_dict(self) -> None:
        """Nested dict is encoded to JSON."""
        result = to_json({"outer": {"inner": 1}})
        assert result == '{"outer": {"inner": 1}}'

    def test_list_value(self) -> None:
        """List values are encoded correctly."""
        result = to_json({"items": [1, 2, 3]})
        assert result == '{"items": [1, 2, 3]}'

    def test_empty_dict(self) -> None:
        """Empty dict returns empty JSON object."""
        assert to_json({}) == "{}"
