"""Tests for runtime transition errors."""

from familyos_cli.plugins.runtime.invalid_runtime_transition_error import (
    InvalidRuntimeTransitionError,
)


def test_invalid_runtime_transition_error() -> None:
    """The runtime transition error should inherit RuntimeError."""

    error = InvalidRuntimeTransitionError(
        "invalid transition",
    )

    assert isinstance(
        error,
        RuntimeError,
    )
    assert str(error) == "invalid transition"
