"""Tests for the validator run result model."""

from familyos_cli.plugins.ecosystem.compliance.validator_run_result import (
    ValidatorRunResult,
)
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)


def test_validator_run_result_defaults_to_empty_message() -> None:
    """A ValidatorRunResult defaults to an empty message."""

    result = ValidatorRunResult(status=ValidatorStatus.SUCCESS, evidence=())

    assert result.message == ""
