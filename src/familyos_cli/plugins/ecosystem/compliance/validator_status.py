"""Compliance validator execution statuses."""

from __future__ import annotations

from enum import StrEnum


class ValidatorStatus(StrEnum):
    """Represent the execution status of a compliance validator.

    Distinct from :class:`~familyos_cli.plugins.ecosystem.compliance.rule_outcome.RuleOutcome`:
    a validator that runs successfully (``SUCCESS``) may still demonstrate
    a rule violation (``RuleOutcome.FAIL``).
    """

    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
