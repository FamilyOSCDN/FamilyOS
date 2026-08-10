"""Plugin runtime observation recorder."""

from __future__ import annotations

from familyos_cli.plugins.runtime.runtime_observation import (
    RuntimeObservation,
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
        plugin_id: str,
    ) -> tuple[RuntimeObservation, ...]:
        """Return observations associated with one plugin."""

        return tuple(
            observation
            for observation in self._observations
            if observation.plugin_id == plugin_id
        )

    def clear(
        self,
    ) -> None:
        """Remove all recorded observations."""

        self._observations.clear()
