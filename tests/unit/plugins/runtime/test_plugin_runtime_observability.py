"""Tests for plugin runtime observability."""

from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)
from familyos_cli.plugins.runtime.runtime_observation import (
    RuntimeObservation,
)
from familyos_cli.plugins.runtime.runtime_plugin_id import (
    RuntimePluginId,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


class ObservablePlugin(
    Plugin,
):
    """Plugin used to verify runtime observability."""


def test_activation_records_runtime_transitions() -> None:
    """Plugin activation should expose its lifecycle transitions."""

    runtime = PluginRuntime()

    runtime.activate(
        ObservablePlugin(),
        plugin_id="familyos.observable",
    )

    assert runtime.context().observations.for_plugin(
        "familyos.observable",
    ) == (
        RuntimeObservation(
            plugin_id=RuntimePluginId("familyos.observable"),
            previous_state=RuntimeState.LOADED,
            new_state=RuntimeState.INITIALIZED,
        ),
        RuntimeObservation(
            plugin_id=RuntimePluginId("familyos.observable"),
            previous_state=RuntimeState.INITIALIZED,
            new_state=RuntimeState.ACTIVE,
        ),
    )


def test_deactivation_records_runtime_transitions() -> None:
    """Plugin deactivation should expose its lifecycle transitions."""

    runtime = PluginRuntime()
    plugin = ObservablePlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.observable",
    )

    runtime.deactivate(
        plugin,
    )

    assert runtime.context().observations.for_plugin(
        "familyos.observable",
    ) == (
        RuntimeObservation(
            plugin_id=RuntimePluginId("familyos.observable"),
            previous_state=RuntimeState.LOADED,
            new_state=RuntimeState.INITIALIZED,
        ),
        RuntimeObservation(
            plugin_id=RuntimePluginId("familyos.observable"),
            previous_state=RuntimeState.INITIALIZED,
            new_state=RuntimeState.ACTIVE,
        ),
        RuntimeObservation(
            plugin_id=RuntimePluginId("familyos.observable"),
            previous_state=RuntimeState.ACTIVE,
            new_state=RuntimeState.STOPPING,
        ),
        RuntimeObservation(
            plugin_id=RuntimePluginId("familyos.observable"),
            previous_state=RuntimeState.STOPPING,
            new_state=RuntimeState.STOPPED,
        ),
    )


def test_runtime_observations_are_isolated_by_plugin() -> None:
    """Runtime observations should remain attributable to each plugin."""

    runtime = PluginRuntime()

    first = ObservablePlugin()
    second = ObservablePlugin()

    runtime.activate(
        first,
        plugin_id="familyos.first",
    )
    runtime.activate(
        second,
        plugin_id="familyos.second",
    )

    runtime.deactivate(
        first,
    )

    assert tuple(
        observation.new_state
        for observation in (
            runtime.context().observations.for_plugin(
                "familyos.first",
            )
        )
    ) == (
        RuntimeState.INITIALIZED,
        RuntimeState.ACTIVE,
        RuntimeState.STOPPING,
        RuntimeState.STOPPED,
    )

    assert tuple(
        observation.new_state
        for observation in (
            runtime.context().observations.for_plugin(
                "familyos.second",
            )
        )
    ) == (
        RuntimeState.INITIALIZED,
        RuntimeState.ACTIVE,
    )
