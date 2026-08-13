"""Validator for PLUGIN-DEP-001."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.compliance.compliance_evidence import (
    ComplianceEvidence,
)
from familyos_cli.plugins.ecosystem.compliance.dependency_expression_parser import (
    parse_dependency_expression,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_builder import (
    EvidenceBuilder,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_type import (
    EvidenceType,
)
from familyos_cli.plugins.ecosystem.compliance.ports.compliance_validator import (
    ComplianceValidator,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validation_context import (
    ValidationContext,
)
from familyos_cli.plugins.ecosystem.compliance.validator_run_result import (
    ValidatorRunResult,
)
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)

VALIDATOR_ID = "dependencies.expression-format"


class DependencyExpressionFormatValidator(ComplianceValidator):
    """Validate that declared dependency expressions are well-formed."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Parse every declared dependency expression, if any are declared."""

        builder = EvidenceBuilder(
            plugin_id=context.plugin_descriptor.id,
            plugin_version=context.plugin_descriptor.version,
            producer=VALIDATOR_ID,
        )

        raw_dependencies = (
            context.manifest.get("dependencies") if context.manifest else None
        )

        if not raw_dependencies:
            evidence = builder.add(
                evidence_type=EvidenceType.DEPENDENCY,
                source="plugin.yaml:dependencies",
                scope="manifest",
                payload={"present": False},
            )

            return ValidatorRunResult(
                status=ValidatorStatus.SUCCESS,
                evidence=(evidence,),
            )

        invalid: list[str] = []

        for entry in raw_dependencies:
            try:
                parse_dependency_expression(str(entry))
            except ValueError:
                invalid.append(str(entry))

        evidence = builder.add(
            evidence_type=EvidenceType.DEPENDENCY,
            source="plugin.yaml:dependencies",
            scope="manifest",
            payload={"present": True, "invalid": invalid},
        )

        return ValidatorRunResult(
            status=ValidatorStatus.SUCCESS,
            evidence=(evidence,),
        )

    def check(
        self,
        evidence: tuple[ComplianceEvidence, ...],
    ) -> RuleOutcome:
        """Return the outcome of the dependency expression format check."""

        payload = evidence[0].payload

        if not payload.get("present"):
            return RuleOutcome.NOT_APPLICABLE

        if payload.get("invalid"):
            return RuleOutcome.FAIL

        return RuleOutcome.PASS
