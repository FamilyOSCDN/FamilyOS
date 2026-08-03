"""Runtime lifecycle transition errors."""

from __future__ import annotations


class InvalidRuntimeTransitionError(RuntimeError):
    """Raised when an invalid runtime lifecycle transition is attempted."""
