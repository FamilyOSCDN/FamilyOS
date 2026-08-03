"""Plugin capability model."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PluginCapability:
    """Describe a capability provided by a plugin."""

    id: PluginCapabilityId

    display_name: str

    description: str = ""

    metadata: dict[str, str] = field(
        default_factory=dict,
    )
