"""Tests for the final canonical Build Result contract."""

from pathlib import Path
from typing import cast

import pytest

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.build_validation import (
    BuildValidationResult,
)


def test_canonical_build_result_preserves_established_authorities() -> None:
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    package_result = cast(CanonicalPackageBuildResult, object())
    validation_result = cast(BuildValidationResult, object())
    evidence_reference = Path("/tmp/build-evidence.json")

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=validation_result,
        evidence_reference=evidence_reference,
    )

    assert result.package_result is package_result
    assert result.validation_result is validation_result
    assert result.evidence_reference is evidence_reference


def test_canonical_build_result_allows_absent_post_execution_authorities() -> None:
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    package_result = cast(CanonicalPackageBuildResult, object())

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=None,
        evidence_reference=None,
    )

    assert result.package_result is package_result
    assert result.validation_result is None
    assert result.evidence_reference is None


def test_canonical_build_result_projects_build_identity_and_context() -> None:
    from familyos_cli.application.build.build_context import (
        BuildProfile,
        BuildTarget,
    )
    from familyos_cli.application.build.build_id import BuildId
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _Context:
        profile = BuildProfile.CI
        target = BuildTarget.FAMILYOS_CLI_PACKAGE

    class _PackageResult:
        def __init__(self) -> None:
            self.build_id = BuildId.generate()
            self.build_context = _Context()

    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(),
    )

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=None,
        evidence_reference=None,
    )

    assert result.build_id is package_result.build_id
    assert result.profile is BuildProfile.CI
    assert result.target is BuildTarget.FAMILYOS_CLI_PACKAGE


def test_profile_requires_build_context() -> None:
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        build_context = None

    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(),
    )

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=None,
        evidence_reference=None,
    )

    with pytest.raises(
        RuntimeError,
        match="Canonical Build Result does not contain Build Context",
    ):
        _ = result.profile


def test_target_requires_build_context() -> None:
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        build_context = None

    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(),
    )

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=None,
        evidence_reference=None,
    )

    with pytest.raises(
        RuntimeError,
        match="Canonical Build Result does not contain Build Context",
    ):
        _ = result.target


def test_canonical_build_result_projects_execution_and_validation_status() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationStatus,
    )
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )
    from familyos_cli.application.build.package_build import PackageBuildStatus

    class _PackageResult:
        status = PackageBuildStatus.SUCCEEDED

    class _ValidationResult:
        status = BuildValidationStatus.PASSED

    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(),
    )
    validation_result = cast(
        BuildValidationResult,
        _ValidationResult(),
    )

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=validation_result,
        evidence_reference=None,
    )

    assert result.execution_status is PackageBuildStatus.SUCCEEDED
    assert result.validation_status is BuildValidationStatus.PASSED


def test_canonical_build_result_allows_absent_validation_status() -> None:
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )
    from familyos_cli.application.build.package_build import PackageBuildStatus

    class _PackageResult:
        status = PackageBuildStatus.FAILED

    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(),
    )

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=None,
        evidence_reference=None,
    )

    assert result.execution_status is PackageBuildStatus.FAILED
    assert result.validation_status is None


def test_canonical_build_result_projects_artifact_manifest() -> None:
    from familyos_cli.application.build.artifact_manifest import ArtifactManifest
    from familyos_cli.application.build.build_id import BuildId
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    manifest = ArtifactManifest(
        build_id=BuildId.generate(),
        entries=(),
    )

    class _PackageResult:
        artifact_manifest = manifest

    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(),
    )

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=None,
        evidence_reference=None,
    )

    assert result.artifact_manifest is manifest


def test_canonical_build_result_allows_absent_artifact_manifest() -> None:
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        artifact_manifest = None

    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(),
    )

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=None,
        evidence_reference=None,
    )

    assert result.artifact_manifest is None


def test_canonical_build_result_projects_package_diagnostic() -> None:
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        diagnostic = "package build failed"

    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(),
    )

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=None,
        evidence_reference=None,
    )

    assert result.diagnostic == "package build failed"


