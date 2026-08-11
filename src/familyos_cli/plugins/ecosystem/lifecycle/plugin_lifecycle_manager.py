"""Plugin lifecycle state manager."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.lifecycle.lifecycle_event import (
    LifecycleEvent,
)
from familyos_cli.plugins.ecosystem.lifecycle.plugin_state import (
    PluginState,
)
from familyos_cli.plugins.identity import PluginId


class PluginLifecycleManager:
    """Manage plugin lifecycle states."""

    def __init__(self) -> None:
        """Initialize the lifecycle manager."""

        self._states: dict[str, PluginState] = {}

    def register(
        self,
        plugin_id: str,
    ) -> None:
        """Register a plugin in the discovered state."""

        canonical_plugin_id = PluginId(plugin_id).value

        self._states[canonical_plugin_id] = PluginState.DISCOVERED

    def transition(
        self,
        plugin_id: str,
        new_state: PluginState,
    ) -> LifecycleEvent:
        """Move a plugin to another lifecycle state."""

        canonical_plugin_id = PluginId(plugin_id).value

        previous_state = self._states[canonical_plugin_id]

        self._states[canonical_plugin_id] = new_state

        return LifecycleEvent(
            plugin_id=canonical_plugin_id,
            previous_state=previous_state,
            new_state=new_state,
        )

    def state(
        self,
        plugin_id: str,
    ) -> PluginState:
        """Return the current lifecycle state of a plugin."""

        canonical_plugin_id = PluginId(plugin_id).value

        return self._states[canonical_plugin_id]
