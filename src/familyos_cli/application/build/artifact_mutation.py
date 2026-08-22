"""Controlled lifecycle transition for intentionally mutated build artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from familyos_cli.application.build.artifact_identity import ArtifactIdentity
from familyos_cli.application.build.artifact_integrity import ArtifactIntegrity
from familyos_cli.application.build.artifact_integrity_service import (
    ArtifactIntegrityService,
)


class ArtifactMutation(Protocol):
    """Intentional mutation applied to artifact bytes."""

    def __call__(self, identity: ArtifactIdentity) -> None:
        """Mutate the artifact represented by the supplied identity."""


@dataclass(frozen=True, slots=True)
class MutatedArtifact:
    """Post-mutation artifact state requiring fresh validation."""

    identity: ArtifactIdentity
    integrity: ArtifactIntegrity


class MutateArtifactUseCase:
    """Apply an intentional mutation and establish fresh byte integrity."""

    def __init__(
        self,
        integrity_service: ArtifactIntegrityService | None = None,
    ) -> None:
        self._integrity_service = (
            integrity_service or ArtifactIntegrityService()
        )

    def execute(
        self,
        identity: ArtifactIdentity,
        mutation: ArtifactMutation,
    ) -> MutatedArtifact:
        """Mutate bytes and return fresh identity and integrity metadata."""

        mutation(identity)

        refreshed_identity = ArtifactIdentity(
            logical_name=identity.logical_name,
            artifact_type=identity.artifact_type,
            version=identity.version,
            source_revision=identity.source_revision,
            build_id=identity.build_id,
            path=identity.path,
            size=identity.path.stat().st_size,
        )

        integrity = self._integrity_service.calculate(refreshed_identity)

        return MutatedArtifact(
            identity=refreshed_identity,
            integrity=integrity,
        )
