"""Tests for final effective-configuration validation results."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.application.build.effective_configuration_validation import (
    EffectiveConfigurationValidationFinding,
    EffectiveConfigurationValidationResult,
    EffectiveConfigurationValidationStatus,
)


def test_successful_result_has_no_findings() -> None:
    result = EffectiveConfigurationValidationResult(
        status=EffectiveConfigurationValidationStatus.SUCCEEDED,
    )

    assert result.successful is True
    assert result.findings == ()
    assert result.diagnostic is None


def test_failed_result_preserves_deterministic_findings() -> None:
    findings = (
        EffectiveConfigurationValidationFinding(
            component="profile",
            diagnostic="resolved profile is inconsistent",
        ),
        EffectiveConfigurationValidationFinding(
            component="target",
            diagnostic="resolved target is inconsistent",
        ),
    )

    result = EffectiveConfigurationValidationResult(
        status=EffectiveConfigurationValidationStatus.FAILED,
        findings=findings,
    )

    assert result.successful is False
    assert result.findings == findings
    assert result.diagnostic == (
        "resolved profile is inconsistent; resolved target is inconsistent"
    )


@pytest.mark.parametrize(
    ("component", "diagnostic", "message"),
    (
        (
            "",
            "failure",
            "effective configuration validation component must not be empty",
        ),
        (
            "profile",
            "",
            "effective configuration validation diagnostic must not be empty",
        ),
    ),
)
def test_finding_rejects_incomplete_failure(
    component: str,
    diagnostic: str,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        EffectiveConfigurationValidationFinding(
            component=component,
            diagnostic=diagnostic,
        )


def test_successful_result_rejects_findings() -> None:
    finding = EffectiveConfigurationValidationFinding(
        component="profile",
        diagnostic="failure",
    )

    with pytest.raises(
        ValueError,
        match=(
            "successful effective configuration validation must not "
            "contain findings"
        ),
    ):
        EffectiveConfigurationValidationResult(
            status=EffectiveConfigurationValidationStatus.SUCCEEDED,
            findings=(finding,),
        )


def test_failed_result_requires_findings() -> None:
    with pytest.raises(
        ValueError,
        match="failed effective configuration validation requires findings",
    ):
        EffectiveConfigurationValidationResult(
            status=EffectiveConfigurationValidationStatus.FAILED,
        )


def test_result_is_immutable() -> None:
    result = EffectiveConfigurationValidationResult(
        status=EffectiveConfigurationValidationStatus.SUCCEEDED,
    )

    with pytest.raises(FrozenInstanceError):
        result.status = (  # type: ignore[misc]
            EffectiveConfigurationValidationStatus.FAILED
        )
