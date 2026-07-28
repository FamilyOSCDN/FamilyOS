"""Generation engine port."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)


class GenerationEngine(Protocol):
    """Contract for generation execution."""

    def generate(
        self,
        destination: Path,
        specification: GenerationSpecification,
        context: dict[str, object],
    ) -> None:
        """Generate artifacts."""
        ...
