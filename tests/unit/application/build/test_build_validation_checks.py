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
from familyos_cli.application.build.build_context import BuildProfile, BuildTarget
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationDomain,
    BuildValidationRequirement,
    BuildValidationStatus,
)
from familyos_cli.application.build.build_validation_checks import (
    BuildValidationCheckFactory,
)
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.effective_build_configuration_view import (
    EffectiveBuildConfigurationView,
)
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.package_build import (
    PackageBuildResult,
    PackageBuildStatus,
)
from familyos_cli.application.build.package_validation import (
    PackageStructuralValidationStatus,
    PythonPackageStructuralValidationResult,
)
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)

_BUILD_ID = BuildId(
    UUID("01234567-89ab-4cde-8f01-23456789abcd")
)

_SOURCE_STATE = SourceState(
    revision="0123456789abcdef0123456789abcdef01234567",
    dirty=False,
)

_DEPENDENCY_STATE = DependencyState(
    declaration_path=Path("/project/pyproject.toml"),
    declaration_digest="a" * 64,
    lock_path=Path("/project/requirements.txt"),
    lock_digest="b" * 64,
)

_TOOLCHAIN_STATE = ToolchainState(
    critical_versions=(
        ToolchainVersion("build", "1.5.0"),
    ),
)

_ENVIRONMENT_STATE = EnvironmentState(
    operating_system="Darwin",
    operating_system_release="24.6.0",
    machine_architecture="arm64",
)


_EFFECTIVE_CONFIGURATION = EffectiveBuildConfigurationView(
    profile=BuildProfile.VALIDATION,
    target=BuildTarget.FAMILYOS_CLI_PACKAGE,
    output_dir=Path("/project/dist"),
    functional_validation=False,
    evidence_output=None,
    evidence_required=False,
    target_supported=True,
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


def test_toolchain_validation_maps_required_toolchain_checks() -> None:
    checks = BuildValidationCheckFactory().from_toolchain_validation(
        python_compatible=True,
        build_available=True,
    )

    assert len(checks) == 2

    python_check, build_check = checks

    assert python_check.check_id == "python-toolchain"
    assert python_check.domain is BuildValidationDomain.TOOLCHAIN
    assert python_check.requirement is BuildValidationRequirement.REQUIRED
    assert python_check.status is BuildValidationStatus.PASSED
    assert python_check.diagnostic is None

    assert build_check.check_id == "python-build-tool"
    assert build_check.domain is BuildValidationDomain.TOOLCHAIN
    assert build_check.requirement is BuildValidationRequirement.REQUIRED
    assert build_check.status is BuildValidationStatus.PASSED
    assert build_check.diagnostic is None


def test_toolchain_validation_python_failure_is_required() -> None:
    checks = BuildValidationCheckFactory().from_toolchain_validation(
        python_compatible=False,
        build_available=True,
        python_diagnostic="Python 3.13 or newer is required",
    )

    python_check, build_check = checks

    assert python_check.status is BuildValidationStatus.FAILED
    assert python_check.diagnostic == "Python 3.13 or newer is required"
    assert build_check.status is BuildValidationStatus.PASSED


def test_toolchain_validation_build_tool_failure_is_required() -> None:
    checks = BuildValidationCheckFactory().from_toolchain_validation(
        python_compatible=True,
        build_available=False,
        build_diagnostic="python -m build is unavailable",
    )

    python_check, build_check = checks

    assert python_check.status is BuildValidationStatus.PASSED
    assert build_check.status is BuildValidationStatus.FAILED
    assert build_check.diagnostic == "python -m build is unavailable"


def test_toolchain_validation_failure_blocks_build_validation() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationProfile,
    )
    from familyos_cli.application.build.build_validation_orchestrator import (
        BuildValidationOrchestrator,
    )

    checks = BuildValidationCheckFactory().from_toolchain_validation(
        python_compatible=False,
        build_available=True,
        python_diagnostic="unsupported Python toolchain",
    )

    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.VALIDATION,
        checks=checks,
    )

    assert result.status is BuildValidationStatus.FAILED
    assert not result.successful


