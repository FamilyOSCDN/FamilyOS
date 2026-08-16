"""Cryptographic integrity metadata for canonical build artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from familyos_cli.application.build.artifact_identity import ArtifactIdentity


class ArtifactDigestAlgorithm(StrEnum):
    """Approved algorithms for canonical artifact integrity."""

    SHA256 = "sha256"


@dataclass(frozen=True, slots=True)
class ArtifactIntegrity:
    """Recorded cryptographic integrity for one identified artifact."""

    artifact_identity: ArtifactIdentity
    algorithm: ArtifactDigestAlgorithm
    digest: str
