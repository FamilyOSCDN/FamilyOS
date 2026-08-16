"""Construct integrity records for identified canonical artifacts."""

from __future__ import annotations

from familyos_cli.application.build.artifact_identity import ArtifactIdentity
from familyos_cli.application.build.artifact_integrity import ArtifactIntegrity
from familyos_cli.application.build.artifact_integrity_service import (
    ArtifactIntegrityService,
)


class BuildArtifactIntegritiesUseCase:
    """Calculate integrity after final artifact identity is established."""

    def __init__(
        self,
        service: ArtifactIntegrityService | None = None,
    ) -> None:
        self._service = service or ArtifactIntegrityService()

    def execute(
        self,
        identities: tuple[ArtifactIdentity, ...],
    ) -> tuple[ArtifactIntegrity, ...]:
        """Return deterministic integrity records for identified artifacts."""

        return tuple(
            self._service.calculate(identity)
            for identity in identities
        )