def test_environment_validation_maps_required_environment_checks(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    output_dir = tmp_path / "dist"
    project_root.mkdir()
    output_dir.mkdir()

    checks = BuildValidationCheckFactory().from_environment_validation(
        project_root_available=project_root.is_dir(),
        output_environment_available=output_dir.is_dir(),
    )

    assert len(checks) == 2

    assert checks[0].check_id == "project-environment"
    assert checks[0].domain is BuildValidationDomain.ENVIRONMENT
    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.PASSED
    assert checks[0].diagnostic is None

    assert checks[1].check_id == "output-environment"
    assert checks[1].domain is BuildValidationDomain.ENVIRONMENT
    assert checks[1].requirement is BuildValidationRequirement.REQUIRED
    assert checks[1].status is BuildValidationStatus.PASSED
    assert checks[1].diagnostic is None


def test_environment_validation_project_failure_is_required() -> None:
    checks = BuildValidationCheckFactory().from_environment_validation(
        project_root_available=False,
        output_environment_available=True,
        project_diagnostic="project root is unavailable",
    )

    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.FAILED
    assert checks[0].diagnostic == "project root is unavailable"


def test_environment_validation_output_failure_is_required() -> None:
    checks = BuildValidationCheckFactory().from_environment_validation(
        project_root_available=True,
        output_environment_available=False,
        output_diagnostic="build output environment is unavailable",
    )

    assert checks[1].requirement is BuildValidationRequirement.REQUIRED
    assert checks[1].status is BuildValidationStatus.FAILED
    assert checks[1].diagnostic == "build output environment is unavailable"


def test_environment_validation_failure_blocks_build_validation() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationProfile,
    )
    from familyos_cli.application.build.build_validation_orchestrator import (
        BuildValidationOrchestrator,
    )

    checks = BuildValidationCheckFactory().from_environment_validation(
        project_root_available=True,
        output_environment_available=False,
        output_diagnostic="output directory cannot support package build",
    )

    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.CI,
        checks=checks,
    )

    assert result.status is BuildValidationStatus.FAILED
    assert not result.successful


def test_input_validation_maps_required_build_inputs() -> None:
    checks = BuildValidationCheckFactory().from_input_validation(
        output_dir_valid=True,
        functional_validation_valid=True,
    )

    assert len(checks) == 2

    output_check, functional_check = checks

    assert output_check.check_id == "output-dir-input"
    assert output_check.domain is BuildValidationDomain.INPUT
    assert output_check.requirement is BuildValidationRequirement.REQUIRED
    assert output_check.status is BuildValidationStatus.PASSED
    assert output_check.diagnostic is None

    assert functional_check.check_id == "functional-validation-input"
    assert functional_check.domain is BuildValidationDomain.INPUT
    assert functional_check.requirement is BuildValidationRequirement.REQUIRED
    assert functional_check.status is BuildValidationStatus.PASSED
    assert functional_check.diagnostic is None


def test_input_validation_output_dir_failure_is_required() -> None:
    checks = BuildValidationCheckFactory().from_input_validation(
        output_dir_valid=False,
        functional_validation_valid=True,
        output_dir_diagnostic="build output path input is invalid",
    )

    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.FAILED
    assert checks[0].diagnostic == "build output path input is invalid"


def test_input_validation_functional_option_failure_is_required() -> None:
    checks = BuildValidationCheckFactory().from_input_validation(
        output_dir_valid=True,
        functional_validation_valid=False,
        functional_validation_diagnostic=(
            "functional validation option is invalid"
        ),
    )

    assert checks[1].requirement is BuildValidationRequirement.REQUIRED
    assert checks[1].status is BuildValidationStatus.FAILED
    assert (
        checks[1].diagnostic
        == "functional validation option is invalid"
    )


def test_input_validation_failure_blocks_build_validation() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationProfile,
    )
    from familyos_cli.application.build.build_validation_orchestrator import (
        BuildValidationOrchestrator,
    )

    checks = BuildValidationCheckFactory().from_input_validation(
        output_dir_valid=False,
        functional_validation_valid=True,
        output_dir_diagnostic="invalid build output input",
    )

    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.CI,
        checks=checks,
    )

    assert result.status is BuildValidationStatus.FAILED
    assert not result.successful


