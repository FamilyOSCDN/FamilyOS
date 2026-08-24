"""Tests for the Testing Framework clock authority."""

from __future__ import annotations

from datetime import UTC, datetime

from familyos_cli.application.ports.testing.testing_clock import TestingClockPort


class _Clock(TestingClockPort):
    def now(self) -> datetime:
        return datetime(
            2026,
            8,
            24,
            19,
            45,
            tzinfo=UTC,
        )


def test_clock_port_exposes_timezone_aware_current_time() -> None:
    current = _Clock().now()

    assert current == datetime(
        2026,
        8,
        24,
        19,
        45,
        tzinfo=UTC,
    )
    assert current.utcoffset() is not None
