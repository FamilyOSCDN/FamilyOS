"""Tests for compliance validator execution statuses."""

from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)


def test_validator_status_values() -> None:
    """Validator statuses expose stable serialized values."""

    assert ValidatorStatus.SUCCESS.value == "success"
    assert ValidatorStatus.PARTIAL.value == "partial"
    assert ValidatorStatus.FAILED.value == "failed"
    assert ValidatorStatus.SKIPPED.value == "skipped"
    assert ValidatorStatus.ERROR.value == "error"
