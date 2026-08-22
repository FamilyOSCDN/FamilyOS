"""Tests for artifact integrity verification after artifact transfer."""

from __future__ import annotations

import shutil
from pathlib import Path
from uuid import UUID

from familyos_cli.application.build.artifact_identity import ArtifactIdentity
from familyos_cli.application.build.artifact_integrity import (
    ArtifactDigestAlgorithm,
    ArtifactIntegrity,
)
from familyos_cli.application.build.artifact_integrity_service import (
    ArtifactIntegrityService,
)
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.verify_artifact_integrities import (
    VerifyArtifactIntegritiesUseCase,
)

_BUILD_ID = BuildId(UUID("01234567-89ab-4cde-8f01-23456789abcd"))


def _integrity(path: Path) -> ArtifactIntegrity:
    identity = ArtifactIdentity(
        logical_name="familyos-cli",
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        version="0.1.0",
        source_revision="0123456789abcdef0123456789abcdef01234567",
        build_id=_BUILD_ID,
        path=path,
        size=path.stat().st_size,
    )
    return ArtifactIntegrityService().calculate(identity)


def _transferred_integrity(
    integrity: ArtifactIntegrity,
    transferred_path: Path,
) -> ArtifactIntegrity:
    identity = integrity.artifact_identity
    transferred_identity = ArtifactIdentity(
        logical_name=identity.logical_name,
        artifact_type=identity.artifact_type,
        version=identity.version,
        source_revision=identity.source_revision,
        build_id=identity.build_id,
        path=transferred_path,
        size=identity.size,
    )
    return ArtifactIntegrity(
        artifact_identity=transferred_identity,
        algorithm=ArtifactDigestAlgorithm.SHA256,
        digest=integrity.digest,
    )


def test_verifies_unchanged_artifact_after_transfer(tmp_path: Path) -> None:
    source = tmp_path / "source" / "artifact.whl"
    transferred = tmp_path / "stage-two" / "artifact.whl"
    source.parent.mkdir()
    transferred.parent.mkdir()
    source.write_bytes(b"canonical artifact bytes")

    recorded = _integrity(source)
    shutil.copyfile(source, transferred)

    result = VerifyArtifactIntegritiesUseCase().execute(
        (_transferred_integrity(recorded, transferred),)
    )

    assert result.successful
    assert len(result.verifications) == 1
    assert result.verifications[0].successful


def test_rejects_byte_mutation_after_transfer(tmp_path: Path) -> None:
    source = tmp_path / "source" / "artifact.whl"
    transferred = tmp_path / "stage-two" / "artifact.whl"
    source.parent.mkdir()
    transferred.parent.mkdir()
    source.write_bytes(b"original")

    recorded = _integrity(source)
    shutil.copyfile(source, transferred)
    transferred.write_bytes(b"mutated!")

    assert transferred.stat().st_size == source.stat().st_size

    result = VerifyArtifactIntegritiesUseCase().execute(
        (_transferred_integrity(recorded, transferred),)
    )

    assert not result.successful
    assert not result.verifications[0].successful


def test_rejects_missing_artifact_after_transfer(tmp_path: Path) -> None:
    source = tmp_path / "source" / "artifact.whl"
    transferred = tmp_path / "stage-two" / "artifact.whl"
    source.parent.mkdir()
    transferred.parent.mkdir()
    source.write_bytes(b"canonical artifact bytes")

    recorded = _integrity(source)

    result = VerifyArtifactIntegritiesUseCase().execute(
        (_transferred_integrity(recorded, transferred),)
    )

    assert not result.successful
    assert not result.verifications[0].successful


def test_requires_nonempty_integrity_set() -> None:
    result = VerifyArtifactIntegritiesUseCase().execute(())

    assert not result.successful
