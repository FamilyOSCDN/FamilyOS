"""Tests for runtime lifecycle states."""

from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


def test_runtime_states() -> None:
    """Runtime states should expose stable values."""

    assert RuntimeState.LOADED.value == "loaded"
    assert RuntimeState.INITIALIZED.value == "initialized"
    assert RuntimeState.ACTIVE.value == "active"
    assert RuntimeState.STOPPING.value == "stopping"
    assert RuntimeState.STOPPED.value == "stopped"
