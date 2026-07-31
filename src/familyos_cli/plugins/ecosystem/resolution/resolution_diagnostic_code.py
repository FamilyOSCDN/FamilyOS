"""Plugin resolution diagnostic codes."""

from __future__ import annotations

from enum import StrEnum


class ResolutionDiagnosticCode(StrEnum):
    """Identify categories of plugin resolution diagnostics."""

    UNSPECIFIED = "unspecified"

    CYCLE_DETECTED = "cycle_detected"

    MISSING_PLUGIN = "missing_plugin"

    MISSING_DEPENDENCY = "missing_dependency"

    VERSION_CONFLICT = "version_conflict"

    UNSATISFIABLE_CONSTRAINT = "unsatisfiable_constraint"

    WARNING = "warning"

    INFO = "info"
