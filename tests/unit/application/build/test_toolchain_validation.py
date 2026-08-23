"""Tests for canonical build-toolchain validation result models."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.application.build.toolchain_validation import (
    ToolchainValidationFinding,
    ToolchainValidationResult,
    ToolchainValidationStatus,
)


def test_successful_result_has_no_findings() -> None:
    result = ToolchainValidationResult(
        status=ToolchainValidationStatus.SUCCEEDED,
    )

    assert result.successful is True
    assert result.findings == ()
    assert result.diagnostic is None


def test_failed_result_preserves_deterministic_findings() -> None:
    findings = (
        ToolchainValidationFinding(
            component="python",
            diagnostic="Python 3.12.9 does not satisfy >=3.13",
        ),
        ToolchainValidationFinding(
            component="build",
            diagnostic="build 1.4.0 does not satisfy >=1.5",
        ),
    )

    result = ToolchainValidationResult(
        status=ToolchainValidationStatus.FAILED,
        findings=findings,
    )

    assert result.successful is False
    assert result.findings == findings
    assert result.diagnostic == (
        "Python 3.12.9 does not satisfy >=3.13; "
        "build 1.4.0 does not satisfy >=1.5"
    )


@pytest.mark.parametrize(
    ("component", "diagnostic", "message"),
    (
        ("", "failure", "toolchain validation component must not be empty"),
        ("python", "", "toolchain validation diagnostic must not be empty"),
    ),
)
def test_finding_rejects_incomplete_identity(
    component: str,
    diagnostic: str,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        ToolchainValidationFinding(
            component=component,
            diagnostic=diagnostic,
        )


def test_successful_result_rejects_findings() -> None:
    with pytest.raises(
        ValueError,
        match="successful toolchain validation must not contain findings",
    ):
        ToolchainValidationResult(
            status=ToolchainValidationStatus.SUCCEEDED,
            findings=(
                ToolchainValidationFinding(
                    component="python",
                    diagnostic="failure",
                ),
            ),
        )


def test_failed_result_requires_findings() -> None:
    with pytest.raises(
        ValueError,
        match="failed toolchain validation must contain findings",
    ):
        ToolchainValidationResult(
            status=ToolchainValidationStatus.FAILED,
        )


def test_result_is_immutable() -> None:
    result = ToolchainValidationResult(
        status=ToolchainValidationStatus.SUCCEEDED,
    )

    with pytest.raises(FrozenInstanceError):
        result.status = ToolchainValidationStatus.FAILED  # type: ignore[misc]
