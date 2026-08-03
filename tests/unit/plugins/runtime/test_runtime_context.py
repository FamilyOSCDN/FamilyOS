"""Tests for the plugin runtime context."""

from familyos_cli.plugins.runtime.runtime_context import (
    RuntimeContext,
)
from familyos_cli.plugins.runtime.runtime_lifecycle_manager import (
    RuntimeLifecycleManager,
)


def test_runtime_context_creates_lifecycle_manager() -> None:
    """Runtime context should provide a lifecycle manager."""

    context = RuntimeContext()

    assert isinstance(
        context.lifecycle,
        RuntimeLifecycleManager,
    )


def test_runtime_context_accepts_lifecycle_manager() -> None:
    """Runtime context should accept an injected lifecycle manager."""

    lifecycle = RuntimeLifecycleManager()

    context = RuntimeContext(
        lifecycle=lifecycle,
    )

    assert context.lifecycle is lifecycle
