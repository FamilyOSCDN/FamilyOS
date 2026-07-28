"""Generation specification."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.application.generation.generation_artifact import (
    GenerationArtifact,
)


@dataclass(frozen=True, slots=True)
class GenerationSpecification:
    """Describes a complete generation execution."""

    directories: list[str] = field(
        default_factory=list,
    )

    artifacts: list[GenerationArtifact] = field(
        default_factory=list,
    )
