"""Plugin contribution model."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PluginContribution:
    """Describe the contribution of a plugin."""

    templates: tuple[Path, ...] = ()

    specifications: tuple[Path, ...] = ()

    variables: Mapping[str, object] = field(
        default_factory=dict,
    )

    generation_contributions: tuple[
        GenerationContribution,
        ...
    ] = ()
