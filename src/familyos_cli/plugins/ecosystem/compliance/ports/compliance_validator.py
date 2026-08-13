"""Compliance validator port."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.plugins.ecosystem.compliance.compliance_evidence import (
    ComplianceEvidence,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validation_context import (
    ValidationContext,
)
from familyos_cli.plugins.ecosystem.compliance.validator_run_result import (
    ValidatorRunResult,
)


class ComplianceValidator(ABC):
    """Contract for a compliance validator.

    A validator produces evidence and reports its own execution status; it
    never declares overall rule compliance. Rule evaluation (PASS/FAIL) is
    decided separately by ``check`` from the evidence the validator
    collected, keeping evidence production and compliance judgment as two
    distinct, independently testable steps.
    """

    @abstractmethod
    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Collect evidence for the bound rule from the validation context."""

        raise NotImplementedError

    @abstractmethod
    def check(
        self,
        evidence: tuple[ComplianceEvidence, ...],
    ) -> RuleOutcome:
        """Derive the rule outcome from evidence produced by ``validate``."""

        raise NotImplementedError
