"""Validator for PLUGIN-CAP-001."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.compliance.compliance_evidence import (
    ComplianceEvidence,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_builder import (
    EvidenceBuilder,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_type import (
    EvidenceType,
)
from familyos_cli.plugins.ecosystem.compliance.plugin_instance_loader import (
    load_plugin_instance,
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

VALIDATOR_ID = "capabilities.namespace"


class CapabilityNamespaceValidator(ComplianceValidator):
    """Validate that capability ids are namespaced under the plugin id."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Collect evidence of capability id namespacing."""

        builder = EvidenceBuilder(
            plugin_id=context.plugin_descriptor.id,
            plugin_version=context.plugin_descriptor.version,
            producer=VALIDATOR_ID,
        )

        try:
            plugin = load_plugin_instance(context.plugin_descriptor)
        except Exception:  # noqa: BLE001 - expected plugin-author failure path
            evidence = builder.add(
                evidence_type=EvidenceType.CAPABILITY,
                source="runtime",
                scope="runtime",
                payload={"loaded": False},
            )

            return ValidatorRunResult(
                status=ValidatorStatus.SUCCESS,
                evidence=(evidence,),
            )

        expected_prefix = f"{context.plugin_descriptor.id}."

        violations = [
            str(capability.id)
            for capability in plugin.capabilities()
            if not str(capability.id).startswith(expected_prefix)
        ]

        evidence = builder.add(
            evidence_type=EvidenceType.CAPABILITY,
            source="capabilities()",
            scope="runtime",
            payload={"loaded": True, "violations": violations},
        )

        return ValidatorRunResult(
            status=ValidatorStatus.SUCCESS,
            evidence=(evidence,),
        )

    def check(
        self,
        evidence: tuple[ComplianceEvidence, ...],
    ) -> RuleOutcome:
        """Return the outcome of the capability namespace check."""

        payload = evidence[0].payload

        if not payload.get("loaded"):
            return RuleOutcome.NOT_EVALUATED

        if payload.get("violations"):
            return RuleOutcome.FAIL

        return RuleOutcome.PASS
