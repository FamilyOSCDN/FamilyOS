"""Plugin runtime transition model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


@dataclass(frozen=True, slots=True)
class RuntimeTransition:
    """Represents a runtime lifecycle state transition."""

    previous_state: RuntimeState
    new_state: RuntimeState
