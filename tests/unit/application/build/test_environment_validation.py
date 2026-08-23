"""Tests for canonical build-environment validation results."""

from __future__ import annotations

import pytest

from familyos_cli.application.build.environment_validation import (
    EnvironmentValidationFinding,
    EnvironmentValidationResult,
    EnvironmentValidationStatus,
)


def test_environment_validation_finding_preserves_failure() -> None:
    finding = EnvironmentValidationFinding(
        component="virtual-environment",
        diagnostic="virtual environment requirement is not satisfied",
    )

    assert finding.component == "virtual-environment"
    assert (
        finding.diagnostic
        == "virtual environment requirement is not satisfied"
    )


@pytest.mark.parametrize(
    ("component", "diagnostic", "message"),
    (
        (
            "",
            "failure",
            "environment validation component must not be empty",
        ),
        (
            "environment",
            "",
            "environment validation diagnostic must not be empty",
        ),
    ),
)
def test_environment_validation_finding_rejects_incomplete_failure(
    component: str,
    diagnostic: str,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        EnvironmentValidationFinding(
            component=component,
            diagnostic=diagnostic,
        )


def test_successful_environment_validation_has_no_findings() -> None:
    result = EnvironmentValidationResult(
        status=EnvironmentValidationStatus.SUCCEEDED,
    )

    assert result.successful is True
    assert result.findings == ()
    assert result.diagnostic is None


def test_failed_environment_validation_preserves_findings() -> None:
    findings = (
        EnvironmentValidationFinding(
            component="temporary-storage",
            diagnostic="temporary storage is unavailable",
        ),
        EnvironmentValidationFinding(
            component="filesystem",
            diagnostic="required filesystem access is unavailable",
        ),
    )

    result = EnvironmentValidationResult(
        status=EnvironmentValidationStatus.FAILED,
        findings=findings,
    )

    assert result.successful is False
    assert result.findings == findings
    assert result.diagnostic == (
        "temporary storage is unavailable; "
        "required filesystem access is unavailable"
    )


def test_successful_environment_validation_rejects_findings() -> None:
    finding = EnvironmentValidationFinding(
        component="environment",
        diagnostic="unexpected failure",
    )

    with pytest.raises(
        ValueError,
        match=(
            "successful environment validation must not contain findings"
        ),
    ):
        EnvironmentValidationResult(
            status=EnvironmentValidationStatus.SUCCEEDED,
            findings=(finding,),
        )


def test_failed_environment_validation_requires_findings() -> None:
    with pytest.raises(
        ValueError,
        match="failed environment validation requires findings",
    ):
        EnvironmentValidationResult(
            status=EnvironmentValidationStatus.FAILED,
        )


def test_environment_validation_result_is_immutable() -> None:
    result = EnvironmentValidationResult(
        status=EnvironmentValidationStatus.SUCCEEDED,
    )

    with pytest.raises(AttributeError):
        result.status = (  # type: ignore[misc]
            EnvironmentValidationStatus.FAILED
        )
