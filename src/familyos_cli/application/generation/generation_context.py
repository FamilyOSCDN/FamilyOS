"""Generation context."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from familyos_cli.domain.models.project import (
    Project,
)


@dataclass(frozen=True, slots=True)
class GenerationContext:
    """Context data used during generation."""

    variables: dict[str, object] = field(
        default_factory=dict,
    )

    project: Project | None = None

    destination: Path | None = None