def test_configuration_validation_maps_required_build_configuration() -> None:
    checks = BuildValidationCheckFactory().from_configuration_validation(
        package_configuration_valid=True,
        dependency_configuration_valid=True,
    )

    assert len(checks) == 2

    assert checks[0].check_id == "package-configuration"
    assert checks[0].domain is BuildValidationDomain.CONFIGURATION
    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.PASSED
    assert checks[0].diagnostic is None

    assert checks[1].check_id == "dependency-configuration"
    assert checks[1].domain is BuildValidationDomain.CONFIGURATION
    assert checks[1].requirement is BuildValidationRequirement.REQUIRED
    assert checks[1].status is BuildValidationStatus.PASSED
    assert checks[1].diagnostic is None


def test_configuration_validation_package_failure_is_required() -> None:
    checks = BuildValidationCheckFactory().from_configuration_validation(
        package_configuration_valid=False,
        dependency_configuration_valid=True,
        package_diagnostic="canonical package configuration is invalid",
    )

    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.FAILED
    assert (
        checks[0].diagnostic
        == "canonical package configuration is invalid"
    )


def test_configuration_validation_dependency_failure_is_required() -> None:
    checks = BuildValidationCheckFactory().from_configuration_validation(
        package_configuration_valid=True,
        dependency_configuration_valid=False,
        dependency_diagnostic=(
            "canonical dependency configuration is invalid"
        ),
    )

    assert checks[1].requirement is BuildValidationRequirement.REQUIRED
    assert checks[1].status is BuildValidationStatus.FAILED
    assert (
        checks[1].diagnostic
        == "canonical dependency configuration is invalid"
    )


def test_configuration_validation_failure_blocks_build_validation() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationProfile,
    )
    from familyos_cli.application.build.build_validation_orchestrator import (
        BuildValidationOrchestrator,
    )

    checks = BuildValidationCheckFactory().from_configuration_validation(
        package_configuration_valid=False,
        dependency_configuration_valid=True,
        package_diagnostic="invalid canonical build configuration",
    )

    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.CI,
        checks=checks,
    )

    assert result.status is BuildValidationStatus.FAILED
    assert not result.successful


def test_evidence_validation_maps_coherent_build_evidence(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.build_evidence import BuildEvidence
    from familyos_cli.application.build.build_validation import (
        BuildValidationProfile,
        BuildValidationResult,
    )

    evidence = BuildEvidence(
        build_id=_BUILD_ID,
        source_state=_SOURCE_STATE,
        runtime_version="3.13.7",
        dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
        effective_configuration=_EFFECTIVE_CONFIGURATION,
        execution_observations=(),
        validation_result=BuildValidationResult(
            build_id=_BUILD_ID,
            profile=BuildValidationProfile.VALIDATION,
            checks=(),
            status=BuildValidationStatus.PASSED,
        ),
        artifact_manifest=ArtifactManifest(
            build_id=_BUILD_ID,
            entries=(),
        ),
        artifact_integrities=(),
    )

    checks = BuildValidationCheckFactory().from_evidence_validation(
        evidence,
        build_id=_BUILD_ID,
    )

    assert len(checks) == 1

    check = checks[0]

    assert check.check_id == "build-evidence"
    assert check.domain is BuildValidationDomain.EVIDENCE
    assert check.requirement is BuildValidationRequirement.REQUIRED
    assert check.status is BuildValidationStatus.PASSED
    assert check.diagnostic is None


def test_evidence_validation_missing_evidence_is_required_failure() -> None:
    checks = BuildValidationCheckFactory().from_evidence_validation(
        None,
        build_id=_BUILD_ID,
    )

    check = checks[0]

    assert check.domain is BuildValidationDomain.EVIDENCE
    assert check.requirement is BuildValidationRequirement.REQUIRED
    assert check.status is BuildValidationStatus.FAILED
    assert check.diagnostic == "Build Evidence is unavailable"


def test_evidence_validation_rejects_evidence_for_different_build() -> None:
    from familyos_cli.application.build.build_evidence import BuildEvidence
    from familyos_cli.application.build.build_validation import (
        BuildValidationProfile,
        BuildValidationResult,
    )

    other_build_id = BuildId(
        UUID("11234567-89ab-4cde-8f01-23456789abcd")
    )

    evidence = BuildEvidence(
        build_id=other_build_id,
        source_state=_SOURCE_STATE,
        runtime_version="3.13.7",
        dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
        effective_configuration=_EFFECTIVE_CONFIGURATION,
        execution_observations=(),
        validation_result=BuildValidationResult(
            build_id=other_build_id,
            profile=BuildValidationProfile.VALIDATION,
            checks=(),
            status=BuildValidationStatus.PASSED,
        ),
        artifact_manifest=ArtifactManifest(
            build_id=other_build_id,
            entries=(),
        ),
        artifact_integrities=(),
    )

    checks = BuildValidationCheckFactory().from_evidence_validation(
        evidence,
        build_id=_BUILD_ID,
    )

    check = checks[0]

    assert check.status is BuildValidationStatus.FAILED
    assert (
        check.diagnostic
        == "Build Evidence build ID does not match validation build"
    )


def test_evidence_validation_failure_blocks_build_validation() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationProfile,
    )
    from familyos_cli.application.build.build_validation_orchestrator import (
        BuildValidationOrchestrator,
    )

    checks = BuildValidationCheckFactory().from_evidence_validation(
        None,
        build_id=_BUILD_ID,
    )

    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.CI,
        checks=checks,
    )

    assert result.status is BuildValidationStatus.FAILED
    assert not result.successful


