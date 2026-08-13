"""Tests for compliance finding workflow status."""

from familyos_cli.plugins.ecosystem.compliance.finding_status import (
    FindingStatus,
)


def test_finding_status_values() -> None:
    """Finding status expose stable serialized values."""

    assert FindingStatus.OPEN.value == "open"
