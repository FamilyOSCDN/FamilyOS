"""Tests for plugin runtime context."""

from familyos_cli.plugins.runtime.runtime_context import (
    RuntimeContext,
)
from familyos_cli.plugins.runtime.runtime_lifecycle_manager import (
    RuntimeLifecycleManager,
)
from familyos_cli.plugins.runtime.runtime_observation_recorder import (
    RuntimeObservationRecorder,
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


def test_runtime_context_creates_observation_recorder() -> None:
    """Runtime context should provide an observation recorder."""

    context = RuntimeContext()

    assert isinstance(
        context.observations,
        RuntimeObservationRecorder,
    )


def test_runtime_context_accepts_observation_recorder() -> None:
    """Runtime context should accept an injected observation recorder."""

    observations = RuntimeObservationRecorder()

    context = RuntimeContext(
        observations=observations,
    )

    assert context.observations is observations


def test_injected_lifecycle_uses_context_observation_recorder() -> None:
    """Injected lifecycle should record through context observations."""

    lifecycle = RuntimeLifecycleManager()
    observations = RuntimeObservationRecorder()

    context = RuntimeContext(
        lifecycle=lifecycle,
        observations=observations,
    )

    assert context.lifecycle is lifecycle
    assert context.observations is observations
