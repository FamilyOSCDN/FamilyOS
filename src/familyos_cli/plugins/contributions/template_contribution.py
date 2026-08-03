"""Template contribution contract."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)


@dataclass(
    frozen=True,
    slots=True,
)
class TemplateContribution(
    Contribution,
):
    """Contribution provided by a plugin for template resources."""

    template_directory: Path
