"""Explanation services and models for diagnostics."""

from .resolution_explainer import ResolutionExplainer
from .resolution_explanation import ResolutionExplanation
from .rules import (
    DefaultRule,
    DependencyCycleRule,
    ExplanationRule,
    ExplanationRuleRegistry,
    MissingDependencyRule,
    VersionConflictRule,
)

__all__ = [
    "DefaultRule",
    "DependencyCycleRule",
    "ExplanationRule",
    "ExplanationRuleRegistry",
    "MissingDependencyRule",
    "ResolutionExplanation",
    "ResolutionExplainer",
    "VersionConflictRule",
]
