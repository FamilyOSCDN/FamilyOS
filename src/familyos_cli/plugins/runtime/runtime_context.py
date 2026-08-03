"""Plugin runtime context."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.runtime.runtime_lifecycle_manager import (
    RuntimeLifecycleManager,
)


@dataclass(slots=True)
class RuntimeContext:
    """Provide shared services for the plugin runtime."""

    lifecycle: RuntimeLifecycleManager = field(
        default_factory=RuntimeLifecycleManager,
    )
