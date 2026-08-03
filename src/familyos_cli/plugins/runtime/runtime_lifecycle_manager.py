"""Runtime lifecycle manager."""

from __future__ import annotations

from familyos_cli.plugins.runtime.invalid_runtime_transition_error import (
    InvalidRuntimeTransitionError,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)
from familyos_cli.plugins.runtime.runtime_transition import (
    RuntimeTransition,
)


class RuntimeLifecycleManager:
    """Manage plugin runtime lifecycle."""

    _ALLOWED_TRANSITIONS: dict[
        RuntimeState,
        set[RuntimeState],
    ] = {
        RuntimeState.LOADED: {
            RuntimeState.INITIALIZED,
        },
        RuntimeState.INITIALIZED: {
            RuntimeState.ACTIVE,
        },
        RuntimeState.ACTIVE: {
            RuntimeState.STOPPING,
        },
        RuntimeState.STOPPING: {
            RuntimeState.STOPPED,
        },
        RuntimeState.STOPPED: set(),
    }

    def __init__(
        self,
    ) -> None:
        """Initialize runtime lifecycle storage."""

        self._states: dict[
            str,
            RuntimeState,
        ] = {}

    def register(
        self,
        plugin_name: str,
    ) -> None:
        """Register a plugin runtime."""

        self._states[
            plugin_name
        ] = RuntimeState.LOADED

    def state(
        self,
        plugin_name: str,
    ) -> RuntimeState:
        """Return current runtime state."""

        return self._states[
            plugin_name
        ]

    def transition(
        self,
        plugin_name: str,
        new_state: RuntimeState,
    ) -> RuntimeTransition:
        """Transition a plugin runtime."""

        current_state = self.state(
            plugin_name,
        )

        if (
            new_state
            not in self._ALLOWED_TRANSITIONS[
                current_state
            ]
        ):
            raise InvalidRuntimeTransitionError(
                f"Invalid runtime transition "
                f"{current_state} -> {new_state}."
            )

        self._states[
            plugin_name
        ] = new_state

        return RuntimeTransition(
            previous_state=current_state,
            new_state=new_state,
        )
