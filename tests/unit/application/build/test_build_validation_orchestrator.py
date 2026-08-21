"""Tests for canonical Build Validation decision orchestration."""

from __future__ import annotations

from uuid import UUID

from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationCheckResult,
    BuildValidationDomain,
    BuildValidationProfile,
    BuildValidationRequirement,
    BuildValidationStatus,
)
from familyos_cli.application.build.build_validation_orchestrator import (
    BuildValidationOrchestrator,
)

_BUILD_ID = BuildId(UUID("01234567-89ab-4cde-8f01-23456789abcd"))


def _check(
    *,
    check_id: str,
    domain: BuildValidationDomain,
    requirement: BuildValidationRequirement,
    status: BuildValidationStatus,
    diagnostic: str | None = None,
) -> BuildValidationCheckResult:
    return BuildValidationCheckResult(
        check_id=check_id,
        domain=domain,
        requirement=requirement,
        status=status,
        diagnostic=diagnostic,
    )


def test_required_failure_fails_overall_validation() -> None:
    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.CI,
        checks=(
            _check(
                check_id="artifact-structure",
                domain=BuildValidationDomain.ARTIFACT,
                requirement=BuildValidationRequirement.REQUIRED,
                status=BuildValidationStatus.FAILED,
                diagnostic="wheel structure is invalid",
            ),
        ),
    )

    assert result.status is BuildValidationStatus.FAILED
    assert not result.successful
    assert len(result.failures) == 1
    assert result.failures[0].check_id == "artifact-structure"
    assert result.failures[0].diagnostic == "wheel structure is invalid"


def test_optional_failure_does_not_fail_overall_validation() -> None:
    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.DEVELOPMENT,
        checks=(
            _check(
                check_id="functional-wheel",
                domain=BuildValidationDomain.FUNCTIONAL_ARTIFACT,
                requirement=BuildValidationRequirement.OPTIONAL,
                status=BuildValidationStatus.FAILED,
                diagnostic="clean install smoke failed",
            ),
        ),
    )

    assert result.status is BuildValidationStatus.PASSED
    assert result.successful
    assert result.failures == ()
    assert len(result.warnings) == 1
    assert result.warnings[0].check_id == "functional-wheel"


def test_informational_failure_does_not_fail_overall_validation() -> None:
    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.DEVELOPMENT,
        checks=(
            _check(
                check_id="environment-observation",
                domain=BuildValidationDomain.ENVIRONMENT,
                requirement=BuildValidationRequirement.INFORMATIONAL,
                status=BuildValidationStatus.FAILED,
                diagnostic="environment differs from canonical CI",
            ),
        ),
    )

    assert result.status is BuildValidationStatus.PASSED
    assert result.successful
    assert result.failures == ()
    assert result.warnings == ()
    assert result.checks[0].diagnostic == (
        "environment differs from canonical CI"
    )


def test_required_skipped_check_fails_overall_validation() -> None:
    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.VALIDATION,
        checks=(
            _check(
                check_id="evidence",
                domain=BuildValidationDomain.EVIDENCE,
                requirement=BuildValidationRequirement.REQUIRED,
                status=BuildValidationStatus.SKIPPED,
                diagnostic="required evidence validation was not executed",
            ),
        ),
    )

    assert result.status is BuildValidationStatus.FAILED
    assert not result.successful
    assert result.checks[0].diagnostic == (
        "required evidence validation was not executed"
    )


def test_all_required_passes_produce_passed_decision() -> None:
    checks = (
        _check(
            check_id="execution",
            domain=BuildValidationDomain.EXECUTION,
            requirement=BuildValidationRequirement.REQUIRED,
            status=BuildValidationStatus.PASSED,
        ),
        _check(
            check_id="artifact",
            domain=BuildValidationDomain.ARTIFACT,
            requirement=BuildValidationRequirement.REQUIRED,
            status=BuildValidationStatus.PASSED,
        ),
        _check(
            check_id="integrity",
            domain=BuildValidationDomain.INTEGRITY,
            requirement=BuildValidationRequirement.REQUIRED,
            status=BuildValidationStatus.PASSED,
        ),
    )

    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.CI,
        checks=checks,
    )

    assert result.status is BuildValidationStatus.PASSED
    assert result.successful
    assert result.checks == checks
    assert result.failures == ()
    assert result.warnings == ()


def test_result_preserves_build_id_profile_and_check_order() -> None:
    checks = (
        _check(
            check_id="first",
            domain=BuildValidationDomain.INPUT,
            requirement=BuildValidationRequirement.REQUIRED,
            status=BuildValidationStatus.PASSED,
        ),
        _check(
            check_id="second",
            domain=BuildValidationDomain.CONFIGURATION,
            requirement=BuildValidationRequirement.OPTIONAL,
            status=BuildValidationStatus.PASSED,
        ),
    )

    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.RELEASE_CANDIDATE,
        checks=checks,
    )

    assert result.build_id == _BUILD_ID
    assert result.profile is BuildValidationProfile.RELEASE_CANDIDATE
    assert result.checks == checks


def test_empty_check_set_is_currently_passed() -> None:
    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.DEVELOPMENT,
        checks=(),
    )

    assert result.status is BuildValidationStatus.PASSED
    assert result.successful
    assert result.checks == ()
