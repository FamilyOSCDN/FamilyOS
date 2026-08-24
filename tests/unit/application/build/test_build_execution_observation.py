"""Tests for canonical build execution observations."""

from familyos_cli.application.build.build_execution_observation import (
    BuildExecutionObservation,
    BuildExecutionStage,
    BuildExecutionStageStatus,
)


def test_execution_stage_values_are_canonical() -> None:
    assert BuildExecutionStage.VALIDATE_INPUTS.value == "validate-inputs"
    assert (
        BuildExecutionStage.VALIDATE_REPOSITORY_LAYOUT.value
        == "validate-repository-layout"
    )
    assert BuildExecutionStage.VALIDATE_TOOLCHAIN.value == "validate-toolchain"
    assert (
        BuildExecutionStage.VALIDATE_ENVIRONMENT.value
        == "validate-environment"
    )
    assert (
        BuildExecutionStage.RESOLVE_BUILD_CONTEXT.value
        == "resolve-build-context"
    )
    assert (
        BuildExecutionStage.VALIDATE_EFFECTIVE_CONFIGURATION.value
        == "validate-effective-configuration"
    )
    assert BuildExecutionStage.PACKAGE.value == "package"
    assert (
        BuildExecutionStage.DISCOVER_ARTIFACTS.value
        == "discover-artifacts"
    )
    assert (
        BuildExecutionStage.VALIDATE_ARTIFACTS.value
        == "validate-artifacts"
    )
    assert (
        BuildExecutionStage.ESTABLISH_ARTIFACT_IDENTITY.value
        == "establish-artifact-identity"
    )
    assert (
        BuildExecutionStage.ESTABLISH_ARTIFACT_INTEGRITY.value
        == "establish-artifact-integrity"
    )
    assert (
        BuildExecutionStage.BUILD_ARTIFACT_MANIFEST.value
        == "build-artifact-manifest"
    )
    assert (
        BuildExecutionStage.FUNCTIONALLY_VALIDATE_WHEEL.value
        == "functionally-validate-wheel"
    )


def test_execution_stage_status_values_are_terminal() -> None:
    assert BuildExecutionStageStatus.SUCCEEDED.value == "succeeded"
    assert BuildExecutionStageStatus.FAILED.value == "failed"


def test_execution_observation_preserves_stage_result() -> None:
    observation = BuildExecutionObservation(
        stage=BuildExecutionStage.PACKAGE,
        status=BuildExecutionStageStatus.FAILED,
        duration_seconds=0.125,
        diagnostic="package frontend failed",
    )

    assert observation.stage is BuildExecutionStage.PACKAGE
    assert observation.status is BuildExecutionStageStatus.FAILED
    assert observation.duration_seconds == 0.125
    assert observation.diagnostic == "package frontend failed"


def test_execution_observation_defaults_to_no_diagnostic() -> None:
    observation = BuildExecutionObservation(
        stage=BuildExecutionStage.VALIDATE_INPUTS,
        status=BuildExecutionStageStatus.SUCCEEDED,
        duration_seconds=0.0,
    )

    assert observation.diagnostic is None


def test_canonical_package_build_result_defaults_to_no_execution_observations() -> None:
    from familyos_cli.application.build.artifact_discovery import (
        CanonicalPackageBuildResult,
    )
    from familyos_cli.application.build.package_build import (
        PackageBuildResult,
        PackageBuildStatus,
    )
    from familyos_cli.application.build.source_state import SourceState

    result = CanonicalPackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        execution=PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
        ),
        source_state=SourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        ),
    )

    assert result.execution_observations == ()


def test_canonical_package_build_result_preserves_execution_observations() -> None:
    from familyos_cli.application.build.artifact_discovery import (
        CanonicalPackageBuildResult,
    )
    from familyos_cli.application.build.package_build import (
        PackageBuildResult,
        PackageBuildStatus,
    )
    from familyos_cli.application.build.source_state import SourceState

    observation = BuildExecutionObservation(
        stage=BuildExecutionStage.PACKAGE,
        status=BuildExecutionStageStatus.SUCCEEDED,
        duration_seconds=0.25,
    )

    result = CanonicalPackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        execution=PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
        ),
        source_state=SourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        ),
        execution_observations=(observation,),
    )

    assert result.execution_observations == (observation,)
