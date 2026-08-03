"""Tests for runtime lifecycle manager."""

import pytest

from familyos_cli.plugins.runtime.invalid_runtime_transition_error import (
    InvalidRuntimeTransitionError,
)
from familyos_cli.plugins.runtime.runtime_lifecycle_manager import (
    RuntimeLifecycleManager,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


def test_register_starts_loaded() -> None:
    """Registered plugins should start in LOADED."""

    manager = RuntimeLifecycleManager()

    manager.register(
        "security",
    )

    assert (
        manager.state(
            "security",
        )
        == RuntimeState.LOADED
    )


def test_valid_transition() -> None:
    """Valid transitions should succeed."""

    manager = RuntimeLifecycleManager()

    manager.register(
        "security",
    )

    transition = manager.transition(
        "security",
        RuntimeState.INITIALIZED,
    )

    assert (
        transition.previous_state
        == RuntimeState.LOADED
    )

    assert (
        transition.new_state
        == RuntimeState.INITIALIZED
    )

    assert (
        manager.state(
            "security",
        )
        == RuntimeState.INITIALIZED
    )


def test_invalid_transition_raises() -> None:
    """Invalid transitions should raise."""

    manager = RuntimeLifecycleManager()

    manager.register(
        "security",
    )

    with pytest.raises(
        InvalidRuntimeTransitionError,
    ):
        manager.transition(
            "security",
            RuntimeState.ACTIVE,
        )
