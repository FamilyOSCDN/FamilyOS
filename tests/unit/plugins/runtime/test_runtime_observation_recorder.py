"""Tests for runtime observation recorder."""

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


def test_recorder_stores_runtime_observations() -> None:
    """Recorder should preserve runtime observations in order."""

    recorder = RuntimeObservationRecorder()

    first = RuntimeObservation(
        plugin_id=RuntimePluginId("familyos.security"),
        previous_state=RuntimeState.LOADED,
        new_state=RuntimeState.INITIALIZED,
    )

    second = RuntimeObservation(
        plugin_id=RuntimePluginId("familyos.security"),
        previous_state=RuntimeState.INITIALIZED,
        new_state=RuntimeState.ACTIVE,
    )

    recorder.record(
        first,
    )
    recorder.record(
        second,
    )

    assert recorder.all() == (
        first,
        second,
    )


def test_recorder_filters_observations_by_plugin_id() -> None:
    """Recorder should return observations for one plugin."""

    recorder = RuntimeObservationRecorder()

    security = RuntimeObservation(
        plugin_id=RuntimePluginId("familyos.security"),
        previous_state=RuntimeState.INITIALIZED,
        new_state=RuntimeState.ACTIVE,
    )

    finance = RuntimeObservation(
        plugin_id=RuntimePluginId("familyos.finance"),
        previous_state=RuntimeState.INITIALIZED,
        new_state=RuntimeState.ACTIVE,
    )

    recorder.record(
        security,
    )
    recorder.record(
        finance,
    )

    assert recorder.for_plugin(
        "familyos.security",
    ) == (security,)


def test_recorder_can_be_cleared() -> None:
    """Recorder should support clearing accumulated observations."""

    recorder = RuntimeObservationRecorder()

    recorder.record(
        RuntimeObservation(
            plugin_id=RuntimePluginId("familyos.security"),
            previous_state=RuntimeState.INITIALIZED,
            new_state=RuntimeState.ACTIVE,
        ),
    )

    recorder.clear()

    assert recorder.all() == ()
