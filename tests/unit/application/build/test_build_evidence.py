"""Tests for immutable canonical Build Evidence."""

from __future__ import annotations

from dataclasses import MISSING, fields, replace
from pathlib import Path
from uuid import UUID

import pytest

from familyos_cli.application.build.artifact_integrity import (
    ArtifactDigestAlgorithm,
    ArtifactIntegrity,
)
from familyos_cli.application.build.artifact_manifest import (
    ArtifactManifest,
    ArtifactManifestEntry,
)
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_context import BuildProfile, BuildTarget
from familyos_cli.application.build.build_evidence import BuildEvidence
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationProfile,
    BuildValidationResult,
    BuildValidationStatus,
)
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.effective_build_configuration_view import (
    EffectiveBuildConfigurationView,
)
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.package_validation import (
    PackageStructuralValidationStatus,
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
    declaration_digest="c" * 64,
    lock_path=Path("/project/requirements.txt"),
    lock_digest="d" * 64,
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


def _manifest() -> ArtifactManifest:
    return ArtifactManifest(
        build_id=_BUILD_ID,
        entries=(
            ArtifactManifestEntry(
                logical_name="familyos-cli",
                artifact_type=ArtifactClass.PYTHON_WHEEL,
                version="0.1.0",
                size=1024,
                path=Path(
                    "dist/familyos_cli-0.1.0-py3-none-any.whl"
                ),
                digest_algorithm=ArtifactDigestAlgorithm.SHA256,
                digest="a" * 64,
                structural_validation_status=(
                    PackageStructuralValidationStatus.VALID
                ),
            ),
        ),
    )


def _validation() -> BuildValidationResult:
    return BuildValidationResult(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.VALIDATION,
        checks=(),
        status=BuildValidationStatus.PASSED,
    )


def test_build_evidence_preserves_canonical_build_authorities() -> None:
    manifest = _manifest()

    evidence = BuildEvidence(
        build_id=_BUILD_ID,
        source_state=_SOURCE_STATE,
        dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
        effective_configuration=_EFFECTIVE_CONFIGURATION,
        validation_result=_validation(),
        artifact_manifest=manifest,
        artifact_integrities=(),
    )

    assert evidence.build_id == _BUILD_ID
    assert evidence.source_state == _SOURCE_STATE
    assert evidence.dependency_state is _DEPENDENCY_STATE
    assert evidence.effective_configuration is _EFFECTIVE_CONFIGURATION
    assert evidence.validation_result == _validation()
    assert evidence.artifact_manifest is manifest
    assert evidence.artifact_integrities == ()


def test_build_evidence_exposes_source_revision() -> None:
    evidence = BuildEvidence(
        build_id=_BUILD_ID,
        source_state=_SOURCE_STATE,
        dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
        effective_configuration=_EFFECTIVE_CONFIGURATION,
        validation_result=_validation(),
        artifact_manifest=_manifest(),
        artifact_integrities=(),
    )

    assert evidence.source_revision == _SOURCE_STATE.revision


def test_build_evidence_exposes_validation_profile() -> None:
    evidence = BuildEvidence(
        build_id=_BUILD_ID,
        source_state=_SOURCE_STATE,
        dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
        effective_configuration=_EFFECTIVE_CONFIGURATION,
        validation_result=_validation(),
        artifact_manifest=_manifest(),
        artifact_integrities=(),
    )

    assert evidence.profile is BuildValidationProfile.VALIDATION


def test_build_evidence_requires_dependency_state() -> None:
    dependency_field = next(
        field
        for field in fields(BuildEvidence)
        if field.name == "dependency_state"
    )

    assert dependency_field.default is MISSING
    assert dependency_field.default_factory is MISSING


def test_build_evidence_requires_effective_configuration() -> None:
    configuration_field = next(
        field
        for field in fields(BuildEvidence)
        if field.name == "effective_configuration"
    )

    assert configuration_field.default is MISSING
    assert configuration_field.default_factory is MISSING


def test_build_evidence_requires_matching_validation_build_id() -> None:
    validation = BuildValidationResult(
        build_id=_OTHER_BUILD_ID,
        profile=BuildValidationProfile.VALIDATION,
        checks=(),
        status=BuildValidationStatus.PASSED,
    )

    with pytest.raises(
        ValueError,
        match="validation result build ID does not match Build Evidence",
    ):
        BuildEvidence(
            build_id=_BUILD_ID,
            source_state=_SOURCE_STATE,
            dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
            effective_configuration=_EFFECTIVE_CONFIGURATION,
            validation_result=validation,
            artifact_manifest=_manifest(),
            artifact_integrities=(),
        )


def test_build_evidence_requires_matching_configuration_profile() -> None:
    configuration = replace(
        _EFFECTIVE_CONFIGURATION,
        profile=BuildProfile.CI,
        evidence_output=Path("/project/build-evidence.json"),
        evidence_required=True,
    )

    with pytest.raises(
        ValueError,
        match=(
            "effective configuration profile does not match "
            "Build Evidence validation profile"
        ),
    ):
        BuildEvidence(
            build_id=_BUILD_ID,
            source_state=_SOURCE_STATE,
            dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
            effective_configuration=configuration,
            validation_result=_validation(),
            artifact_manifest=_manifest(),
            artifact_integrities=(),
        )


def test_build_evidence_requires_matching_manifest_build_id() -> None:
    manifest = ArtifactManifest(
        build_id=_OTHER_BUILD_ID,
        entries=(),
    )

    with pytest.raises(
        ValueError,
        match="artifact manifest build ID does not match Build Evidence",
    ):
        BuildEvidence(
            build_id=_BUILD_ID,
            source_state=_SOURCE_STATE,
            dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
            effective_configuration=_EFFECTIVE_CONFIGURATION,
            validation_result=_validation(),
            artifact_manifest=manifest,
            artifact_integrities=(),
        )


def test_build_evidence_requires_captured_source_revision() -> None:
    source_state = SourceState(
        revision=None,
        dirty=False,
    )

    with pytest.raises(
        ValueError,
        match="requires a captured source revision",
    ):
        BuildEvidence(
            build_id=_BUILD_ID,
            source_state=source_state,
            dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
            effective_configuration=_EFFECTIVE_CONFIGURATION,
            validation_result=_validation(),
            artifact_manifest=_manifest(),
            artifact_integrities=(),
        )


def test_build_evidence_rejects_integrity_from_different_build() -> None:
    from familyos_cli.application.build.artifact_identity import ArtifactIdentity

    foreign_identity = ArtifactIdentity(
        build_id=_OTHER_BUILD_ID,
        source_revision=_SOURCE_STATE.revision,
        logical_name="familyos-cli",
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        version="0.1.0",
        size=1024,
        path=Path("dist/foreign.whl"),
    )

    foreign_integrity = ArtifactIntegrity(
        artifact_identity=foreign_identity,
        algorithm=ArtifactDigestAlgorithm.SHA256,
        digest="b" * 64,
    )

    with pytest.raises(
        ValueError,
        match="artifact integrity build ID does not match Build Evidence",
    ):
        BuildEvidence(
            build_id=_BUILD_ID,
            source_state=_SOURCE_STATE,
            dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
            effective_configuration=_EFFECTIVE_CONFIGURATION,
            validation_result=_validation(),
            artifact_manifest=_manifest(),
            artifact_integrities=(foreign_integrity,),
        )


def test_build_evidence_rejects_integrity_not_represented_by_manifest() -> None:
    from familyos_cli.application.build.artifact_identity import ArtifactIdentity

    identity = ArtifactIdentity(
        build_id=_BUILD_ID,
        source_revision=_SOURCE_STATE.revision,
        logical_name="familyos-cli",
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        version="0.1.0",
        size=1024,
        path=Path("dist/different.whl"),
    )

    integrity = ArtifactIntegrity(
        artifact_identity=identity,
        algorithm=ArtifactDigestAlgorithm.SHA256,
        digest="b" * 64,
    )

    with pytest.raises(
        ValueError,
        match="artifact integrity is not represented by artifact manifest",
    ):
        BuildEvidence(
            build_id=_BUILD_ID,
            source_state=_SOURCE_STATE,
            dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
            effective_configuration=_EFFECTIVE_CONFIGURATION,
            validation_result=_validation(),
            artifact_manifest=_manifest(),
            artifact_integrities=(integrity,),
        )


def test_build_evidence_exposes_captured_source_dirty_state() -> None:
    source_state = SourceState(
        revision="0123456789abcdef0123456789abcdef01234567",
        dirty=True,
    )

    evidence = BuildEvidence(
        build_id=_BUILD_ID,
        source_state=source_state,
        dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
        effective_configuration=_EFFECTIVE_CONFIGURATION,
        validation_result=_validation(),
        artifact_manifest=_manifest(),
        artifact_integrities=(),
    )

    assert evidence.source_revision == source_state.revision
    assert evidence.source_dirty is True
