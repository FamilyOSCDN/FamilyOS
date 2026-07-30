"""Plugin resolution diagnostic model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResolutionDiagnostic:
    """Describes a diagnostic produced during plugin resolution."""

    plugin: str
    message: str
