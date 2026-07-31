"""Public API for plugin resolution conflict models."""

from .conflict_reason import ConflictReason
from .plugin_conflict import PluginConflict

__all__ = [
    "ConflictReason",
    "PluginConflict",
]
