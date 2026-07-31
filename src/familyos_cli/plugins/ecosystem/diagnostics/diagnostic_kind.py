"""Plugin resolution diagnostic kinds."""

from __future__ import annotations

from enum import StrEnum


class DiagnosticKind(StrEnum):
    """Identify the nature of a plugin resolution diagnostic."""

    VERSION_CONFLICT = "version_conflict"
    DEPENDENCY_CYCLE = "dependency_cycle"
    MISSING_DEPENDENCY = "missing_dependency"
    UNKNOWN_PLUGIN = "unknown_plugin"
    INVALID_PACKAGE = "invalid_package"
    RESOLUTION_FAILURE = "resolution_failure"
    INFORMATION = "information"
