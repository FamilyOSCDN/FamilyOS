"""Artifact generator contract."""

from __future__ import annotations

from typing import Protocol


class ArtifactGeneratorContract(Protocol):
    """Contract for artifact generation."""

    def generate(
        self,
        artifact_type: str,
        name: str,
    ) -> None:
        """Generate an artifact."""
        ...