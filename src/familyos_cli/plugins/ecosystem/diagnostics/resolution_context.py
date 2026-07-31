"""Resolution context for diagnostic generation."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.diagnostics.ports import (
    CycleDetectionSource,
)
from familyos_cli.plugins.ecosystem.resolution import ResolutionPlan


@dataclass(frozen=True, slots=True)
class ResolutionContext:
    """Provide all information required for diagnostics."""

    plan: ResolutionPlan
    cycle_source: CycleDetectionSource | None = None
