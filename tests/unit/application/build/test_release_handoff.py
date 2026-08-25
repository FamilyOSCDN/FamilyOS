"""Contracts for explicit Build-to-Release handoff representation."""

from __future__ import annotations

from pathlib import Path
from typing import cast
from uuid import UUID

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.artifact_manifest import ArtifactManifest
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationProfile,
    BuildValidationResult,
    BuildValidationStatus,
)
from familyos_cli.application.build.canonical_build_result import (
    CanonicalBuildResult,
)
from familyos_cli.application.build.package_build import PackageBuildStatus

_BUILD_ID = BuildId(
    UUID("01234567-89ab-4cde-8f01-23456789abcd")
)

_EVIDENCE_REFERENCE = Path("/tmp/build-evidence.json")


class _PackageResult:
    def __init__(
        self,
        *,
        artifact_manifest: ArtifactManifest,
    ) -> None:
        self.build_id = _BUILD_ID
        self.status = PackageBuildStatus.SUCCEEDED
        self.artifact_manifest = artifact_manifest
        self.build_context = None
        self.diagnostic = None


def _validation_result() -> BuildValidationResult:
    return BuildValidationResult(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.CI,
        checks=(),
        status=BuildValidationStatus.PASSED,
    )


def _manifest() -> ArtifactManifest:
    return ArtifactManifest(
        build_id=_BUILD_ID,
        entries=(),
    )


def _canonical_result() -> CanonicalBuildResult:
    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(
            artifact_manifest=_manifest(),
        ),
    )

    return CanonicalBuildResult(
        package_result=package_result,
        validation_result=_validation_result(),
        evidence_reference=_EVIDENCE_REFERENCE,
    )


def test_release_handoff_preserves_established_authorities() -> None:
    from familyos_cli.application.build.release_handoff import (
        ReleaseHandoff,
    )

    result = _canonical_result()

    handoff = ReleaseHandoff.from_canonical_result(result)

    assert handoff.build_id is result.build_id
    assert handoff.artifact_manifest is result.artifact_manifest
    assert handoff.validation_result is result.validation_result
    assert handoff.evidence_reference is result.evidence_reference


def test_release_handoff_requires_eligible_build_result() -> None:
    from familyos_cli.application.build.release_handoff import (
        ReleaseHandoff,
    )

    result = CanonicalBuildResult(
        package_result=_canonical_result().package_result,
        validation_result=None,
        evidence_reference=_EVIDENCE_REFERENCE,
    )

    try:
        ReleaseHandoff.from_canonical_result(result)
    except ValueError as exc:
        assert "eligible" in str(exc).lower()
    else:
        raise AssertionError(
            "ineligible CanonicalBuildResult accepted for Release handoff"
        )


def test_release_handoff_does_not_recalculate_authorities() -> None:
    from familyos_cli.application.build.release_handoff import (
        ReleaseHandoff,
    )

    result = _canonical_result()

    handoff = ReleaseHandoff.from_canonical_result(result)

    assert handoff.artifact_manifest is result.artifact_manifest
    assert handoff.validation_result is result.validation_result
    assert handoff.evidence_reference is result.evidence_reference


def test_release_handoff_exposes_existing_artifact_paths() -> None:
    from familyos_cli.application.build.release_handoff import (
        ReleaseHandoff,
    )

    result = _canonical_result()

    handoff = ReleaseHandoff.from_canonical_result(result)

    assert handoff.artifact_paths == tuple(
        entry.path
        for entry in handoff.artifact_manifest.entries
    )


def test_release_handoff_artifact_paths_are_derived_from_manifest() -> None:
    from familyos_cli.application.build.release_handoff import (
        ReleaseHandoff,
    )

    result = _canonical_result()

    handoff = ReleaseHandoff.from_canonical_result(result)

    expected_paths = tuple(
        entry.path
        for entry in handoff.artifact_manifest.entries
    )

    assert isinstance(handoff.artifact_paths, tuple)
    assert handoff.artifact_paths == expected_paths


def test_release_handoff_does_not_create_replacement_artifact_paths() -> None:
    from familyos_cli.application.build.release_handoff import (
        ReleaseHandoff,
    )

    result = _canonical_result()

    handoff = ReleaseHandoff.from_canonical_result(result)

    for artifact_path in handoff.artifact_paths:
        assert artifact_path.parent.name == "dist"

def test_release_handoff_exposes_canonical_artifact_digests() -> None:
    from familyos_cli.application.build.release_handoff import (
        ReleaseHandoff,
    )

    result = _canonical_result()

    handoff = ReleaseHandoff.from_canonical_result(result)

    assert handoff.artifact_digests == tuple(
        (
            entry.path,
            entry.digest_algorithm,
            entry.digest,
        )
        for entry in handoff.artifact_manifest.entries
    )


def test_release_handoff_artifact_digests_are_derived_from_manifest() -> None:
    from familyos_cli.application.build.release_handoff import (
        ReleaseHandoff,
    )

    result = _canonical_result()

    handoff = ReleaseHandoff.from_canonical_result(result)

    expected = tuple(
        (
            entry.path,
            entry.digest_algorithm,
            entry.digest,
        )
        for entry in handoff.artifact_manifest.entries
    )

    assert handoff.artifact_digests == expected


def test_release_handoff_does_not_recalculate_artifact_digests() -> None:
    from familyos_cli.application.build.release_handoff import (
        ReleaseHandoff,
    )

    result = _canonical_result()

    handoff = ReleaseHandoff.from_canonical_result(result)

    for projected, entry in zip(
        handoff.artifact_digests,
        handoff.artifact_manifest.entries,
        strict=True,
    ):
        path, algorithm, digest = projected

        assert path is entry.path
        assert algorithm is entry.digest_algorithm
        assert digest is entry.digest
