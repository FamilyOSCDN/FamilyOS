"""Plugin runtime observation recorder."""

from __future__ import annotations

from familyos_cli.plugins.runtime.runtime_observation import (
    RuntimeObservation,
)
from familyos_cli.plugins.runtime.runtime_plugin_id import (
    RuntimePluginId,
)


class RuntimeObservationRecorder:
    """Collect runtime observations in recording order."""

    def __init__(
        self,
    ) -> None:
        """Initialize an empty observation recorder."""

        self._observations: list[
            RuntimeObservation
        ] = []

    def record(
        self,
        observation: RuntimeObservation,
    ) -> None:
        """Record a runtime observation."""

        self._observations.append(
            observation,
        )

    def all(
        self,
    ) -> tuple[RuntimeObservation, ...]:
        """Return all recorded observations."""

        return tuple(
            self._observations,
        )

    def for_plugin(
        self,
        plugin_id: str | RuntimePluginId,
    ) -> tuple[RuntimeObservation, ...]:
        """Return observations associated with one plugin."""

        runtime_plugin_id = self._runtime_plugin_id(
            plugin_id,
        )

        return tuple(
            observation
            for observation in self._observations
            if observation.plugin_id == runtime_plugin_id
        )

    def clear(
        self,
    ) -> None:
        """Remove all recorded observations."""

        self._observations.clear()

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
