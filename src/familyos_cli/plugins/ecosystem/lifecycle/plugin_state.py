"""Plugin lifecycle states."""

from __future__ import annotations

from enum import StrEnum


class PluginState(StrEnum):
    """Available plugin lifecycle states."""

    DISCOVERED = "discovered"
    AVAILABLE = "available"
    INSTALLED = "installed"
    ENABLED = "enabled"
    DISABLED = "disabled"
    REMOVED = "removed"
