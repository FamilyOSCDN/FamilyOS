"""Tests for the system-backed Testing Framework clock."""

from __future__ import annotations

from datetime import datetime

from familyos_cli.infrastructure.testing.system_testing_clock import (
    SystemTestingClock,
)

from familyos_cli.application.ports.testing import TestingClockPort


def test_system_clock_implements_testing_clock_port() -> None:
    assert isinstance(
        SystemTestingClock(),
        TestingClockPort,
    )


def test_system_clock_returns_timezone_aware_datetime() -> None:
    current = SystemTestingClock().now()

    assert isinstance(current, datetime)
    assert current.tzinfo is not None
    assert current.utcoffset() is not None
