"""Plugin lifecycle event."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.lifecycle.plugin_state import (
    PluginState,
)
from familyos_cli.plugins.identity import PluginId


@dataclass(frozen=True, slots=True)
class LifecycleEvent:
    """Represent a plugin lifecycle state transition."""

    plugin_id: str
    previous_state: PluginState
    new_state: PluginState

    def __post_init__(self) -> None:
        """Validate the Plugin Identifier."""

        canonical_plugin_id = PluginId(self.plugin_id).value

        object.__setattr__(
            self,
            "plugin_id",
            canonical_plugin_id,
        )
