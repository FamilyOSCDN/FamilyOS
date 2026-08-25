"""Explicit Build-to-Release handoff of established authorities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from familyos_cli.application.build.artifact_manifest import ArtifactManifest
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationResult,
)
from familyos_cli.application.build.canonical_build_result import (
    CanonicalBuildResult,
)


@dataclass(frozen=True, slots=True)
class ReleaseHandoff:
    """Preserve trusted Build authorities for downstream Release evaluation."""

    build_id: BuildId
    artifact_manifest: ArtifactManifest
    validation_result: BuildValidationResult
    evidence_reference: Path

    @property
    def artifact_paths(self) -> tuple[Path, ...]:
        """Return the exact artifact paths established by the manifest."""

        return tuple(
            entry.path
            for entry in self.artifact_manifest.entries
        )

    @property
    def artifact_digests(
        self,
    ) -> tuple[tuple[Path, str, str], ...]:
        """Return artifact digest authorities established by the manifest."""

        return tuple(
            (
                entry.path,
                entry.digest_algorithm,
                entry.digest,
            )
            for entry in self.artifact_manifest.entries
        )

    @classmethod
    def from_canonical_result(
        cls,
        result: CanonicalBuildResult,
    ) -> ReleaseHandoff:
        """Create a handoff only from an eligible canonical Build Result."""

        if not result.release_handoff_eligible:
            raise ValueError(
                "Canonical Build Result is not eligible for Release handoff"
            )

        artifact_manifest = result.artifact_manifest
        validation_result = result.validation_result
        evidence_reference = result.evidence_reference

        if artifact_manifest is None:
            raise RuntimeError(
                "eligible Build Result lacks artifact manifest"
            )

        if validation_result is None:
            raise RuntimeError(
                "eligible Build Result lacks validation result"
            )

        if evidence_reference is None:
            raise RuntimeError(
                "eligible Build Result lacks evidence reference"
            )

        return cls(
            build_id=result.build_id,
            artifact_manifest=artifact_manifest,
            validation_result=validation_result,
            evidence_reference=evidence_reference,
        )
