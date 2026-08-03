"""
Public runtime API for the FamilyOS Plugin SDK.
"""

from .hook_dispatcher import HookDispatcher
from .invalid_runtime_transition_error import (
    InvalidRuntimeTransitionError,
)
from .lifecycle import Lifecycle
from .plugin_activator import PluginActivator
from .plugin_runtime import PluginRuntime
from .runtime_context import RuntimeContext
from .runtime_lifecycle_manager import RuntimeLifecycleManager
from .runtime_state import RuntimeState
from .runtime_transition import RuntimeTransition

__all__ = [
    "HookDispatcher",
    "InvalidRuntimeTransitionError",
    "Lifecycle",
    "PluginActivator",
    "PluginRuntime",
    "RuntimeContext",
    "RuntimeLifecycleManager",
    "RuntimeState",
    "RuntimeTransition",
]
