"""Structured manifest metadata for canonical build artifact sets."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from familyos_cli.application.build.artifact_integrity import (
    ArtifactDigestAlgorithm,
)
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_id import BuildId

if TYPE_CHECKING:
    from familyos_cli.application.build.package_validation import (
        PackageStructuralValidationStatus,
    )


@dataclass(frozen=True, slots=True)
class ArtifactManifestEntry:
    """Manifest metadata for one canonical build artifact."""

    logical_name: str
    artifact_type: ArtifactClass
    version: str
    size: int
    path: Path
    digest_algorithm: ArtifactDigestAlgorithm
    digest: str
    structural_validation_status: PackageStructuralValidationStatus


@dataclass(frozen=True, slots=True)
class ArtifactManifest:
    """Structured record of one canonical generated artifact set."""

    build_id: BuildId
    entries: tuple[ArtifactManifestEntry, ...]
