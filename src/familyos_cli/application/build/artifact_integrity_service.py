"""Calculate and verify canonical artifact integrity."""

from __future__ import annotations

import hashlib

from familyos_cli.application.build.artifact_identity import ArtifactIdentity
from familyos_cli.application.build.artifact_integrity import (
    ArtifactDigestAlgorithm,
    ArtifactIntegrity,
)


class ArtifactIntegrityService:
    """Calculate SHA-256 integrity from final artifact bytes."""

    def calculate(
        self,
        identity: ArtifactIdentity,
    ) -> ArtifactIntegrity:
        """Calculate canonical integrity for the identified artifact."""

        return ArtifactIntegrity(
            artifact_identity=identity,
            algorithm=ArtifactDigestAlgorithm.SHA256,
            digest=self._sha256(identity),
        )

    def verify(
        self,
        integrity: ArtifactIntegrity,
    ) -> bool:
        """Recalculate current bytes and compare with recorded integrity."""

        if integrity.algorithm is not ArtifactDigestAlgorithm.SHA256:
            return False

        identity = integrity.artifact_identity

        try:
            current_size = identity.path.stat().st_size
        except OSError:
            return False

        if current_size != identity.size:
            return False

        return self._sha256(identity) == integrity.digest

    def _sha256(
        self,
        identity: ArtifactIdentity,
    ) -> str:
        """Return lowercase hexadecimal SHA-256 of current artifact bytes."""

        with identity.path.open("rb") as artifact_file:
            return hashlib.file_digest(
                artifact_file,
                "sha256",
            ).hexdigest()