def test_canonical_build_result_prefers_validation_failure_diagnostic() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationCheckResult,
        BuildValidationDomain,
        BuildValidationRequirement,
        BuildValidationStatus,
    )
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        diagnostic = None

    validation_result = BuildValidationResult(
        build_id=cast(object, None),  # type: ignore[arg-type]
        profile=cast(object, None),  # type: ignore[arg-type]
        checks=(
            BuildValidationCheckResult(
                check_id="artifact-integrity",
                domain=BuildValidationDomain.INTEGRITY,
                requirement=BuildValidationRequirement.REQUIRED,
                status=BuildValidationStatus.FAILED,
                diagnostic="artifact integrity verification failed",
            ),
        ),
        status=BuildValidationStatus.FAILED,
    )

    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(),
    )

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=validation_result,
        evidence_reference=None,
    )

    assert result.diagnostic == "artifact integrity verification failed"


def test_canonical_build_result_has_no_diagnostic_when_none_exists() -> None:
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        diagnostic = None

    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(),
    )

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=None,
        evidence_reference=None,
    )

    assert result.diagnostic is None


def test_canonical_build_result_has_no_failure_category_when_successful() -> None:
    from typing import cast

    from familyos_cli.application.build.artifact_discovery import (
        CanonicalPackageBuildResult,
    )
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        successful = True
        execution_observations = ()

    result = CanonicalBuildResult(
        package_result=cast(CanonicalPackageBuildResult, _PackageResult()),
        validation_result=None,
        evidence_reference=None,
    )

    assert result.failure_category is None


def test_canonical_build_result_projects_required_validation_failure_category(
) -> None:
    from typing import cast

    from familyos_cli.application.build.artifact_discovery import (
        CanonicalPackageBuildResult,
    )
    from familyos_cli.application.build.build_failure_category import (
        BuildFailureCategory,
    )
    from familyos_cli.application.build.build_validation import (
        BuildValidationCheckResult,
        BuildValidationDomain,
        BuildValidationRequirement,
        BuildValidationResult,
        BuildValidationStatus,
    )
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        successful = True
        execution_observations = ()

    validation_result = BuildValidationResult(
        build_id=cast(object, None),  # type: ignore[arg-type]
        profile=cast(object, None),  # type: ignore[arg-type]
        checks=(
            BuildValidationCheckResult(
                check_id="artifact-integrity",
                domain=BuildValidationDomain.INTEGRITY,
                requirement=BuildValidationRequirement.REQUIRED,
                status=BuildValidationStatus.FAILED,
                diagnostic="artifact integrity verification failed",
            ),
        ),
        status=BuildValidationStatus.FAILED,
    )

    result = CanonicalBuildResult(
        package_result=cast(CanonicalPackageBuildResult, _PackageResult()),
        validation_result=validation_result,
        evidence_reference=None,
    )

    assert result.failure_category is BuildFailureCategory.INTEGRITY


def test_canonical_build_result_projects_failed_execution_stage_category(
) -> None:
    from typing import cast

    from familyos_cli.application.build.artifact_discovery import (
        CanonicalPackageBuildResult,
    )
    from familyos_cli.application.build.build_execution_observation import (
        BuildExecutionObservation,
        BuildExecutionStage,
        BuildExecutionStageStatus,
    )
    from familyos_cli.application.build.build_failure_category import (
        BuildFailureCategory,
    )
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        successful = False
        execution_observations = (
            BuildExecutionObservation(
                stage=BuildExecutionStage.VALIDATE_TOOLCHAIN,
                status=BuildExecutionStageStatus.FAILED,
                duration_seconds=0.1,
                diagnostic="unsupported build toolchain",
            ),
        )

    result = CanonicalBuildResult(
        package_result=cast(CanonicalPackageBuildResult, _PackageResult()),
        validation_result=None,
        evidence_reference=None,
    )

    assert result.failure_category is BuildFailureCategory.TOOLCHAIN


