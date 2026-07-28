"""Aggregated plugin contribution."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(
    frozen=True,
    slots=True,
)
class AggregatedContribution:
    """Represents the merged contributions of all active plugins."""

    templates: tuple[Path, ...] = ()
    specifications: tuple[Path, ...] = ()

    variables: Mapping[str, object] = field(
        default_factory=dict,
    )
