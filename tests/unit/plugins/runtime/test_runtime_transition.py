"""Tests for runtime transitions."""

from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)
from familyos_cli.plugins.runtime.runtime_transition import (
    RuntimeTransition,
)


def test_runtime_transition_creation() -> None:
    """A runtime transition should preserve both states."""

    transition = RuntimeTransition(
        previous_state=RuntimeState.LOADED,
        new_state=RuntimeState.INITIALIZED,
    )

    assert transition.previous_state == RuntimeState.LOADED
    assert transition.new_state == RuntimeState.INITIALIZED
