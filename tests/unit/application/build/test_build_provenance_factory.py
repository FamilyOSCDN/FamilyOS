"""Tests for Build Provenance construction from Build Evidence."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

from familyos_cli.application.build.artifact_identity import ArtifactIdentity
from familyos_cli.application.build.artifact_integrity import (
    ArtifactDigestAlgorithm,
    ArtifactIntegrity,
)
from familyos_cli.application.build.artifact_manifest import (
    ArtifactManifest,
    ArtifactManifestEntry,
)
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_context import (
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.build_context_fingerprint import (
    BuildContextFingerprint,
)
from familyos_cli.application.build.build_evidence import BuildEvidence
from familyos_cli.application.build.build_execution_observation import (
    BuildExecutionObservation,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_provenance_factory import (
    BuildProvenanceFactory,
)
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

_BUILD_ID = BuildId(UUID("01234567-89ab-4cde-8f01-23456789abcd"))
_SOURCE_STATE = SourceState(
    revision="0123456789abcdef0123456789abcdef01234567",
    dirty=False,
)
_FINGERPRINT = BuildContextFingerprint(
    algorithm="sha256",
    digest="f" * 64,
)
_ARTIFACT_PATH = Path("dist/familyos_cli-0.1.0-py3-none-any.whl")

_IDENTITY = ArtifactIdentity(
    logical_name="familyos-cli",
    artifact_type=ArtifactClass.PYTHON_WHEEL,
    version="0.1.0",
    source_revision=_SOURCE_STATE.revision,
    build_id=_BUILD_ID,
    path=_ARTIFACT_PATH,
    size=1024,
)

_INTEGRITY = ArtifactIntegrity(
    artifact_identity=_IDENTITY,
    algorithm=ArtifactDigestAlgorithm.SHA256,
    digest="a" * 64,
)

_MANIFEST = ArtifactManifest(
    build_id=_BUILD_ID,
    entries=(
        ArtifactManifestEntry(
            logical_name="familyos-cli",
            artifact_type=ArtifactClass.PYTHON_WHEEL,
            version="0.1.0",
            size=1024,
            path=_ARTIFACT_PATH,
            digest_algorithm=ArtifactDigestAlgorithm.SHA256,
            digest="a" * 64,
            structural_validation_status=(PackageStructuralValidationStatus.VALID),
        ),
    ),
)


def _evidence() -> BuildEvidence:
    return BuildEvidence(
        build_id=_BUILD_ID,
        build_context_fingerprint=_FINGERPRINT,
        source_state=_SOURCE_STATE,
        runtime_version="3.13.7",
        dependency_state=DependencyState(
            declaration_path=Path("/project/pyproject.toml"),
            declaration_digest="b" * 64,
            lock_path=Path("/project/requirements.txt"),
            lock_digest="c" * 64,
        ),
        toolchain_state=ToolchainState(
            critical_versions=(ToolchainVersion("build", "1.5.0"),),
        ),
        environment_state=EnvironmentState(
            operating_system="Linux",
            operating_system_release="6.8",
            machine_architecture="x86_64",
        ),
        effective_configuration=EffectiveBuildConfigurationView(
            profile=BuildProfile.VALIDATION,
            target=BuildTarget.FAMILYOS_CLI_PACKAGE,
            output_dir=Path("/project/dist"),
            functional_validation=False,
            evidence_output=None,
            evidence_required=False,
            target_supported=True,
        ),
        execution_observations=tuple[BuildExecutionObservation, ...](),
        validation_result=BuildValidationResult(
            build_id=_BUILD_ID,
            profile=BuildValidationProfile.VALIDATION,
            checks=(),
            status=BuildValidationStatus.PASSED,
        ),
        artifact_manifest=_MANIFEST,
        artifact_integrities=(_INTEGRITY,),
    )


def test_factory_projects_canonical_provenance() -> None:
    evidence = _evidence()

    provenance = BuildProvenanceFactory().from_build_evidence(evidence)

    assert provenance.build_id is evidence.build_id
    assert provenance.build_context_fingerprint is evidence.build_context_fingerprint
    assert provenance.source_state is evidence.source_state
    assert provenance.dependency_state is evidence.dependency_state
    assert provenance.toolchain_state is evidence.toolchain_state
    assert provenance.environment_state is evidence.environment_state
    assert provenance.artifact_integrities is evidence.artifact_integrities


def test_factory_does_not_recalculate_or_copy_authorities() -> None:
    evidence = _evidence()

    provenance = BuildProvenanceFactory().from_build_evidence(evidence)

    assert provenance.build_context_fingerprint is _FINGERPRINT
    assert provenance.source_state is _SOURCE_STATE
    assert provenance.dependency_state is evidence.dependency_state
    assert provenance.toolchain_state is evidence.toolchain_state
    assert provenance.environment_state is evidence.environment_state
    assert provenance.artifact_integrities == (_INTEGRITY,)


def test_factory_preserves_artifact_digest_authority() -> None:
    provenance = BuildProvenanceFactory().from_build_evidence(_evidence())

    integrity = provenance.artifact_integrities[0]

    assert integrity.algorithm is ArtifactDigestAlgorithm.SHA256
    assert integrity.digest == "a" * 64
