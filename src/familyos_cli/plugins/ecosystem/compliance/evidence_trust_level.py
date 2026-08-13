"""Compliance evidence trust levels."""

from __future__ import annotations

from enum import StrEnum


class EvidenceTrustLevel(StrEnum):
    """Represent confidence in evidence provenance and integrity.

    Only ``LOCAL`` is produced by this implementation slice. The other
    members define the target model for future evidence sources (trusted
    CI, attested/signed artifacts).
    """

    UNVERIFIED = "unverified"
    LOCAL = "local"
    TRUSTED = "trusted"
    ATTESTED = "attested"
