"""Tests for verification result."""

from familyos_cli.plugins.ecosystem.verification import (
    VerificationResult,
)


def test_valid_result_reports_success() -> None:
    """Valid result should report success."""

    result = VerificationResult(
        valid=True,
        reason="Package verified.",
    )

    assert result.is_valid() is True
    assert result.successful is True
    assert result.failed is False
    assert result.reason == "Package verified."


def test_invalid_result_reports_failure() -> None:
    """Invalid result should report failure."""

    result = VerificationResult(
        valid=False,
        reason="Plugin name is missing.",
    )

    assert result.is_valid() is False
    assert result.successful is False
    assert result.failed is True
    assert result.reason == "Plugin name is missing."
