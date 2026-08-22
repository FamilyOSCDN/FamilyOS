"""Tests for controlled intentional artifact mutation lifecycle."""

from __future__ import annotations

import hashlib
from pathlib import Path
from uuid import UUID

from familyos_cli.application.build.artifact_identity import ArtifactIdentity
from familyos_cli.application.build.artifact_mutation import (
    MutateArtifactUseCase,
)
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_id import BuildId

_BUILD_ID = BuildId(
    UUID("01234567-89ab-4cde-8f01-23456789abcd")
)


def _identity(path: Path) -> ArtifactIdentity:
    return ArtifactIdentity(
        logical_name="familyos-cli",
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        version="0.1.0",
        source_revision="0123456789abcdef0123456789abcdef01234567",
        build_id=_BUILD_ID,
        path=path,
        size=path.stat().st_size,
    )


def test_mutation_recalculates_digest_from_new_bytes(
    tmp_path: Path,
) -> None:
    artifact = tmp_path / "artifact.whl"
    artifact.write_bytes(b"before")

    original = _identity(artifact)

    def mutate(identity: ArtifactIdentity) -> None:
        identity.path.write_bytes(b"after!")

    result = MutateArtifactUseCase().execute(
        original,
        mutate,
    )

    assert result.integrity.digest == hashlib.sha256(
        b"after!"
    ).hexdigest()
    assert result.integrity.artifact_identity is result.identity


def test_mutation_refreshes_material_identity(
    tmp_path: Path,
) -> None:
    artifact = tmp_path / "artifact.whl"
    artifact.write_bytes(b"short")

    original = _identity(artifact)

    def mutate(identity: ArtifactIdentity) -> None:
        identity.path.write_bytes(b"longer artifact bytes")

    result = MutateArtifactUseCase().execute(
        original,
        mutate,
    )

    assert result.identity.path == original.path
    assert result.identity.logical_name == original.logical_name
    assert result.identity.artifact_type is original.artifact_type
    assert result.identity.version == original.version
    assert result.identity.source_revision == original.source_revision
    assert result.identity.build_id == original.build_id
    assert result.identity.size == len(b"longer artifact bytes")
    assert result.identity.size != original.size


def test_mutation_invalidates_previous_integrity(
    tmp_path: Path,
) -> None:
    artifact = tmp_path / "artifact.whl"
    artifact.write_bytes(b"original")

    original = _identity(artifact)

    from familyos_cli.application.build.artifact_integrity_service import (
        ArtifactIntegrityService,
    )

    service = ArtifactIntegrityService()
    previous_integrity = service.calculate(original)

    def mutate(identity: ArtifactIdentity) -> None:
        identity.path.write_bytes(b"mutated!")

    result = MutateArtifactUseCase().execute(
        original,
        mutate,
    )

    assert not service.verify(previous_integrity)
    assert service.verify(result.integrity)
    assert result.integrity.digest != previous_integrity.digest


def test_mutated_artifact_carries_no_validation_state(
    tmp_path: Path,
) -> None:
    artifact = tmp_path / "artifact.whl"
    artifact.write_bytes(b"before")

    original = _identity(artifact)

    def mutate(identity: ArtifactIdentity) -> None:
        identity.path.write_bytes(b"after!")

    result = MutateArtifactUseCase().execute(
        original,
        mutate,
    )

    for field in (
        "validated",
        "validation",
        "validation_result",
        "structural_validation",
        "functional_validation",
        "trusted",
    ):
        assert not hasattr(result, field)
        assert not hasattr(result.identity, field)
        assert not hasattr(result.integrity, field)
