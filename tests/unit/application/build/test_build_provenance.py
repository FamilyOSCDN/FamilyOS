"""Tests for canonical Build Provenance."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

import pytest

from familyos_cli.application.build.artifact_identity import ArtifactIdentity
from familyos_cli.application.build.artifact_integrity import (
    ArtifactDigestAlgorithm,
    ArtifactIntegrity,
)
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_context_fingerprint import (
    BuildContextFingerprint,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_provenance import BuildProvenance
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)

_BUILD_ID = BuildId(UUID("01234567-89ab-4cde-8f01-23456789abcd"))
_OTHER_BUILD_ID = BuildId(UUID("11234567-89ab-4cde-8f01-23456789abcd"))
_SOURCE_REVISION = "0123456789abcdef0123456789abcdef01234567"
_OTHER_REVISION = "fedcba9876543210fedcba9876543210fedcba98"

_DEPENDENCY_STATE = DependencyState(
    declaration_path=Path("/project/pyproject.toml"),
    declaration_digest="c" * 64,
    lock_path=Path("/project/requirements.txt"),
    lock_digest="d" * 64,
)

_TOOLCHAIN_STATE = ToolchainState(
    critical_versions=(ToolchainVersion("build", "1.5.0"),),
)

_ENVIRONMENT_STATE = EnvironmentState(
    operating_system="Linux",
    operating_system_release="6.8",
    machine_architecture="x86_64",
)


def _integrity(
    *,
    artifact_type: ArtifactClass = ArtifactClass.PYTHON_WHEEL,
    build_id: BuildId = _BUILD_ID,
    source_revision: str | None = _SOURCE_REVISION,
) -> ArtifactIntegrity:
    suffix = ".whl" if artifact_type is ArtifactClass.PYTHON_WHEEL else ".tar.gz"

    identity = ArtifactIdentity(
        logical_name="familyos-cli",
        artifact_type=artifact_type,
        version="0.1.0",
        source_revision=source_revision,
        build_id=build_id,
        path=Path(f"/tmp/familyos_cli-0.1.0{suffix}"),
        size=100,
    )

    return ArtifactIntegrity(
        artifact_identity=identity,
        algorithm=ArtifactDigestAlgorithm.SHA256,
        digest="a" * 64,
    )


def _provenance(
    *,
    source_state: SourceState | None = None,
    artifact_integrities: tuple[ArtifactIntegrity, ...] | None = None,
) -> BuildProvenance:
    return BuildProvenance(
        build_id=_BUILD_ID,
        build_context_fingerprint=BuildContextFingerprint(
            algorithm="sha256",
            digest="b" * 64,
        ),
        source_state=(
            source_state
            if source_state is not None
            else SourceState(
                revision=_SOURCE_REVISION,
                dirty=False,
            )
        ),
        dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
        artifact_integrities=(
            artifact_integrities
            if artifact_integrities is not None
            else (_integrity(),)
        ),
    )


def test_provenance_preserves_canonical_relationship() -> None:
    provenance = _provenance()

    assert provenance.build_id == _BUILD_ID
    assert provenance.build_context_fingerprint.algorithm == "sha256"
    assert provenance.source_state.revision == _SOURCE_REVISION
    assert provenance.dependency_state is _DEPENDENCY_STATE
    assert provenance.toolchain_state is _TOOLCHAIN_STATE
    assert provenance.environment_state is _ENVIRONMENT_STATE
    assert len(provenance.artifact_integrities) == 1


def test_provenance_requires_source_revision() -> None:
    with pytest.raises(
        ValueError,
        match="requires a captured source revision",
    ):
        _provenance(
            source_state=SourceState(
                revision=None,
                dirty=False,
            )
        )


def test_provenance_requires_artifact_integrities() -> None:
    with pytest.raises(
        ValueError,
        match="requires artifact integrity records",
    ):
        _provenance(artifact_integrities=())


def test_provenance_rejects_different_artifact_build_id() -> None:
    with pytest.raises(
        ValueError,
        match="build ID does not match",
    ):
        _provenance(artifact_integrities=(_integrity(build_id=_OTHER_BUILD_ID),))


def test_provenance_rejects_different_artifact_source_revision() -> None:
    with pytest.raises(
        ValueError,
        match="source revision does not match",
    ):
        _provenance(artifact_integrities=(_integrity(source_revision=_OTHER_REVISION),))


def test_provenance_rejects_unknown_artifact_source_revision() -> None:
    with pytest.raises(
        ValueError,
        match="source revision does not match",
    ):
        _provenance(artifact_integrities=(_integrity(source_revision=None),))


def test_provenance_accepts_distinct_canonical_artifact_types() -> None:
    provenance = _provenance(
        artifact_integrities=(
            _integrity(
                artifact_type=ArtifactClass.PYTHON_WHEEL,
            ),
            _integrity(
                artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
            ),
        )
    )

    assert tuple(
        integrity.artifact_identity.artifact_type
        for integrity in provenance.artifact_integrities
    ) == (
        ArtifactClass.PYTHON_WHEEL,
        ArtifactClass.SOURCE_DISTRIBUTION,
    )


def test_provenance_rejects_duplicate_artifact_types() -> None:
    with pytest.raises(
        ValueError,
        match="artifact types must be unique",
    ):
        _provenance(
            artifact_integrities=(
                _integrity(),
                _integrity(),
            )
        )


def test_provenance_contains_no_trust_or_attestation_claims() -> None:
    provenance = _provenance()

    for field in (
        "trusted",
        "verified",
        "signed",
        "signature",
        "attestation",
        "slsa",
        "builder_identity",
        "runner_identity",
    ):
        assert not hasattr(provenance, field)
