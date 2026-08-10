"""Runtime lifecycle manager."""

from __future__ import annotations

from familyos_cli.plugins.runtime.invalid_runtime_transition_error import (
    InvalidRuntimeTransitionError,
)
from familyos_cli.plugins.runtime.runtime_observation import (
    RuntimeObservation,
)
from familyos_cli.plugins.runtime.runtime_observation_recorder import (
    RuntimeObservationRecorder,
)
from familyos_cli.plugins.runtime.runtime_plugin_id import (
    RuntimePluginId,
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
        observations: RuntimeObservationRecorder | None = None,
    ) -> None:
        """Initialize runtime lifecycle storage."""

        self._states: dict[
            RuntimePluginId,
            RuntimeState,
        ] = {}

        self._observations = observations

    def register(
        self,
        plugin_id: str | RuntimePluginId,
    ) -> None:
        """Register a plugin runtime."""

        runtime_plugin_id = self._runtime_plugin_id(
            plugin_id,
        )

        self._states[
            runtime_plugin_id
        ] = RuntimeState.LOADED

    def state(
        self,
        plugin_id: str | RuntimePluginId,
    ) -> RuntimeState:
        """Return current runtime state."""

        runtime_plugin_id = self._runtime_plugin_id(
            plugin_id,
        )

        return self._states[
            runtime_plugin_id
        ]

    def transition(
        self,
        plugin_id: str | RuntimePluginId,
        new_state: RuntimeState,
    ) -> RuntimeTransition:
        """Transition a plugin runtime."""

        runtime_plugin_id = self._runtime_plugin_id(
            plugin_id,
        )

        current_state = self.state(
            runtime_plugin_id,
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
            runtime_plugin_id
        ] = new_state

        transition = RuntimeTransition(
            previous_state=current_state,
            new_state=new_state,
        )

        if self._observations is not None:
            self._observations.record(
                RuntimeObservation(
                    plugin_id=runtime_plugin_id,
                    previous_state=current_state,
                    new_state=new_state,
                ),
            )

        return transition

    def set_observation_recorder(
        self,
        observations: RuntimeObservationRecorder,
    ) -> None:
        """Attach an observation recorder to the lifecycle manager."""

        self._observations = observations

    def _runtime_plugin_id(
        self,
        plugin_id: str | RuntimePluginId,
    ) -> RuntimePluginId:
        """Return a canonical runtime plugin identifier."""

        if isinstance(
            plugin_id,
            RuntimePluginId,
        ):
            return plugin_id

        return RuntimePluginId(
            plugin_id,
        )