def test_source_validation_maps_clean_identified_source() -> None:
    checks = BuildValidationCheckFactory().from_source_validation(
        revision_identified=True,
        working_tree_clean=True,
    )

    assert len(checks) == 2

    revision, working_tree = checks

    assert revision.check_id == "source-revision"
    assert revision.domain is BuildValidationDomain.SOURCE
    assert revision.requirement is BuildValidationRequirement.REQUIRED
    assert revision.status is BuildValidationStatus.PASSED
    assert revision.diagnostic is None

    assert working_tree.check_id == "source-working-tree"
    assert working_tree.domain is BuildValidationDomain.SOURCE
    assert working_tree.requirement is BuildValidationRequirement.REQUIRED
    assert working_tree.status is BuildValidationStatus.PASSED
    assert working_tree.diagnostic is None


def test_source_validation_rejects_unidentified_revision() -> None:
    checks = BuildValidationCheckFactory().from_source_validation(
        revision_identified=False,
        working_tree_clean=True,
        revision_diagnostic="source revision is unavailable",
    )

    revision = checks[0]

    assert revision.check_id == "source-revision"
    assert revision.domain is BuildValidationDomain.SOURCE
    assert revision.requirement is BuildValidationRequirement.REQUIRED
    assert revision.status is BuildValidationStatus.FAILED
    assert revision.diagnostic == "source revision is unavailable"


def test_source_validation_rejects_dirty_working_tree() -> None:
    checks = BuildValidationCheckFactory().from_source_validation(
        revision_identified=True,
        working_tree_clean=False,
        working_tree_diagnostic="source working tree is dirty",
    )

    working_tree = checks[1]

    assert working_tree.check_id == "source-working-tree"
    assert working_tree.domain is BuildValidationDomain.SOURCE
    assert working_tree.requirement is BuildValidationRequirement.REQUIRED
    assert working_tree.status is BuildValidationStatus.FAILED
    assert working_tree.diagnostic == "source working tree is dirty"


def test_source_validation_failure_blocks_build_validation() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationProfile,
    )
    from familyos_cli.application.build.build_validation_orchestrator import (
        BuildValidationOrchestrator,
    )

    checks = BuildValidationCheckFactory().from_source_validation(
        revision_identified=True,
        working_tree_clean=False,
        working_tree_diagnostic="source working tree is dirty",
    )

    result = BuildValidationOrchestrator().execute(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.RELEASE_CANDIDATE,
        checks=checks,
    )

    assert result.status is BuildValidationStatus.FAILED
    assert not result.successful


