"""Generation artifact."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.application.generation.generation_options import (
    GenerationOptions,
)


@dataclass(frozen=True, slots=True)
class GenerationArtifact:
    """Represents one executable generation artifact."""

    template: str

    destination: str

    context: GenerationContext = field(
        default_factory=GenerationContext,
    )

    options: GenerationOptions = field(
        default_factory=GenerationOptions,
    )
