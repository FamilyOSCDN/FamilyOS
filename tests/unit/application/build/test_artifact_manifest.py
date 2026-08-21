"""Tests for canonical artifact manifest generation."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

import pytest

from familyos_cli.application.build.artifact_discovery import DiscoveredArtifact
from familyos_cli.application.build.artifact_identity import ArtifactIdentity
from familyos_cli.application.build.artifact_integrity import (
    ArtifactDigestAlgorithm,
    ArtifactIntegrity,
)
from familyos_cli.application.build.artifact_manifest import ArtifactManifest
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_artifact_manifest import (
    BuildArtifactManifestUseCase,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.package_identity import PackageIdentity
from familyos_cli.application.build.package_validation import (
    CandidatePackageValidationResult,
    PackageStructuralValidationStatus,
    PythonPackageStructuralValidationResult,
)

_BUILD_ID = BuildId(UUID("01234567-89ab-4cde-8f01-23456789abcd"))
_OTHER_BUILD_ID = BuildId(UUID("11234567-89ab-4cde-8f01-23456789abcd"))


def _validated_candidate(
    path: Path,
    artifact_class: ArtifactClass,
) -> CandidatePackageValidationResult:
    return CandidatePackageValidationResult(
        candidate=DiscoveredArtifact(path, artifact_class),
        status=PackageStructuralValidationStatus.VALID,
        package_identity=PackageIdentity(
            name="familyos-cli",
            version="0.1.0",
        ),
    )


def _integrity(
    path: Path,
    artifact_class: ArtifactClass,
    *,
    build_id: BuildId = _BUILD_ID,
    digest: str,
) -> ArtifactIntegrity:
    identity = ArtifactIdentity(
        logical_name="familyos-cli",
        artifact_type=artifact_class,
        version="0.1.0",
        source_revision="0123456789abcdef0123456789abcdef01234567",
        build_id=build_id,
        path=path,
        size=path.stat().st_size,
    )
    return ArtifactIntegrity(
        artifact_identity=identity,
        algorithm=ArtifactDigestAlgorithm.SHA256,
        digest=digest,
    )


def test_manifest_records_complete_artifact_set(tmp_path: Path) -> None:
    wheel = tmp_path / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = tmp_path / "familyos_cli-0.1.0.tar.gz"
    wheel.write_bytes(b"wheel")
    sdist.write_bytes(b"sdist")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(wheel, ArtifactClass.PYTHON_WHEEL),
            _validated_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),
        ),
    )

    integrities = (
        _integrity(
            wheel,
            ArtifactClass.PYTHON_WHEEL,
            digest="a" * 64,
        ),
        _integrity(
            sdist,
            ArtifactClass.SOURCE_DISTRIBUTION,
            digest="b" * 64,
        ),
    )

    manifest = BuildArtifactManifestUseCase().execute(
        integrities,
        validation,
        build_id=_BUILD_ID,
    )

    assert isinstance(manifest, ArtifactManifest)
    assert manifest.build_id == _BUILD_ID
    assert len(manifest.entries) == 2

    wheel_entry = manifest.entries[0]
    assert wheel_entry.logical_name == "familyos-cli"
    assert wheel_entry.artifact_type is ArtifactClass.PYTHON_WHEEL
    assert wheel_entry.version == "0.1.0"
    assert wheel_entry.size == len(b"wheel")
    assert wheel_entry.path == wheel
    assert wheel_entry.digest_algorithm is ArtifactDigestAlgorithm.SHA256
    assert wheel_entry.digest == "a" * 64
    assert (
        wheel_entry.structural_validation_status
        is PackageStructuralValidationStatus.VALID
    )


def test_manifest_preserves_established_artifact_order(
    tmp_path: Path,
) -> None:
    wheel = tmp_path / "artifact.whl"
    sdist = tmp_path / "artifact.tar.gz"
    wheel.write_bytes(b"wheel")
    sdist.write_bytes(b"sdist")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(wheel, ArtifactClass.PYTHON_WHEEL),
            _validated_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),
        ),
    )

    manifest = BuildArtifactManifestUseCase().execute(
        (
            _integrity(
                wheel,
                ArtifactClass.PYTHON_WHEEL,
                digest="a" * 64,
            ),
            _integrity(
                sdist,
                ArtifactClass.SOURCE_DISTRIBUTION,
                digest="b" * 64,
            ),
        ),
        validation,
        build_id=_BUILD_ID,
    )

    assert tuple(entry.path for entry in manifest.entries) == (
        wheel,
        sdist,
    )


def test_manifest_rejects_missing_integrity(tmp_path: Path) -> None:
    wheel = tmp_path / "artifact.whl"
    sdist = tmp_path / "artifact.tar.gz"
    wheel.write_bytes(b"wheel")
    sdist.write_bytes(b"sdist")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(wheel, ArtifactClass.PYTHON_WHEEL),
            _validated_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),
        ),
    )

    with pytest.raises(ValueError, match="manifest is incomplete"):
        BuildArtifactManifestUseCase().execute(
            (
                _integrity(
                    wheel,
                    ArtifactClass.PYTHON_WHEEL,
                    digest="a" * 64,
                ),
            ),
            validation,
            build_id=_BUILD_ID,
        )


def test_manifest_rejects_integrity_without_validation(
    tmp_path: Path,
) -> None:
    wheel = tmp_path / "artifact.whl"
    unexpected = tmp_path / "unexpected.tar.gz"
    wheel.write_bytes(b"wheel")
    unexpected.write_bytes(b"unexpected")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(wheel, ArtifactClass.PYTHON_WHEEL),
        ),
    )

    with pytest.raises(
        ValueError,
        match="artifact sets differ",
    ):
        BuildArtifactManifestUseCase().execute(
            (
                _integrity(
                    unexpected,
                    ArtifactClass.SOURCE_DISTRIBUTION,
                    digest="b" * 64,
                ),
            ),
            validation,
            build_id=_BUILD_ID,
        )


def test_manifest_rejects_mismatched_build_id(tmp_path: Path) -> None:
    wheel = tmp_path / "artifact.whl"
    wheel.write_bytes(b"wheel")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(wheel, ArtifactClass.PYTHON_WHEEL),
        ),
    )

    with pytest.raises(ValueError, match="Build ID does not match"):
        BuildArtifactManifestUseCase().execute(
            (
                _integrity(
                    wheel,
                    ArtifactClass.PYTHON_WHEEL,
                    build_id=_OTHER_BUILD_ID,
                    digest="a" * 64,
                ),
            ),
            validation,
            build_id=_BUILD_ID,
        )


def test_manifest_does_not_recalculate_artifact_bytes(
    tmp_path: Path,
) -> None:
    wheel = tmp_path / "artifact.whl"
    wheel.write_bytes(b"original")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(wheel, ArtifactClass.PYTHON_WHEEL),
        ),
    )

    integrity = _integrity(
        wheel,
        ArtifactClass.PYTHON_WHEEL,
        digest="c" * 64,
    )

    wheel.write_bytes(b"mutated!")

    manifest = BuildArtifactManifestUseCase().execute(
        (integrity,),
        validation,
        build_id=_BUILD_ID,
    )

    assert manifest.entries[0].digest == "c" * 64
    assert manifest.entries[0].size == len(b"original")


def test_manifest_has_no_build_evidence_or_trust_semantics(
    tmp_path: Path,
) -> None:
    wheel = tmp_path / "artifact.whl"
    wheel.write_bytes(b"wheel")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(wheel, ArtifactClass.PYTHON_WHEEL),
        ),
    )

    manifest = BuildArtifactManifestUseCase().execute(
        (
            _integrity(
                wheel,
                ArtifactClass.PYTHON_WHEEL,
                digest="a" * 64,
            ),
        ),
        validation,
        build_id=_BUILD_ID,
    )

    for field in (
        "build_evidence",
        "trusted",
        "provenance",
        "signature",
        "published",
        "released",
    ):
        assert not hasattr(manifest, field)
        assert not hasattr(manifest.entries[0], field)


def test_manifest_rejects_duplicate_integrity_paths(
    tmp_path: Path,
) -> None:
    wheel = tmp_path / "artifact.whl"
    sdist = tmp_path / "artifact.tar.gz"
    wheel.write_bytes(b"wheel")
    sdist.write_bytes(b"sdist")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(wheel, ArtifactClass.PYTHON_WHEEL),
            _validated_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),
        ),
    )

    duplicate = _integrity(
        wheel,
        ArtifactClass.PYTHON_WHEEL,
        digest="a" * 64,
    )

    with pytest.raises(
        ValueError,
        match="duplicate artifact paths",
    ):
        BuildArtifactManifestUseCase().execute(
            (duplicate, duplicate),
            validation,
            build_id=_BUILD_ID,
        )


def test_manifest_rejects_artifact_type_mismatch(
    tmp_path: Path,
) -> None:
    wheel = tmp_path / "artifact.whl"
    wheel.write_bytes(b"wheel")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(
                wheel,
                ArtifactClass.PYTHON_WHEEL,
            ),
        ),
    )

    with pytest.raises(
        ValueError,
        match="type does not match",
    ):
        BuildArtifactManifestUseCase().execute(
            (
                _integrity(
                    wheel,
                    ArtifactClass.SOURCE_DISTRIBUTION,
                    digest="a" * 64,
                ),
            ),
            validation,
            build_id=_BUILD_ID,
        )
