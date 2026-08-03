"""Plugin runtime lifecycle states."""

from __future__ import annotations

from enum import StrEnum


class RuntimeState(StrEnum):
    """Execution lifecycle states of a loaded plugin."""

    LOADED = "loaded"
    INITIALIZED = "initialized"
    ACTIVE = "active"
    STOPPING = "stopping"
    STOPPED = "stopped"
