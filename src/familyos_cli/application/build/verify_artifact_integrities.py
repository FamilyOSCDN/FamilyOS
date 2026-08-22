"""Verify recorded artifact integrity against current artifact bytes."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.application.build.artifact_integrity import ArtifactIntegrity
from familyos_cli.application.build.artifact_integrity_service import (
    ArtifactIntegrityService,
)


@dataclass(frozen=True, slots=True)
class ArtifactIntegrityVerification:
    """Verification result for one recorded artifact integrity."""

    integrity: ArtifactIntegrity
    successful: bool


@dataclass(frozen=True, slots=True)
class ArtifactIntegrityVerificationResult:
    """Aggregate verification result for a recorded artifact set."""

    verifications: tuple[ArtifactIntegrityVerification, ...]

    @property
    def successful(self) -> bool:
        """Return whether every recorded artifact still matches its bytes."""

        return bool(self.verifications) and all(
            verification.successful
            for verification in self.verifications
        )


class VerifyArtifactIntegritiesUseCase:
    """Verify current artifact bytes against recorded integrity metadata."""

    def __init__(
        self,
        service: ArtifactIntegrityService | None = None,
    ) -> None:
        self._service = service or ArtifactIntegrityService()

    def execute(
        self,
        integrities: tuple[ArtifactIntegrity, ...],
    ) -> ArtifactIntegrityVerificationResult:
        """Verify every integrity record against the current artifact bytes."""

        return ArtifactIntegrityVerificationResult(
            verifications=tuple(
                ArtifactIntegrityVerification(
                    integrity=integrity,
                    successful=self._service.verify(integrity),
                )
                for integrity in integrities
            )
        )
