"""Canonical fingerprint identity for a resolved Build Context."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BuildContextFingerprint:
    """Deterministic identity of canonical Build Context inputs."""

    algorithm: str
    digest: str

    def __post_init__(self) -> None:
        if self.algorithm != "sha256":
            raise ValueError("Build Context fingerprint algorithm must be sha256")

        if len(self.digest) != 64:
            raise ValueError(
                "Build Context fingerprint digest must contain 64 hexadecimal characters"
            )

        try:
            int(self.digest, 16)
        except ValueError as exc:
            raise ValueError(
                "Build Context fingerprint digest must be hexadecimal"
            ) from exc

        if self.digest != self.digest.lower():
            raise ValueError(
                "Build Context fingerprint digest must use lowercase hexadecimal"
            )

    def matches(self, other: BuildContextFingerprint) -> bool:
        """Return whether two canonical Build Context fingerprints match."""

        return self == other
