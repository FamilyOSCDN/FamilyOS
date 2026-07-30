"""Plugin lifecycle event model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.lifecycle.plugin_state import (
    PluginState,
)


@dataclass(frozen=True, slots=True)
class LifecycleEvent:
    """Represents a lifecycle state transition."""

    plugin_name: str
    previous_state: PluginState
    new_state: PluginState
