"""Plugin runtime context."""

from __future__ import annotations

from familyos_cli.plugins.runtime.runtime_lifecycle_manager import (
    RuntimeLifecycleManager,
)
from familyos_cli.plugins.runtime.runtime_observation_recorder import (
    RuntimeObservationRecorder,
)


class RuntimeContext:
    """Provide shared services for the plugin runtime."""

    def __init__(
        self,
        lifecycle: RuntimeLifecycleManager | None = None,
        observations: RuntimeObservationRecorder | None = None,
    ) -> None:
        """Initialize shared runtime services."""

        self.observations = (
            observations
            if observations is not None
            else RuntimeObservationRecorder()
        )

        self.lifecycle = (
            lifecycle
            if lifecycle is not None
            else RuntimeLifecycleManager()
        )

        self.lifecycle.set_observation_recorder(
            self.observations,
        )
