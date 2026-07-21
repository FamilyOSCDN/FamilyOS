from __future__ import annotations

from collections.abc import Callable


class HookRegistry:
    """Registry of plugin hooks."""

    def __init__(self) -> None:
        """Initialize an empty hook registry."""
        self._hooks: dict[str, list[Callable[..., object]]] = {}

    def register(
        self,
        hook_name: str,
        callback: Callable[..., object],
    ) -> None:
        """Register a callback for a hook."""
        self._hooks.setdefault(hook_name, []).append(callback)

    def get(self, hook_name: str) -> list[Callable[..., object]]:
        """Return all callbacks registered for a hook."""
        return self._hooks.get(hook_name, []).copy()

    def clear(self) -> None:
        """Remove all registered hooks."""
        self._hooks.clear()