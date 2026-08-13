"""Validator for PLUGIN-DEP-002."""

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

VALIDATOR_ID = "dependencies.no-self-dependency"


class DependencyNoSelfDependencyValidator(ComplianceValidator):
    """Validate that a plugin does not declare a dependency on itself."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Check every parseable declared dependency against the plugin id."""

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

        self_dependencies: list[str] = []

        for entry in raw_dependencies:
            try:
                parsed = parse_dependency_expression(str(entry))
            except ValueError:
                # Malformed entries are reported by PLUGIN-DEP-001, not here.
                continue

            if parsed.plugin_id == context.plugin_descriptor.id:
                self_dependencies.append(str(entry))

        evidence = builder.add(
            evidence_type=EvidenceType.DEPENDENCY,
            source="plugin.yaml:dependencies",
            scope="manifest",
            payload={
                "present": True,
                "self_dependencies": self_dependencies,
            },
        )

        return ValidatorRunResult(
            status=ValidatorStatus.SUCCESS,
            evidence=(evidence,),
        )

    def check(
        self,
        evidence: tuple[ComplianceEvidence, ...],
    ) -> RuleOutcome:
        """Return the outcome of the self-dependency check."""

        payload = evidence[0].payload

        if not payload.get("present"):
            return RuleOutcome.NOT_APPLICABLE

        if payload.get("self_dependencies"):
            return RuleOutcome.FAIL

        return RuleOutcome.PASS
