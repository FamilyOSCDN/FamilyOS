"""Tests for canonical artifact integrity."""

from __future__ import annotations

import hashlib
from pathlib import Path
from uuid import UUID

from familyos_cli.application.build import (
    ArtifactClass,
    ArtifactDigestAlgorithm,
    ArtifactIdentity,
    ArtifactIntegrityService,
    BuildArtifactIntegritiesUseCase,
    BuildId,
)

_BUILD_ID = BuildId(UUID("01234567-89ab-4cde-8f01-23456789abcd"))


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


def test_calculate_uses_sha256_of_final_bytes(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.whl"
    artifact.write_bytes(b"final artifact bytes")

    integrity = ArtifactIntegrityService().calculate(_identity(artifact))

    assert integrity.algorithm is ArtifactDigestAlgorithm.SHA256
    assert integrity.digest == hashlib.sha256(
        b"final artifact bytes"
    ).hexdigest()
    assert len(integrity.digest) == 64


def test_verify_accepts_unchanged_artifact(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.whl"
    artifact.write_bytes(b"unchanged")

    service = ArtifactIntegrityService()
    integrity = service.calculate(_identity(artifact))

    assert service.verify(integrity)


def test_verify_rejects_same_size_byte_mutation(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.whl"
    artifact.write_bytes(b"original")

    service = ArtifactIntegrityService()
    integrity = service.calculate(_identity(artifact))

    artifact.write_bytes(b"mutated!")

    assert artifact.stat().st_size == integrity.artifact_identity.size
    assert not service.verify(integrity)


def test_verify_rejects_size_changing_mutation(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.whl"
    artifact.write_bytes(b"original")

    service = ArtifactIntegrityService()
    integrity = service.calculate(_identity(artifact))

    artifact.write_bytes(b"changed-size")

    assert not service.verify(integrity)


def test_recalculation_after_mutation_produces_new_digest(
    tmp_path: Path,
) -> None:
    artifact = tmp_path / "artifact.whl"
    artifact.write_bytes(b"before")

    service = ArtifactIntegrityService()
    first_identity = _identity(artifact)
    first = service.calculate(first_identity)

    artifact.write_bytes(b"after!")

    second_identity = _identity(artifact)
    second = service.calculate(second_identity)

    assert first.digest != second.digest
    assert not service.verify(first)
    assert service.verify(second)


def test_missing_artifact_fails_integrity_verification(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.whl"
    artifact.write_bytes(b"content")

    service = ArtifactIntegrityService()
    integrity = service.calculate(_identity(artifact))

    artifact.unlink()

    assert not service.verify(integrity)


def test_integrity_builder_preserves_identity_order(tmp_path: Path) -> None:
    wheel = tmp_path / "artifact.whl"
    sdist = tmp_path / "artifact.tar.gz"
    wheel.write_bytes(b"wheel")
    sdist.write_bytes(b"sdist")

    wheel_identity = ArtifactIdentity(
        logical_name="familyos-cli",
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        version="0.1.0",
        source_revision=None,
        build_id=_BUILD_ID,
        path=wheel,
        size=wheel.stat().st_size,
    )
    sdist_identity = ArtifactIdentity(
        logical_name="familyos-cli",
        artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
        version="0.1.0",
        source_revision=None,
        build_id=_BUILD_ID,
        path=sdist,
        size=sdist.stat().st_size,
    )

    integrities = BuildArtifactIntegritiesUseCase().execute(
        (wheel_identity, sdist_identity)
    )

    assert tuple(
        integrity.artifact_identity
        for integrity in integrities
    ) == (wheel_identity, sdist_identity)


def test_artifact_identity_remains_integrity_neutral(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.whl"
    artifact.write_bytes(b"content")

    identity = _identity(artifact)

    for field in (
        "digest",
        "digest_algorithm",
        "integrity",
        "trusted",
        "verified",
    ):
        assert not hasattr(identity, field)
