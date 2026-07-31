"""Public API for plugin resolution diagnostics."""

from .adapters import (
    ConflictDiagnosticAdapter,
    CycleDiagnosticAdapter,
    ResolutionConflictAdapter,
    ResolutionConflictDiagnosticAdapter,
    ResolutionCycleDiagnosticAdapter,
)
from .conflicts import (
    ConflictReason,
    PluginConflict,
)
from .cycles import (
    DependencyCycle,
)
from .detection import (
    ConflictDetector,
    CycleDetector,
)
from .diagnostic_builder import (
    DiagnosticBuilder,
)
from .diagnostic_kind import (
    DiagnosticKind,
)
from .diagnostic_report import (
    DiagnosticReport,
)
from .diagnostic_severity import (
    DiagnosticSeverity,
)
from .explaining import (
    DefaultRule,
    DependencyCycleRule,
    ExplanationRule,
    ExplanationRuleRegistry,
    MissingDependencyRule,
    ResolutionExplainer,
    ResolutionExplanation,
    VersionConflictRule,
)
from .formatting import (
    ExplanationFormatter,
    JsonExplanationFormatter,
    TextExplanationFormatter,
)
from .pipeline import (
    DiagnosticPipeline,
)
from .plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)
from .ports import (
    ConflictDetectionSource,
    CycleDetectionSource,
    ResolutionContextDiagnosticAdapter,
    ResolutionDiagnosticAdapter,
)
from .rendering import (
    DiagnosticCliRenderer,
    TerminalFormatter,
)
from .resolution_context import (
    ResolutionContext,
)
from .suggestions import (
    ResolutionSuggestion,
    SuggestionGenerator,
)

__all__ = [
    "ConflictDetectionSource",
    "ConflictDiagnosticAdapter",
    "ConflictDetector",
    "ConflictReason",
    "CycleDetectionSource",
    "CycleDiagnosticAdapter",
    "CycleDetector",
    "DefaultRule",
    "DependencyCycle",
    "DependencyCycleRule",
    "DiagnosticBuilder",
    "DiagnosticCliRenderer",
    "DiagnosticKind",
    "DiagnosticPipeline",
    "DiagnosticReport",
    "DiagnosticSeverity",
    "ExplanationFormatter",
    "ExplanationRule",
    "ExplanationRuleRegistry",
    "JsonExplanationFormatter",
    "MissingDependencyRule",
    "PluginConflict",
    "PluginResolutionDiagnostic",
    "ResolutionConflictAdapter",
    "ResolutionConflictDiagnosticAdapter",
    "ResolutionContext",
    "ResolutionContextDiagnosticAdapter",
    "ResolutionCycleDiagnosticAdapter",
    "ResolutionDiagnosticAdapter",
    "ResolutionExplainer",
    "ResolutionExplanation",
    "ResolutionSuggestion",
    "SuggestionGenerator",
    "TerminalFormatter",
    "TextExplanationFormatter",
    "VersionConflictRule",
]
