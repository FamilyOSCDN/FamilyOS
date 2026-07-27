"""Domain generator contract."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from familyos_cli.domain.models.domain_artifact import DomainArtifact


class DomainGeneratorContract(Protocol):
    """Contract for domain generation."""

    def generate(
        self,
        artifact: DomainArtifact,
        root: Path,
    ) -> Path:
        """Generate a domain artifact."""
        ...
