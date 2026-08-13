"""Canonical compliance rule evaluation outcomes."""

from __future__ import annotations

from enum import StrEnum


class RuleOutcome(StrEnum):
    """Represent the outcome of evaluating a compliance rule.

    Distinct from :class:`~familyos_cli.plugins.ecosystem.compliance.severity.Severity`:
    outcome describes evaluation state, severity describes consequence.
    Missing or incomplete evidence must never resolve to ``PASS``.
    """

    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    NOT_EVALUATED = "not_evaluated"
    ERROR = "error"
