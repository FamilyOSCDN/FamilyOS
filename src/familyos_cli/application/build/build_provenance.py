"""Canonical provenance relationship for one completed build."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.application.build.artifact_integrity import ArtifactIntegrity
from familyos_cli.application.build.build_context_fingerprint import (
    BuildContextFingerprint,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.toolchain_state import ToolchainState


@dataclass(frozen=True, slots=True)
class BuildProvenance:
    """Trace one canonical build from source and context to final artifacts."""

    build_id: BuildId
    build_context_fingerprint: BuildContextFingerprint
    source_state: SourceState
    dependency_state: DependencyState
    toolchain_state: ToolchainState
    environment_state: EnvironmentState
    artifact_integrities: tuple[ArtifactIntegrity, ...]

    def __post_init__(self) -> None:
        """Reject incomplete or internally inconsistent provenance."""

        if self.source_state.revision is None:
            raise ValueError("Build Provenance requires a captured source revision")

        if not self.artifact_integrities:
            raise ValueError("Build Provenance requires artifact integrity records")

        artifact_types = []

        for integrity in self.artifact_integrities:
            identity = integrity.artifact_identity

            if identity.build_id != self.build_id:
                raise ValueError(
                    "artifact integrity build ID does not match Build Provenance"
                )

            if identity.source_revision != self.source_state.revision:
                raise ValueError(
                    "artifact source revision does not match Build Provenance"
                )

            artifact_types.append(identity.artifact_type)

        if len(artifact_types) != len(set(artifact_types)):
            raise ValueError("Build Provenance artifact types must be unique")
