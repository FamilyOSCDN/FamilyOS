"""Contracts for downstream consumption of canonical Release handoff."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import cast
from uuid import UUID

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.artifact_manifest import (
    ArtifactManifest,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationProfile,
    BuildValidationResult,
    BuildValidationStatus,
)
from familyos_cli.application.build.canonical_build_result import (
    CanonicalBuildResult,
)
from familyos_cli.application.build.package_build import (
    PackageBuildStatus,
)
from familyos_cli.application.build.release_handoff import (
    ReleaseHandoff,
)

_BUILD_ID = BuildId(
    UUID("01234567-89ab-4cde-8f01-23456789abcd")
)

_EVIDENCE_REFERENCE = Path("/tmp/build-evidence.json")


@dataclass(frozen=True)
class _PackageResult:
    build_id: BuildId = _BUILD_ID
    status: PackageBuildStatus = PackageBuildStatus.SUCCEEDED
    artifact_manifest: ArtifactManifest | None = ArtifactManifest(
        build_id=_BUILD_ID,
        entries=(),
    )
    build_context: None = None
    diagnostic: None = None


def _canonical_result() -> CanonicalBuildResult:
    package_result = cast(
        CanonicalPackageBuildResult,
        _PackageResult(),
    )

    validation_result = BuildValidationResult(
        build_id=_BUILD_ID,
        profile=BuildValidationProfile.CI,
        checks=(),
        status=BuildValidationStatus.PASSED,
    )

    return CanonicalBuildResult(
        package_result=package_result,
        validation_result=validation_result,
        evidence_reference=_EVIDENCE_REFERENCE,
    )


def test_release_consumer_accepts_existing_handoff() -> None:
    from familyos_cli.application.build.release_handoff_consumer import (
        ReleaseHandoffConsumer,
    )

    handoff = ReleaseHandoff.from_canonical_result(
        _canonical_result()
    )

    consumed = ReleaseHandoffConsumer().consume(handoff)

    assert consumed is handoff


def test_release_consumer_preserves_all_build_authorities() -> None:
    from familyos_cli.application.build.release_handoff_consumer import (
        ReleaseHandoffConsumer,
    )

    handoff = ReleaseHandoff.from_canonical_result(
        _canonical_result()
    )

    consumed = ReleaseHandoffConsumer().consume(handoff)

    assert consumed.build_id is handoff.build_id
    assert consumed.artifact_manifest is handoff.artifact_manifest
    assert consumed.validation_result is handoff.validation_result
    assert consumed.evidence_reference is handoff.evidence_reference


def test_release_consumer_does_not_replace_artifact_paths() -> None:
    from familyos_cli.application.build.release_handoff_consumer import (
        ReleaseHandoffConsumer,
    )

    handoff = ReleaseHandoff.from_canonical_result(
        _canonical_result()
    )

    consumed = ReleaseHandoffConsumer().consume(handoff)

    assert consumed.artifact_paths == handoff.artifact_paths
