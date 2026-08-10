"""Base contribution contract."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)


@dataclass(
    frozen=True,
    slots=True,
)
class Contribution:
    """Base class for every plugin contribution."""

    id: PluginContributionId