def test_input_validation_consumes_canonical_authority() -> None:
    from familyos_cli.application.build.build_input_validation import (
        BuildInputValidationCheck,
        BuildInputValidationResult,
    )

    authority = BuildInputValidationResult(
        checks=(
            BuildInputValidationCheck(
                input_name="canonical-input",
                successful=True,
            ),
        ),
    )

    checks = (
        BuildValidationCheckFactory()
        .from_input_validation_result(authority)
    )

    assert len(checks) == 1
    assert checks[0].check_id == "canonical-input"
    assert checks[0].domain is BuildValidationDomain.INPUT
    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.PASSED
    assert checks[0].diagnostic is None


def test_configuration_validation_consumes_canonical_authority() -> None:
    from familyos_cli.application.build.effective_configuration_validation import (
        EffectiveConfigurationValidationResult,
        EffectiveConfigurationValidationStatus,
    )

    authority = EffectiveConfigurationValidationResult(
        status=EffectiveConfigurationValidationStatus.SUCCEEDED,
    )

    checks = (
        BuildValidationCheckFactory()
        .from_configuration_validation_result(authority)
    )

    assert len(checks) == 1
    assert checks[0].check_id == "effective-configuration"
    assert checks[0].domain is BuildValidationDomain.CONFIGURATION
    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.PASSED
    assert checks[0].diagnostic is None


def test_toolchain_validation_consumes_canonical_authority() -> None:
    from familyos_cli.application.build.toolchain_validation import (
        ToolchainValidationResult,
        ToolchainValidationStatus,
    )

    authority = ToolchainValidationResult(
        status=ToolchainValidationStatus.SUCCEEDED,
    )

    checks = (
        BuildValidationCheckFactory()
        .from_toolchain_validation_result(authority)
    )

    assert len(checks) == 1
    assert checks[0].check_id == "canonical-toolchain"
    assert checks[0].domain is BuildValidationDomain.TOOLCHAIN
    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.PASSED
    assert checks[0].diagnostic is None


def test_environment_validation_consumes_canonical_authority() -> None:
    from familyos_cli.application.build.environment_validation import (
        EnvironmentValidationResult,
        EnvironmentValidationStatus,
    )

    authority = EnvironmentValidationResult(
        status=EnvironmentValidationStatus.SUCCEEDED,
    )

    checks = (
        BuildValidationCheckFactory()
        .from_environment_validation_result(authority)
    )

    assert len(checks) == 1
    assert checks[0].check_id == "canonical-environment"
    assert checks[0].domain is BuildValidationDomain.ENVIRONMENT
    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.PASSED
    assert checks[0].diagnostic is None


def test_input_validation_result_preserves_failed_check_diagnostic() -> None:
    from familyos_cli.application.build.build_input_validation import (
        BuildInputValidationCheck,
        BuildInputValidationResult,
    )

    authority = BuildInputValidationResult(
        checks=(
            BuildInputValidationCheck(
                input_name="requirements.txt",
                successful=False,
                diagnostic="required build input missing: requirements.txt",
            ),
        ),
    )

    checks = (
        BuildValidationCheckFactory()
        .from_input_validation_result(authority)
    )

    assert len(checks) == 1
    assert checks[0].check_id == "requirements.txt"
    assert checks[0].domain is BuildValidationDomain.INPUT
    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.FAILED
    assert checks[0].diagnostic == (
        "required build input missing: requirements.txt"
    )


def test_configuration_validation_result_preserves_failure_diagnostic() -> None:
    from familyos_cli.application.build.effective_configuration_validation import (
        EffectiveConfigurationValidationFinding,
        EffectiveConfigurationValidationResult,
        EffectiveConfigurationValidationStatus,
    )

    authority = EffectiveConfigurationValidationResult(
        status=EffectiveConfigurationValidationStatus.FAILED,
        findings=(
            EffectiveConfigurationValidationFinding(
                component="profile",
                diagnostic="resolved profile is inconsistent",
            ),
            EffectiveConfigurationValidationFinding(
                component="target",
                diagnostic="resolved target is inconsistent",
            ),
        ),
    )

    checks = (
        BuildValidationCheckFactory()
        .from_configuration_validation_result(authority)
    )

    assert len(checks) == 1
    assert checks[0].check_id == "effective-configuration"
    assert checks[0].domain is BuildValidationDomain.CONFIGURATION
    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.FAILED
    assert checks[0].diagnostic == (
        "resolved profile is inconsistent; "
        "resolved target is inconsistent"
    )


