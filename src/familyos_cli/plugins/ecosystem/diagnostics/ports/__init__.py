"""Public protocols for plugin resolution diagnostics."""

from .conflict_detection_source import ConflictDetectionSource
from .cycle_detection_source import CycleDetectionSource
from .resolution_context_adapter import (
    ResolutionContextDiagnosticAdapter,
)
from .resolution_diagnostic_adapter import ResolutionDiagnosticAdapter

__all__ = [
    "ConflictDetectionSource",
    "CycleDetectionSource",
    "ResolutionContextDiagnosticAdapter",
    "ResolutionDiagnosticAdapter",
]
