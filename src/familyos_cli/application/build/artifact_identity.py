"""Explicit identity metadata for validated build artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_id import BuildId


@dataclass(frozen=True, slots=True)
class ArtifactIdentity:
    """Identity metadata for one structurally validated candidate artifact."""

    logical_name: str
    artifact_type: ArtifactClass
    version: str
    source_revision: str | None
    build_id: BuildId
    path: Path
    size: int