def test_toolchain_validation_result_preserves_failure_diagnostic() -> None:
    from familyos_cli.application.build.toolchain_validation import (
        ToolchainValidationFinding,
        ToolchainValidationResult,
        ToolchainValidationStatus,
    )

    authority = ToolchainValidationResult(
        status=ToolchainValidationStatus.FAILED,
        findings=(
            ToolchainValidationFinding(
                component="python",
                diagnostic="Python 3.12.9 does not satisfy >=3.13",
            ),
            ToolchainValidationFinding(
                component="build",
                diagnostic="build 1.4.0 does not satisfy >=1.5",
            ),
        ),
    )

    checks = (
        BuildValidationCheckFactory()
        .from_toolchain_validation_result(authority)
    )

    assert len(checks) == 1
    assert checks[0].check_id == "canonical-toolchain"
    assert checks[0].domain is BuildValidationDomain.TOOLCHAIN
    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.FAILED
    assert checks[0].diagnostic == (
        "Python 3.12.9 does not satisfy >=3.13; "
        "build 1.4.0 does not satisfy >=1.5"
    )


def test_environment_validation_result_preserves_failure_diagnostic() -> None:
    from familyos_cli.application.build.environment_validation import (
        EnvironmentValidationFinding,
        EnvironmentValidationResult,
        EnvironmentValidationStatus,
    )

    authority = EnvironmentValidationResult(
        status=EnvironmentValidationStatus.FAILED,
        findings=(
            EnvironmentValidationFinding(
                component="temporary-storage",
                diagnostic="temporary storage is unavailable",
            ),
            EnvironmentValidationFinding(
                component="filesystem",
                diagnostic="required filesystem access is unavailable",
            ),
        ),
    )

    checks = (
        BuildValidationCheckFactory()
        .from_environment_validation_result(authority)
    )

    assert len(checks) == 1
    assert checks[0].check_id == "canonical-environment"
    assert checks[0].domain is BuildValidationDomain.ENVIRONMENT
    assert checks[0].requirement is BuildValidationRequirement.REQUIRED
    assert checks[0].status is BuildValidationStatus.FAILED
    assert checks[0].diagnostic == (
        "temporary storage is unavailable; "
        "required filesystem access is unavailable"
    )


def test_testing_validation_consumes_passing_canonical_pytest_gate() -> None:
    from datetime import UTC, datetime
    from uuid import UUID

    from familyos_cli.application.testing import (
        TestExecutionId,
        TestExecutionResult,
        TestExecutionStatus,
        TestExecutionSummary,
        TestingEvidence,
    )
    from familyos_cli.application.validation.ci_validation import (
        GateResult,
        ValidationStatus,
    )

    evidence = TestingEvidence(
        execution_id=TestExecutionId(
            UUID("01234567-89ab-cdef-0123-456789abcdef")
        ),
        source_revision="0123456789abcdef0123456789abcdef01234567",
        source_dirty=False,
        result=TestExecutionResult(
            status=TestExecutionStatus.PASSED,
            summary=TestExecutionSummary(
                discovered=1,
                executed=1,
                passed=1,
                failed=0,
                skipped=0,
                errors=0,
                duration_seconds=0.1,
            ),
        ),
        captured_at=datetime(
            2026,
            8,
            25,
            18,
            30,
            tzinfo=UTC,
        ),
        native_exit_code=0,
    )

    gate = GateResult(
        gate_id="pytest",
        status=ValidationStatus.PASSED,
        exit_code=0,
        testing_evidence=evidence,
    )

    checks = (
        BuildValidationCheckFactory()
        .from_testing_validation(gate)
    )

    assert len(checks) == 1

    check = checks[0]

    assert check.check_id == "release-readiness-testing"
    assert check.domain is BuildValidationDomain.TESTING
    assert check.requirement is BuildValidationRequirement.REQUIRED
    assert check.status is BuildValidationStatus.PASSED
    assert check.diagnostic is None


