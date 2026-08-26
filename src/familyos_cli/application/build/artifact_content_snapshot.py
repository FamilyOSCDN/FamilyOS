"""Semantic content snapshots for canonical build artifacts."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.application.build.artifact_integrity import (
    ArtifactDigestAlgorithm,
)
from familyos_cli.application.build.artifact_type import ArtifactClass


@dataclass(frozen=True, slots=True)
class ArtifactContentMember:
    """Canonical semantic identity for one regular archive member."""

    path: str
    size: int
    digest_algorithm: ArtifactDigestAlgorithm
    digest: str

    def __post_init__(self) -> None:
        """Reject non-canonical content-member identity."""

        if not self.path:
            raise ValueError("artifact content member path must not be empty")
        if self.path.startswith("/"):
            raise ValueError(
                "artifact content member path must be relative"
            )
        if "\\" in self.path:
            raise ValueError(
                "artifact content member path must use POSIX separators"
            )

        parts = self.path.split("/")
        if any(part in {"", ".", ".."} for part in parts):
            raise ValueError(
                "artifact content member path must be canonical"
            )

        if parts[0].endswith(":"):
            raise ValueError(
                "artifact content member path must not be drive-qualified"
            )

        if self.size < 0:
            raise ValueError(
                "artifact content member size must not be negative"
            )

        if self.digest_algorithm is not ArtifactDigestAlgorithm.SHA256:
            raise ValueError(
                "artifact content member digest algorithm must be sha256"
            )

        if len(self.digest) != 64:
            raise ValueError(
                "artifact content member SHA-256 digest must contain "
                "64 hexadecimal characters"
            )

        if self.digest != self.digest.lower():
            raise ValueError(
                "artifact content member SHA-256 digest must be lowercase"
            )

        try:
            int(self.digest, 16)
        except ValueError as error:
            raise ValueError(
                "artifact content member SHA-256 digest must be hexadecimal"
            ) from error


@dataclass(frozen=True, slots=True)
class ArtifactContentSnapshot:
    """Deterministic semantic content inventory for one package artifact."""

    artifact_type: ArtifactClass
    members: tuple[ArtifactContentMember, ...]

    def __post_init__(self) -> None:
        """Require deterministic unique member ordering."""

        paths = tuple(member.path for member in self.members)

        if paths != tuple(sorted(paths)):
            raise ValueError(
                "artifact content snapshot members must be sorted by path"
            )

        if len(paths) != len(set(paths)):
            raise ValueError(
                "artifact content snapshot member paths must be unique"
            )

    def matches(self, other: ArtifactContentSnapshot) -> bool:
        """Return whether two artifacts have equivalent semantic content."""

        return (
            self.artifact_type is other.artifact_type
            and self.members == other.members
        )
