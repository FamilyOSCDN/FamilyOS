"""Contracts for trusted artifact eligibility before Release handoff."""

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
        status: PackageBuildStatus = PackageBuildStatus.SUCCEEDED,
        artifact_manifest: ArtifactManifest | None,
    ) -> None:
        self.build_id = _BUILD_ID
        self.status = status
        self.artifact_manifest = artifact_manifest
        self.build_context = None
        self.diagnostic = None


def _validation_result(
    *,
    status: BuildValidationStatus = BuildValidationStatus.PASSED,
) -> BuildValidationResult:
    return BuildValidationResult(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.CI,
        checks=(),
        status=status,
    )


def _manifest() -> ArtifactManifest:
    return ArtifactManifest(
        build_id=_BUILD_ID,
        entries=(),
    )


def _canonical_result(
    *,
    execution_status: PackageBuildStatus = PackageBuildStatus.SUCCEEDED,
    validation_result: BuildValidationResult | None = None,
    artifact_manifest: ArtifactManifest | None = None,
    evidence_reference: Path | None = _EVIDENCE_REFERENCE,
) -> CanonicalBuildResult:
    if validation_result is None:
        validation_result = _validation_result()

    if artifact_manifest is None:
        artifact_manifest = _manifest()

    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(
            status=execution_status,
            artifact_manifest=artifact_manifest,
        ),
    )

    return CanonicalBuildResult(
        package_result=package_result,
        validation_result=validation_result,
        evidence_reference=evidence_reference,
    )


def test_successful_validated_build_is_release_handoff_eligible() -> None:
    result = _canonical_result()

    assert result.release_handoff_eligible


def test_build_without_validation_is_not_release_handoff_eligible() -> None:
    result = _canonical_result(
        validation_result=_validation_result(),
    )

    result = CanonicalBuildResult(
        package_result=result.package_result,
        validation_result=None,
        evidence_reference=result.evidence_reference,
    )

    assert not result.release_handoff_eligible


def test_failed_validation_is_not_release_handoff_eligible() -> None:
    result = _canonical_result(
        validation_result=_validation_result(
            status=BuildValidationStatus.FAILED,
        ),
    )

    assert not result.release_handoff_eligible


def test_build_without_manifest_is_not_release_handoff_eligible() -> None:
    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(
            artifact_manifest=None,
        ),
    )

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=_validation_result(),
        evidence_reference=_EVIDENCE_REFERENCE,
    )

    assert not result.release_handoff_eligible


def test_build_without_evidence_is_not_release_handoff_eligible() -> None:
    result = _canonical_result(
        evidence_reference=None,
    )

    assert not result.release_handoff_eligible


def test_failed_execution_is_not_release_handoff_eligible() -> None:
    result = _canonical_result(
        execution_status=PackageBuildStatus.FAILED,
    )

    assert not result.release_handoff_eligible


def test_mismatched_validation_build_id_is_not_release_handoff_eligible() -> None:
    other_build_id = BuildId(
        UUID("11234567-89ab-4cde-8f01-23456789abcd")
    )

    validation_result = BuildValidationResult(
        build_id=other_build_id,
        profile=BuildValidationProfile.CI,
        checks=(),
        status=BuildValidationStatus.PASSED,
    )

    result = _canonical_result(
        validation_result=validation_result,
    )

    assert not result.release_handoff_eligible


def test_mismatched_manifest_build_id_is_not_release_handoff_eligible() -> None:
    other_build_id = BuildId(
        UUID("11234567-89ab-4cde-8f01-23456789abcd")
    )

    manifest = ArtifactManifest(
        build_id=other_build_id,
        entries=(),
    )

    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(
            artifact_manifest=manifest,
        ),
    )

    result = CanonicalBuildResult(
        package_result=package_result,
        validation_result=_validation_result(),
        evidence_reference=_EVIDENCE_REFERENCE,
    )

    assert not result.release_handoff_eligible