def test_testing_validation_maps_failed_pytest_gate_to_required_failure() -> None:
    from familyos_cli.application.validation.ci_validation import (
        GateResult,
        ValidationStatus,
    )

    gate = GateResult(
        gate_id="pytest",
        status=ValidationStatus.FAILED,
        exit_code=1,
        diagnostic="canonical pytest suite failed",
    )

    checks = (
        BuildValidationCheckFactory()
        .from_testing_validation(gate)
    )

    assert len(checks) == 1

    check = checks[0]

    assert check.check_id == "release-readiness-testing"
    assert check.domain is BuildValidationDomain.TESTING
    assert check.requirement is BuildValidationRequirement.REQUIRED
    assert check.status is BuildValidationStatus.FAILED
    assert check.diagnostic == "canonical pytest suite failed"


def test_testing_validation_maps_pytest_gate_error_to_required_failure() -> None:
    from familyos_cli.application.validation.ci_validation import (
        GateResult,
        ValidationStatus,
    )

    gate = GateResult(
        gate_id="pytest",
        status=ValidationStatus.ERROR,
        exit_code=2,
        diagnostic=(
            "pytest testing evidence freshness cannot be established"
        ),
    )

    checks = (
        BuildValidationCheckFactory()
        .from_testing_validation(gate)
    )

    assert len(checks) == 1

    check = checks[0]

    assert check.domain is BuildValidationDomain.TESTING
    assert check.requirement is BuildValidationRequirement.REQUIRED
    assert check.status is BuildValidationStatus.FAILED
    assert check.diagnostic == (
        "pytest testing evidence freshness cannot be established"
    )


def test_testing_validation_rejects_non_pytest_gate() -> None:
    import pytest

    from familyos_cli.application.validation.ci_validation import (
        GateResult,
        ValidationStatus,
    )

    gate = GateResult(
        gate_id="ruff",
        status=ValidationStatus.PASSED,
        exit_code=0,
    )

    with pytest.raises(
        ValueError,
        match="release-readiness testing requires canonical pytest gate",
    ):
        (
            BuildValidationCheckFactory()
            .from_testing_validation(gate)
        )


def test_testing_validation_requires_testing_evidence_for_passing_gate() -> None:
    import pytest

    from familyos_cli.application.validation.ci_validation import (
        GateResult,
        ValidationStatus,
    )

    gate = GateResult(
        gate_id="pytest",
        status=ValidationStatus.PASSED,
        exit_code=0,
        testing_evidence=None,
    )

    with pytest.raises(
        ValueError,
        match=(
            "release-readiness testing requires canonical "
            "Testing Evidence"
        ),
    ):
        (
            BuildValidationCheckFactory()
            .from_testing_validation(gate)
        )


def test_testing_validation_failure_does_not_require_successful_evidence() -> None:
    from familyos_cli.application.validation.ci_validation import (
        GateResult,
        ValidationStatus,
    )

    gate = GateResult(
        gate_id="pytest",
        status=ValidationStatus.FAILED,
        exit_code=1,
        diagnostic="canonical pytest suite failed",
        testing_evidence=None,
    )

    checks = (
        BuildValidationCheckFactory()
        .from_testing_validation(gate)
    )

    assert len(checks) == 1

    check = checks[0]

    assert check.domain is BuildValidationDomain.TESTING
    assert check.requirement is BuildValidationRequirement.REQUIRED
    assert check.status is BuildValidationStatus.FAILED
    assert check.diagnostic == "canonical pytest suite failed"


def test_plugin_compliance_validation_projects_passing_official_gate() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationDomain,
        BuildValidationRequirement,
        BuildValidationStatus,
    )
    from familyos_cli.application.build.build_validation_checks import (
        BuildValidationCheckFactory,
    )
    from familyos_cli.application.validation import (
        GateResult,
        PluginValidationSummary,
        ValidationStatus,
    )

    gate = GateResult(
        gate_id="builtin-plugin-compliance",
        status=ValidationStatus.PASSED,
        profile_id="official",
        plugins=(
            PluginValidationSummary(
                plugin_id="familyos.security",
                plugin_version="1.0.0",
                status="compliant",
                rule_outcomes=(),
            ),
        ),
    )

    checks = BuildValidationCheckFactory().from_plugin_compliance_validation(
        gate
    )

    assert len(checks) == 1

    check = checks[0]

    assert check.check_id == "official-plugin-compliance"
    assert check.domain is BuildValidationDomain.COMPLIANCE
    assert check.requirement is BuildValidationRequirement.REQUIRED
    assert check.status is BuildValidationStatus.PASSED
    assert check.diagnostic is None


