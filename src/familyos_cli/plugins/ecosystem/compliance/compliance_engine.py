"""Compliance validation engine."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from familyos_cli.plugins.ecosystem.compliance.compliance_decision import (
    ComplianceDecisionEvaluator,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_evidence import (
    ComplianceEvidence,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_finding import (
    ComplianceFinding,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_profile import (
    ComplianceProfile,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_request import (
    ComplianceRequest,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_result import (
    ComplianceResult,
)
from familyos_cli.plugins.ecosystem.compliance.finding_generator import (
    FindingGenerator,
)
from familyos_cli.plugins.ecosystem.compliance.profile_registry import (
    ProfileRegistry,
)
from familyos_cli.plugins.ecosystem.compliance.rule_evaluation import (
    RuleEvaluation,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.rule_registry import RuleRegistry
from familyos_cli.plugins.ecosystem.compliance.validation_context_builder import (
    ValidationContextBuilder,
)
from familyos_cli.plugins.ecosystem.compliance.validator_registry import (
    ValidatorRegistry,
)
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)

_FAILED_VALIDATOR_STATUSES = (ValidatorStatus.FAILED, ValidatorStatus.ERROR)


class ComplianceEngine:
    """Coordinate compliance evaluation from a request to a finalized result.

    See docs/epics/EPIC-PLUGIN-002-plugin-compliance-framework/
    08-Validation-Engine.md for the full conceptual model. This slice
    treats rules as independent (no dependency graph) and evaluates them
    sequentially (no parallel execution) — see the plan's explicit
    non-goals.
    """

    def __init__(
        self,
        *,
        rule_registry: RuleRegistry,
        profile_registry: ProfileRegistry,
        validator_registry: ValidatorRegistry,
        context_builder: ValidationContextBuilder,
    ) -> None:
        """Initialize the engine with its governed registries."""

        self._rule_registry = rule_registry
        self._profile_registry = profile_registry
        self._validator_registry = validator_registry
        self._context_builder = context_builder

    def evaluate(
        self,
        request: ComplianceRequest,
    ) -> ComplianceResult:
        """Evaluate a plugin against a compliance profile."""

        evaluation_id = str(uuid4())
        started_at = datetime.now(UTC)

        profile = self._profile_registry.get(request.profile_id)
        context = self._context_builder.build(request.plugin_descriptor)

        rule_evaluations: list[RuleEvaluation] = []
        all_evidence: list[ComplianceEvidence] = []
        findings: list[ComplianceFinding] = []

        for rule_id in self._effective_rule_ids(profile):
            rule = self._rule_registry.get(rule_id)
            mandatory = rule.mandatory or rule_id in profile.mandatory_rule_ids

            if not rule.applicability.applies_to(context.classification):
                evaluation = RuleEvaluation(
                    rule_id=rule.id,
                    domain=rule.domain,
                    outcome=RuleOutcome.NOT_APPLICABLE,
                    severity=rule.severity,
                    validator_status=ValidatorStatus.SKIPPED,
                    evidence_refs=(),
                    message="Not applicable to this plugin classification.",
                    mandatory=mandatory,
                )
            else:
                validator = self._validator_registry.get(rule.validator_id)

                try:
                    run_result = validator.validate(context)
                except Exception as error:  # noqa: BLE001 - validator bug, not a plugin failure
                    evaluation = RuleEvaluation(
                        rule_id=rule.id,
                        domain=rule.domain,
                        outcome=RuleOutcome.ERROR,
                        severity=rule.severity,
                        validator_status=ValidatorStatus.ERROR,
                        evidence_refs=(),
                        message=f"Validator error: {error}",
                        mandatory=mandatory,
                    )
                else:
                    all_evidence.extend(run_result.evidence)

                    if run_result.status in _FAILED_VALIDATOR_STATUSES:
                        outcome = RuleOutcome.ERROR
                    else:
                        outcome = validator.check(run_result.evidence)

                    evaluation = RuleEvaluation(
                        rule_id=rule.id,
                        domain=rule.domain,
                        outcome=outcome,
                        severity=rule.severity,
                        validator_status=run_result.status,
                        evidence_refs=tuple(
                            item.id for item in run_result.evidence
                        ),
                        message=run_result.message,
                        mandatory=mandatory,
                    )

            rule_evaluations.append(evaluation)

            finding = FindingGenerator.from_evaluation(
                rule,
                evaluation,
                evaluation_id=evaluation_id,
                finding_id=f"{evaluation_id}:{rule.id}",
            )

            if finding is not None:
                findings.append(finding)

        status = ComplianceDecisionEvaluator.decide(
            tuple(rule_evaluations),
            profile,
        )

        return ComplianceResult(
            evaluation_id=evaluation_id,
            plugin_id=context.plugin_descriptor.id,
            plugin_version=context.plugin_descriptor.version,
            profile_id=profile.id,
            status=status,
            rule_evaluations=tuple(rule_evaluations),
            findings=tuple(findings),
            evidence=tuple(all_evidence),
            started_at=started_at,
            completed_at=datetime.now(UTC),
        )

    @staticmethod
    def _effective_rule_ids(
        profile: ComplianceProfile,
    ) -> tuple[str, ...]:
        """Resolve the effective rule set: included + mandatory - excluded."""

        excluded = set(profile.excluded_rule_ids)

        effective = [
            rule_id
            for rule_id in profile.included_rule_ids
            if rule_id not in excluded
        ]

        for rule_id in profile.mandatory_rule_ids:
            if rule_id not in effective and rule_id not in excluded:
                effective.append(rule_id)

        return tuple(effective)
