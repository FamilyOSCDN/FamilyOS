"""Validator execution result model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.compliance.compliance_evidence import (
    ComplianceEvidence,
)
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)


@dataclass(frozen=True, slots=True)
class ValidatorRunResult:
    """Represent the outcome of executing a compliance validator.

    A validator never declares compliance itself: it reports execution
    status and produced evidence. Rule evaluation (PASS/FAIL) is decided
    separately by the rule's paired ``check(evidence)`` function.
    """

    status: ValidatorStatus
    evidence: tuple[ComplianceEvidence, ...]
    message: str = ""
