"""Tests for canonical Build Evidence construction."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

import pytest

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.artifact_manifest import ArtifactManifest
from familyos_cli.application.build.build_context import (
    BuildContext,
    BuildEffectiveConfiguration,
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.build_evidence_factory import (
    BuildEvidenceFactory,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationProfile,
    BuildValidationResult,
    BuildValidationStatus,
)
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.package_build import (
    PackageBuildResult,
    PackageBuildStatus,
)
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)

_BUILD_ID = BuildId(
    UUID("01234567-89ab-4cde-8f01-23456789abcd")
)

_OTHER_BUILD_ID = BuildId(
    UUID("11234567-89ab-4cde-8f01-23456789abcd")
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


def _build_context() -> BuildContext:
    return BuildContext(
        build_id=_BUILD_ID,
        source_state=_SOURCE_STATE,
        dependency_state=_DEPENDENCY_STATE,
        toolchain_state=ToolchainState(
            critical_versions=(ToolchainVersion("build", "1.5.0"),),
        ),
        environment_state=EnvironmentState(
            operating_system="Darwin",
            operating_system_release="24.6.0",
            machine_architecture="arm64",
        ),
        profile=BuildProfile.VALIDATION,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
        runtime_version="3.13.7",
        effective_configuration=BuildEffectiveConfiguration(
            functional_validation=False,
        ),
        output_dir=Path("/project/dist"),
    )


def _package_result() -> CanonicalPackageBuildResult:
    return CanonicalPackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        execution=PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
            outputs=(Path("dist/familyos_cli-0.1.0-py3-none-any.whl"),),
        ),
        source_state=_SOURCE_STATE,
        build_context=_build_context(),
        build_id=_BUILD_ID,
        artifact_integrities=(),
        artifact_manifest=ArtifactManifest(
            build_id=_BUILD_ID,
            entries=(),
        ),
    )


def _validation_result(
    *,
    build_id: BuildId = _BUILD_ID,
) -> BuildValidationResult:
    return BuildValidationResult(
        build_id=build_id,
        profile=BuildValidationProfile.VALIDATION,
        checks=(),
        status=BuildValidationStatus.PASSED,
    )


def test_factory_preserves_canonical_package_build_authorities() -> None:
    package_result = _package_result()
    validation_result = _validation_result()

    evidence = BuildEvidenceFactory().from_package_build(
        package_result,
        validation_result,
    )

    assert evidence.build_id == package_result.build_id
    assert evidence.source_state is package_result.source_state
    assert package_result.build_context is not None
    assert (
        evidence.dependency_state
        is package_result.build_context.dependency_state
    )
    assert evidence.effective_configuration.profile is BuildProfile.VALIDATION
    assert (
        evidence.effective_configuration.target
        is BuildTarget.FAMILYOS_CLI_PACKAGE
    )
    assert evidence.effective_configuration.output_dir == Path("/project/dist")
    assert evidence.effective_configuration.functional_validation is False
    assert evidence.effective_configuration.evidence_requested is False
    assert evidence.effective_configuration.evidence_required is False
    assert evidence.effective_configuration.target_supported is True
    assert evidence.validation_result is validation_result
    assert evidence.artifact_manifest is package_result.artifact_manifest
    assert evidence.artifact_integrities is package_result.artifact_integrities


def test_factory_preserves_validation_profile() -> None:
    evidence = BuildEvidenceFactory().from_package_build(
        _package_result(),
        _validation_result(),
    )

    assert evidence.profile is BuildValidationProfile.VALIDATION


def test_factory_requires_build_context() -> None:
    package_result = _package_result()

    package_result = CanonicalPackageBuildResult(
        status=package_result.status,
        execution=package_result.execution,
        source_state=package_result.source_state,
        build_id=package_result.build_id,
        artifact_integrities=package_result.artifact_integrities,
        artifact_manifest=package_result.artifact_manifest,
    )

    with pytest.raises(
        ValueError,
        match="package build does not contain Build Context",
    ):
        BuildEvidenceFactory().from_package_build(
            package_result,
            _validation_result(),
        )


def test_factory_rejects_mismatched_validation_build_id() -> None:
    with pytest.raises(
        ValueError,
        match="validation result build ID does not match package build",
    ):
        BuildEvidenceFactory().from_package_build(
            _package_result(),
            _validation_result(build_id=_OTHER_BUILD_ID),
        )


def test_factory_requires_artifact_manifest() -> None:
    package_result = _package_result()

    package_result = CanonicalPackageBuildResult(
        status=package_result.status,
        execution=package_result.execution,
        source_state=package_result.source_state,
        build_context=package_result.build_context,
        build_id=package_result.build_id,
        artifact_integrities=package_result.artifact_integrities,
    )

    with pytest.raises(
        ValueError,
        match="package build does not contain an artifact manifest",
    ):
        BuildEvidenceFactory().from_package_build(
            package_result,
            _validation_result(),
        )


def test_factory_requires_captured_source_revision() -> None:
    package_result = _package_result()

    package_result = CanonicalPackageBuildResult(
        status=package_result.status,
        execution=package_result.execution,
        source_state=SourceState(
            revision=None,
            dirty=False,
        ),
        build_context=package_result.build_context,
        build_id=package_result.build_id,
        artifact_integrities=package_result.artifact_integrities,
        artifact_manifest=package_result.artifact_manifest,
    )

    with pytest.raises(
        ValueError,
        match="package build does not contain a captured source revision",
    ):
        BuildEvidenceFactory().from_package_build(
            package_result,
            _validation_result(),
        )


def test_factory_preserves_toolchain_and_environment_authorities() -> None:
    package_result = _package_result()

    evidence = BuildEvidenceFactory().from_package_build(
        package_result,
        _validation_result(),
    )

    assert package_result.build_context is not None
    assert (
        evidence.toolchain_state
        is package_result.build_context.toolchain_state
    )
    assert (
        evidence.environment_state
        is package_result.build_context.environment_state
    )
