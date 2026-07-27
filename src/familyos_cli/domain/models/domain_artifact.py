"""Domain artifact model."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DomainArtifact:
    """Represents a FamilyOS domain documentation artifact."""

    name: str
    description: str = ""

    @property
    def normalized_name(self) -> str:
        """Return the normalized domain name."""

        return self.name.strip().lower().replace(" ", "-")

    @property
    def display_name(self) -> str:
        """Return the display name."""

        return self.name.strip()

    def target_directory(
        self,
        root: Path,
    ) -> Path:
        """Return the target directory for the domain."""

        return (
            root
            / "docs"
            / "30-domains"
            / self.normalized_name
        )