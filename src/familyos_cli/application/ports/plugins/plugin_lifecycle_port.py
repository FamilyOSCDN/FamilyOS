"""Plugin lifecycle port."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.plugins.ecosystem.lifecycle import (
    LifecycleEvent,
    PluginState,
)


class PluginLifecyclePort(ABC):
    """Contract for plugin lifecycle management."""

    @abstractmethod
    def transition(
        self,
        plugin_name: str,
        new_state: PluginState,
    ) -> LifecycleEvent:
        """Transition plugin state."""

        raise NotImplementedError
