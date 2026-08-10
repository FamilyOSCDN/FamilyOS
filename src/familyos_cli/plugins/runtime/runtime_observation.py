"""Plugin runtime observation model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


@dataclass(
    frozen=True,
    slots=True,
)
class RuntimeObservation:
    """Describe an observable plugin runtime state transition."""

    plugin_id: str
    previous_state: RuntimeState
    new_state: RuntimeState
