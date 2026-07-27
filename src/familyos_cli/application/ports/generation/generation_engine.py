"""Generation engine port."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from familyos_cli.domain.models.project_specification import (
    ProjectSpecification,
)


class GenerationEngine(Protocol):
    """Contract for generation execution."""

    def generate(
        self,
        destination: Path,
        specification: ProjectSpecification,
        context: dict[str, object],
    ) -> None:
        """Generate artifacts."""
        ...