"""Tests for minimal artifact identity metadata."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

from familyos_cli.application.build import (
    ArtifactClass,
    BuildArtifactIdentitiesUseCase,
    BuildId,
    CandidatePackageValidationResult,
    DiscoveredArtifact,
    PackageIdentity,
    PackageStructuralValidationStatus,
    PythonPackageStructuralValidationResult,
)

_BUILD_ID = BuildId(UUID("01234567-89ab-4cde-8f01-23456789abcd"))
_SOURCE_REVISION = "0123456789abcdef0123456789abcdef01234567"


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


def test_identity_records_validated_package_and_execution_context(
    tmp_path: Path,
) -> None:
    wheel = tmp_path / "familyos_cli-0.1.0-py3-none-any.whl"
    wheel.write_bytes(b"wheel-bytes")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(wheel, ArtifactClass.PYTHON_WHEEL),
        ),
    )

    identities = BuildArtifactIdentitiesUseCase().execute(
        validation,
        build_id=_BUILD_ID,
        source_revision=_SOURCE_REVISION,
    )

    assert len(identities) == 1
    identity = identities[0]
    assert identity.logical_name == "familyos-cli"
    assert identity.artifact_type is ArtifactClass.PYTHON_WHEEL
    assert identity.version == "0.1.0"
    assert identity.source_revision == _SOURCE_REVISION
    assert identity.build_id == _BUILD_ID
    assert identity.path == wheel
    assert identity.size == len(b"wheel-bytes")


def test_identity_allows_unknown_source_revision(tmp_path: Path) -> None:
    sdist = tmp_path / "familyos_cli-0.1.0.tar.gz"
    sdist.write_bytes(b"sdist")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),
        ),
    )

    identities = BuildArtifactIdentitiesUseCase().execute(
        validation,
        build_id=_BUILD_ID,
        source_revision=None,
    )

    assert identities[0].source_revision is None


def test_invalid_candidate_does_not_receive_artifact_identity(
    tmp_path: Path,
) -> None:
    wheel = tmp_path / "broken.whl"
    wheel.write_bytes(b"broken")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.INVALID,
        candidate_results=(
            CandidatePackageValidationResult(
                candidate=DiscoveredArtifact(
                    wheel,
                    ArtifactClass.PYTHON_WHEEL,
                ),
                status=PackageStructuralValidationStatus.INVALID,
                diagnostics=("wheel is corrupt",),
            ),
        ),
    )

    identities = BuildArtifactIdentitiesUseCase().execute(
        validation,
        build_id=_BUILD_ID,
        source_revision=_SOURCE_REVISION,
    )

    assert identities == ()


def test_identity_order_is_deterministic(tmp_path: Path) -> None:
    wheel = tmp_path / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = tmp_path / "familyos_cli-0.1.0.tar.gz"
    wheel.write_bytes(b"wheel")
    sdist.write_bytes(b"sdist")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),
            _validated_candidate(wheel, ArtifactClass.PYTHON_WHEEL),
        ),
    )

    identities = BuildArtifactIdentitiesUseCase().execute(
        validation,
        build_id=_BUILD_ID,
        source_revision=_SOURCE_REVISION,
    )

    assert tuple(identity.artifact_type for identity in identities) == (
        ArtifactClass.PYTHON_WHEEL,
        ArtifactClass.SOURCE_DISTRIBUTION,
    )


def test_identity_contains_no_integrity_or_trust_fields(tmp_path: Path) -> None:
    wheel = tmp_path / "familyos_cli-0.1.0-py3-none-any.whl"
    wheel.write_bytes(b"wheel")

    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=(
            _validated_candidate(wheel, ArtifactClass.PYTHON_WHEEL),
        ),
    )

    identity = BuildArtifactIdentitiesUseCase().execute(
        validation,
        build_id=_BUILD_ID,
        source_revision=_SOURCE_REVISION,
    )[0]

    for field in (
        "digest",
        "trusted",
        "verified",
        "provenance",
        "validation_status",
        "manifest",
    ):
        assert not hasattr(identity, field)
