"""Domain generation contribution."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DomainGenerationContribution(
    Contribution,
):
    """Contribution provided by a plugin for domain generation."""

    domain: str

    description: str

    artifacts: tuple[str, ...]
