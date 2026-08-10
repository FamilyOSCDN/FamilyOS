"""Tests for runtime lifecycle observability."""

from familyos_cli.plugins.runtime.runtime_context import (
    RuntimeContext,
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


def test_lifecycle_transition_records_observation() -> None:
    """Lifecycle transitions should be recorded automatically."""

    context = RuntimeContext()

    context.lifecycle.register(
        "familyos.security",
    )

    context.lifecycle.transition(
        "familyos.security",
        RuntimeState.INITIALIZED,
    )

    assert context.observations.all() == (
        RuntimeObservation(
            plugin_id=RuntimePluginId("familyos.security"),
            previous_state=RuntimeState.LOADED,
            new_state=RuntimeState.INITIALIZED,
        ),
    )


def test_multiple_lifecycle_transitions_preserve_order() -> None:
    """Runtime observations should preserve transition order."""

    context = RuntimeContext()

    context.lifecycle.register(
        "familyos.security",
    )

    context.lifecycle.transition(
        "familyos.security",
        RuntimeState.INITIALIZED,
    )

    context.lifecycle.transition(
        "familyos.security",
        RuntimeState.ACTIVE,
    )

    assert context.observations.all() == (
        RuntimeObservation(
            plugin_id=RuntimePluginId("familyos.security"),
            previous_state=RuntimeState.LOADED,
            new_state=RuntimeState.INITIALIZED,
        ),
        RuntimeObservation(
            plugin_id=RuntimePluginId("familyos.security"),
            previous_state=RuntimeState.INITIALIZED,
            new_state=RuntimeState.ACTIVE,
        ),
    )
