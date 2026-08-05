"""Tests for SecurityLevel."""

from familyos_cli.plugins.builtin.security.domain.security_level import (
    SecurityLevel,
)


def test_security_level_values() -> None:
    """Security levels expose expected values."""

    assert SecurityLevel.LOW.value == "low"
    assert SecurityLevel.MEDIUM.value == "medium"
    assert SecurityLevel.HIGH.value == "high"
    assert SecurityLevel.CRITICAL.value == "critical"


def test_security_level_contains_all_levels() -> None:
    """Security levels contain four entries."""

    assert len(SecurityLevel) == 4
