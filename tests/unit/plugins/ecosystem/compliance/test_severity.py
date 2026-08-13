"""Tests for compliance rule severity levels."""

from familyos_cli.plugins.ecosystem.compliance.severity import Severity


def test_severity_values() -> None:
    """Severity levels expose stable serialized values."""

    assert Severity.INFO.value == "info"
    assert Severity.WARNING.value == "warning"
    assert Severity.ERROR.value == "error"
    assert Severity.CRITICAL.value == "critical"
