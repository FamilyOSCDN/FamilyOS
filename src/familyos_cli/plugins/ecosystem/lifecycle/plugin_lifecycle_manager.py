"""Plugin lifecycle manager."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.lifecycle.lifecycle_event import (
    LifecycleEvent,
)
from familyos_cli.plugins.ecosystem.lifecycle.plugin_state import (
    PluginState,
)


class PluginLifecycleManager:
    """Manage installed plugin lifecycle states."""

    def __init__(self) -> None:
        """Initialize lifecycle storage."""

        self._states: dict[str, PluginState] = {}

    def register(
        self,
        plugin_name: str,
    ) -> None:
        """Register a discovered plugin."""

        self._states[plugin_name] = PluginState.DISCOVERED

    def transition(
        self,
        plugin_name: str,
        new_state: PluginState,
    ) -> LifecycleEvent:
        """Move plugin to another lifecycle state."""

        previous_state = self._states[plugin_name]

        self._states[plugin_name] = new_state

        return LifecycleEvent(
            plugin_name=plugin_name,
            previous_state=previous_state,
            new_state=new_state,
        )

    def state(
        self,
        plugin_name: str,
    ) -> PluginState:
        """Return current plugin state."""

        return self._states[plugin_name]
