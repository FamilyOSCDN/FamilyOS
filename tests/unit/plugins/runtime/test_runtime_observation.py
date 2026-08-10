"""Tests for runtime observations."""

from familyos_cli.plugins.runtime.runtime_observation import (
    RuntimeObservation,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


def test_runtime_observation_records_transition() -> None:
    """Observation should describe one plugin runtime transition."""

    observation = RuntimeObservation(
        plugin_id="familyos.security",
        previous_state=RuntimeState.INITIALIZED,
        new_state=RuntimeState.ACTIVE,
    )

    assert observation.plugin_id == "familyos.security"
    assert (
        observation.previous_state
        is RuntimeState.INITIALIZED
    )
    assert observation.new_state is RuntimeState.ACTIVE


def test_runtime_observation_is_immutable() -> None:
    """Runtime observations should be immutable value objects."""

    observation = RuntimeObservation(
        plugin_id="familyos.security",
        previous_state=RuntimeState.INITIALIZED,
        new_state=RuntimeState.ACTIVE,
    )

    assert observation == RuntimeObservation(
        plugin_id="familyos.security",
        previous_state=RuntimeState.INITIALIZED,
        new_state=RuntimeState.ACTIVE,
    )
