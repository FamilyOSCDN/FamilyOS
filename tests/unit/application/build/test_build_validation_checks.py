"""Tests for mapping canonical package-build results to validation checks."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

from familyos_cli.application.build.artifact_discovery import (
    ArtifactDiscoveryResult,
    ArtifactDiscoveryStatus,
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.artifact_manifest import ArtifactManifest
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationDomain,
    BuildValidationRequirement,
    BuildValidationStatus,
)
from familyos_cli.application.build.build_validation_checks import (
    BuildValidationCheckFactory,
)
from familyos_cli.application.build.package_build import (
    PackageBuildResult,
    PackageBuildStatus,
)
from familyos_cli.application.build.package_validation import (
    PackageStructuralValidationStatus,
    PythonPackageStructuralValidationResult,
)
from familyos_cli.application.build.source_state import SourceState

_BUILD_ID = BuildId(
    UUID("01234567-89ab-4cde-8f01-23456789abcd")
)

_SOURCE_STATE = SourceState(
    revision="0123456789abcdef0123456789abcdef01234567",
    dirty=False,
)


def _successful_result(
    tmp_path: Path,
) -> CanonicalPackageBuildResult:
    output_dir = tmp_path / "dist"
    output_dir.mkdir()

    return CanonicalPackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        execution=PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
        ),
        source_state=_SOURCE_STATE,
        build_id=_BUILD_ID,
        artifact_integrities=(),
        artifact_manifest=ArtifactManifest(
            build_id=_BUILD_ID,
            entries=(),
        ),
        discovery=ArtifactDiscoveryResult(
            status=ArtifactDiscoveryStatus.SUCCEEDED,
            output_dir=output_dir,
        ),
        validation=PythonPackageStructuralValidationResult(
            status=PackageStructuralValidationStatus.VALID,
            candidate_results=(),
        ),
    )


def test_factory_emits_canonical_check_order(
    tmp_path: Path,
) -> None:
    result = _successful_result(tmp_path)

    checks = BuildValidationCheckFactory().from_package_build(
        result,
        functional_requirement=BuildValidationRequirement.OPTIONAL,
    )

    assert tuple(check.check_id for check in checks) == (
        "build-execution",
        "artifact-discovery",
        "artifact-structural-validation",
        "artifact-metadata",
        "artifact-integrity",
        "functional-artifact-validation",
    )


def test_factory_maps_established_domains(
    tmp_path: Path,
) -> None:
    result = _successful_result(tmp_path)

    checks = BuildValidationCheckFactory().from_package_build(
        result,
        functional_requirement=BuildValidationRequirement.OPTIONAL,
    )

    assert tuple(check.domain for check in checks) == (
        BuildValidationDomain.EXECUTION,
        BuildValidationDomain.ARTIFACT,
        BuildValidationDomain.ARTIFACT,
        BuildValidationDomain.METADATA,
        BuildValidationDomain.INTEGRITY,
        BuildValidationDomain.FUNCTIONAL_ARTIFACT,
    )


def test_missing_discovery_fails_required_artifact_check(
    tmp_path: Path,
) -> None:
    result = _successful_result(tmp_path)

    result = CanonicalPackageBuildResult(
        status=result.status,
        execution=result.execution,
        source_state=result.source_state,
        build_id=result.build_id,
    )

    checks = BuildValidationCheckFactory().from_package_build(
        result,
        functional_requirement=BuildValidationRequirement.OPTIONAL,
    )

    discovery = next(
        check
        for check in checks
        if check.check_id == "artifact-discovery"
    )

    assert discovery.status is BuildValidationStatus.FAILED
    assert (
        discovery.requirement
        is BuildValidationRequirement.REQUIRED
    )
    assert (
        discovery.diagnostic
        == "artifact discovery was not completed"
    )


def test_missing_manifest_fails_metadata_check(
    tmp_path: Path,
) -> None:
    result = _successful_result(tmp_path)

    result = CanonicalPackageBuildResult(
        status=result.status,
        execution=result.execution,
        source_state=result.source_state,
        build_id=result.build_id,
        discovery=result.discovery,
        validation=result.validation,
    )

    checks = BuildValidationCheckFactory().from_package_build(
        result,
        functional_requirement=BuildValidationRequirement.OPTIONAL,
    )

    metadata = next(
        check
        for check in checks
        if check.check_id == "artifact-metadata"
    )

    assert metadata.status is BuildValidationStatus.FAILED
    assert metadata.domain is BuildValidationDomain.METADATA


def test_unperformed_optional_functional_validation_is_skipped(
    tmp_path: Path,
) -> None:
    result = _successful_result(tmp_path)

    checks = BuildValidationCheckFactory().from_package_build(
        result,
        functional_requirement=BuildValidationRequirement.OPTIONAL,
    )

    functional = checks[-1]

    assert functional.status is BuildValidationStatus.SKIPPED
    assert (
        functional.requirement
        is BuildValidationRequirement.OPTIONAL
    )
    assert functional.diagnostic == (
        "functional artifact validation was not executed"
    )


def test_unperformed_required_functional_validation_is_skipped_for_orchestrator(
    tmp_path: Path,
) -> None:
    result = _successful_result(tmp_path)

    checks = BuildValidationCheckFactory().from_package_build(
        result,
        functional_requirement=BuildValidationRequirement.REQUIRED,
    )

    functional = checks[-1]

    assert functional.status is BuildValidationStatus.SKIPPED
    assert (
        functional.requirement
        is BuildValidationRequirement.REQUIRED
    )


def test_factory_and_orchestrator_produce_failed_decision_when_required_check_fails(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationProfile,
    )
    from familyos_cli.application.build.build_validation_orchestrator import (
        BuildValidationOrchestrator,
    )

    result = _successful_result(tmp_path)

    checks = BuildValidationCheckFactory().from_package_build(
        result,
        functional_requirement=BuildValidationRequirement.OPTIONAL,
    )

    validation_result = BuildValidationOrchestrator().execute(
        build_id=result.build_id,
        profile=BuildValidationProfile.VALIDATION,
        checks=checks,
    )

    integrity = next(
        check
        for check in validation_result.checks
        if check.check_id == "artifact-integrity"
    )

    assert integrity.status is BuildValidationStatus.FAILED
    assert validation_result.status is BuildValidationStatus.FAILED
    assert not validation_result.successful
    assert integrity in validation_result.failures


def test_real_canonical_build_maps_to_successful_validation_decision(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationProfile,
    )
    from familyos_cli.application.build.build_validation_orchestrator import (
        BuildValidationOrchestrator,
    )
    from familyos_cli.bootstrap import ApplicationFactory

    result = ApplicationFactory.create().run_package_build_use_case().execute(
        tmp_path / "dist",
        validate_functionally=True,
    )

    assert result.successful

    checks = BuildValidationCheckFactory().from_package_build(
        result,
        functional_requirement=BuildValidationRequirement.REQUIRED,
    )

    validation_result = BuildValidationOrchestrator().execute(
        build_id=result.build_id,
        profile=BuildValidationProfile.VALIDATION,
        checks=checks,
    )

    assert validation_result.successful
    assert validation_result.status is BuildValidationStatus.PASSED

    assert tuple(check.status for check in validation_result.checks) == (
        BuildValidationStatus.PASSED,
        BuildValidationStatus.PASSED,
        BuildValidationStatus.PASSED,
        BuildValidationStatus.PASSED,
        BuildValidationStatus.PASSED,
        BuildValidationStatus.PASSED,
    )

    assert validation_result.failures == ()
    assert validation_result.warnings == ()


def test_dependency_validation_maps_canonical_gate_results() -> None:
    from familyos_cli.application.validation import (
        GateResult,
        ValidationStatus,
    )

    checks = BuildValidationCheckFactory().from_dependency_validation(
        (
            GateResult(
                gate_id="dependency-freshness",
                status=ValidationStatus.PASSED,
            ),
            GateResult(
                gate_id="dependency-consistency",
                status=ValidationStatus.PASSED,
            ),
        )
    )

    assert tuple(check.check_id for check in checks) == (
        "dependency-freshness",
        "dependency-consistency",
    )
    assert all(
        check.domain is BuildValidationDomain.DEPENDENCY
        for check in checks
    )
    assert all(
        check.requirement is BuildValidationRequirement.REQUIRED
        for check in checks
    )
    assert all(
        check.status is BuildValidationStatus.PASSED
        for check in checks
    )


def test_dependency_validation_preserves_failure_diagnostic() -> None:
    from familyos_cli.application.validation import (
        GateResult,
        ValidationStatus,
    )

    checks = BuildValidationCheckFactory().from_dependency_validation(
        (
            GateResult(
                gate_id="dependency-freshness",
                status=ValidationStatus.FAILED,
                exit_code=1,
                diagnostic="dependency lock is stale",
            ),
            GateResult(
                gate_id="dependency-consistency",
                status=ValidationStatus.PASSED,
            ),
        )
    )

    freshness = checks[0]

    assert freshness.status is BuildValidationStatus.FAILED
    assert freshness.diagnostic == "dependency lock is stale"


def test_dependency_validation_consistency_failure_is_required() -> None:
    from familyos_cli.application.validation import (
        GateResult,
        ValidationStatus,
    )

    checks = BuildValidationCheckFactory().from_dependency_validation(
        (
            GateResult(
                gate_id="dependency-freshness",
                status=ValidationStatus.PASSED,
            ),
            GateResult(
                gate_id="dependency-consistency",
                status=ValidationStatus.FAILED,
                diagnostic="installed dependencies are inconsistent",
            ),
        )
    )

    consistency = checks[1]

    assert consistency.status is BuildValidationStatus.FAILED
    assert (
        consistency.requirement
        is BuildValidationRequirement.REQUIRED
    )
    assert (
        consistency.diagnostic
        == "installed dependencies are inconsistent"
    )


def test_dependency_validation_error_blocks_build_validation() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationProfile,
    )
    from familyos_cli.application.build.build_validation_orchestrator import (
        BuildValidationOrchestrator,
    )
    from familyos_cli.application.validation import (
        GateResult,
        ValidationStatus,
    )

    checks = BuildValidationCheckFactory().from_dependency_validation(
        (
            GateResult(
                gate_id="dependency-freshness",
                status=ValidationStatus.ERROR,
                diagnostic="dependency gate could not execute",
            ),
            GateResult(
                gate_id="dependency-consistency",
                status=ValidationStatus.PASSED,
            ),
        )
    )

    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.CI,
        checks=checks,
    )

    assert checks[0].status is BuildValidationStatus.FAILED
    assert checks[0].diagnostic == "dependency gate could not execute"
    assert result.status is BuildValidationStatus.FAILED
    assert not result.successful


def test_dependency_validation_rejects_non_dependency_gate() -> None:
    import pytest

    from familyos_cli.application.validation import (
        GateResult,
        ValidationStatus,
    )

    with pytest.raises(
        ValueError,
        match="Unsupported dependency validation gate",
    ):
        BuildValidationCheckFactory().from_dependency_validation(
            (
                GateResult(
                    gate_id="ruff",
                    status=ValidationStatus.PASSED,
                ),
            )
        )