def test_plugin_compliance_validation_projects_failed_gate() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationStatus,
    )
    from familyos_cli.application.build.build_validation_checks import (
        BuildValidationCheckFactory,
    )
    from familyos_cli.application.validation import (
        GateResult,
        PluginValidationSummary,
        ValidationStatus,
    )

    gate = GateResult(
        gate_id="builtin-plugin-compliance",
        status=ValidationStatus.FAILED,
        diagnostic="familyos.security is non-compliant",
        profile_id="official",
        plugins=(
            PluginValidationSummary(
                plugin_id="familyos.security",
                plugin_version="1.0.0",
                status="non_compliant",
                rule_outcomes=(),
            ),
        ),
    )

    check = (
        BuildValidationCheckFactory()
        .from_plugin_compliance_validation(gate)[0]
    )

    assert check.status is BuildValidationStatus.FAILED
    assert check.diagnostic == "familyos.security is non-compliant"


def test_plugin_compliance_validation_projects_error_gate() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationStatus,
    )
    from familyos_cli.application.build.build_validation_checks import (
        BuildValidationCheckFactory,
    )
    from familyos_cli.application.validation import (
        GateResult,
        ValidationStatus,
    )

    gate = GateResult(
        gate_id="builtin-plugin-compliance",
        status=ValidationStatus.ERROR,
        diagnostic="compliance evaluation failed",
        profile_id="official",
    )

    check = (
        BuildValidationCheckFactory()
        .from_plugin_compliance_validation(gate)[0]
    )

    assert check.status is BuildValidationStatus.FAILED
    assert check.diagnostic == "compliance evaluation failed"


def test_plugin_compliance_validation_rejects_noncanonical_gate() -> None:
    import pytest

    from familyos_cli.application.build.build_validation_checks import (
        BuildValidationCheckFactory,
    )
    from familyos_cli.application.validation import (
        GateResult,
        ValidationStatus,
    )

    gate = GateResult(
        gate_id="pytest",
        status=ValidationStatus.PASSED,
        profile_id="official",
    )

    with pytest.raises(
        ValueError,
        match="requires canonical builtin-plugin-compliance gate",
    ):
        BuildValidationCheckFactory().from_plugin_compliance_validation(
            gate
        )


def test_plugin_compliance_validation_rejects_nonofficial_profile() -> None:
    import pytest

    from familyos_cli.application.build.build_validation_checks import (
        BuildValidationCheckFactory,
    )
    from familyos_cli.application.validation import (
        GateResult,
        PluginValidationSummary,
        ValidationStatus,
    )

    gate = GateResult(
        gate_id="builtin-plugin-compliance",
        status=ValidationStatus.PASSED,
        profile_id="development",
        plugins=(
            PluginValidationSummary(
                plugin_id="familyos.security",
                plugin_version="1.0.0",
                status="compliant",
                rule_outcomes=(),
            ),
        ),
    )

    with pytest.raises(
        ValueError,
        match="requires canonical official profile",
    ):
        BuildValidationCheckFactory().from_plugin_compliance_validation(
            gate
        )


def test_plugin_compliance_validation_rejects_empty_success() -> None:
    import pytest

    from familyos_cli.application.build.build_validation_checks import (
        BuildValidationCheckFactory,
    )
    from familyos_cli.application.validation import (
        GateResult,
        ValidationStatus,
    )

    gate = GateResult(
        gate_id="builtin-plugin-compliance",
        status=ValidationStatus.PASSED,
        profile_id="official",
        plugins=(),
    )

    with pytest.raises(
        ValueError,
        match="successful plugin compliance requires plugin results",
    ):
        BuildValidationCheckFactory().from_plugin_compliance_validation(
            gate
        )
