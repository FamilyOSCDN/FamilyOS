"""Generation context."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from familyos_cli.domain.models.project import Project


@dataclass(
    frozen=True,
    slots=True,
)
class GenerationContext:
    """Immutable context used during project generation."""

    project: Project

    destination: Path

    variables: dict[str, object]