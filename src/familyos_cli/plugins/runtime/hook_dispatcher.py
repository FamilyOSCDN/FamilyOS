from __future__ import annotations

from familyos_cli.plugins.hooks import HookRegistry


class HookDispatcher:
    """Dispatch hook events to registered callbacks."""

    def __init__(
        self,
        registry: HookRegistry,
    ) -> None:
        """Initialize the hook dispatcher."""
        self._registry = registry

    def dispatch(
        self,
        event: str,
        context: object,
    ) -> None:
        """Dispatch an event to all registered callbacks."""
        for callback in self._registry.get(event):
            callback(context)