def test_canonical_build_result_validation_failure_precedes_execution_failure(
) -> None:
    from typing import cast

    from familyos_cli.application.build.artifact_discovery import (
        CanonicalPackageBuildResult,
    )
    from familyos_cli.application.build.build_execution_observation import (
        BuildExecutionObservation,
        BuildExecutionStage,
        BuildExecutionStageStatus,
    )
    from familyos_cli.application.build.build_failure_category import (
        BuildFailureCategory,
    )
    from familyos_cli.application.build.build_validation import (
        BuildValidationCheckResult,
        BuildValidationDomain,
        BuildValidationRequirement,
        BuildValidationResult,
        BuildValidationStatus,
    )
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        successful = False
        execution_observations = (
            BuildExecutionObservation(
                stage=BuildExecutionStage.PACKAGE,
                status=BuildExecutionStageStatus.FAILED,
                duration_seconds=0.2,
            ),
        )

    validation_result = BuildValidationResult(
        build_id=cast(object, None),  # type: ignore[arg-type]
        profile=cast(object, None),  # type: ignore[arg-type]
        checks=(
            BuildValidationCheckResult(
                check_id="dependency-consistency",
                domain=BuildValidationDomain.DEPENDENCY,
                requirement=BuildValidationRequirement.REQUIRED,
                status=BuildValidationStatus.FAILED,
                diagnostic="dependency state is inconsistent",
            ),
        ),
        status=BuildValidationStatus.FAILED,
    )

    result = CanonicalBuildResult(
        package_result=cast(CanonicalPackageBuildResult, _PackageResult()),
        validation_result=validation_result,
        evidence_reference=None,
    )

    assert result.failure_category is BuildFailureCategory.DEPENDENCY


def test_canonical_build_result_falls_back_to_execution_failure_category(
) -> None:
    from typing import cast

    from familyos_cli.application.build.artifact_discovery import (
        CanonicalPackageBuildResult,
    )
    from familyos_cli.application.build.build_failure_category import (
        BuildFailureCategory,
    )
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        successful = False
        execution_observations = ()

    result = CanonicalBuildResult(
        package_result=cast(CanonicalPackageBuildResult, _PackageResult()),
        validation_result=None,
        evidence_reference=None,
    )

    assert result.failure_category is BuildFailureCategory.EXECUTION


def test_successful_canonical_build_result_has_no_corrective_information(
) -> None:
    from typing import cast

    from familyos_cli.application.build.artifact_discovery import (
        CanonicalPackageBuildResult,
    )
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        successful = True
        execution_observations = ()

    result = CanonicalBuildResult(
        package_result=cast(CanonicalPackageBuildResult, _PackageResult()),
        validation_result=None,
        evidence_reference=None,
    )

    assert result.corrective_information is None


def test_failed_canonical_build_result_projects_corrective_information(
) -> None:
    from typing import cast

    from familyos_cli.application.build.artifact_discovery import (
        CanonicalPackageBuildResult,
    )
    from familyos_cli.application.build.build_execution_observation import (
        BuildExecutionObservation,
        BuildExecutionStage,
        BuildExecutionStageStatus,
    )
    from familyos_cli.application.build.canonical_build_result import (
        CanonicalBuildResult,
    )

    class _PackageResult:
        successful = False
        execution_observations = (
            BuildExecutionObservation(
                stage=BuildExecutionStage.VALIDATE_TOOLCHAIN,
                status=BuildExecutionStageStatus.FAILED,
                duration_seconds=0.1,
                diagnostic="unsupported build toolchain",
            ),
        )

    result = CanonicalBuildResult(
        package_result=cast(CanonicalPackageBuildResult, _PackageResult()),
        validation_result=None,
        evidence_reference=None,
    )

    assert result.corrective_information == (
        "Restore the required build toolchain and retry."
    )
