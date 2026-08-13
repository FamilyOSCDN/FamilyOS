"""Validator for PLUGIN-CAP-002."""

from __future__ import annotations

from collections import Counter

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

VALIDATOR_ID = "capabilities.uniqueness"


class CapabilityUniquenessValidator(ComplianceValidator):
    """Validate that capability display names are non-empty and unique."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Collect evidence of capability display name uniqueness."""

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

        display_names = [
            capability.display_name for capability in plugin.capabilities()
        ]

        empty = [name for name in display_names if not name.strip()]

        counts = Counter(display_names)
        duplicates = sorted(
            name for name, count in counts.items() if count > 1 and name.strip()
        )

        evidence = builder.add(
            evidence_type=EvidenceType.CAPABILITY,
            source="capabilities()",
            scope="runtime",
            payload={
                "loaded": True,
                "empty_count": len(empty),
                "duplicates": duplicates,
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
        """Return the outcome of the capability uniqueness check."""

        payload = evidence[0].payload

        if not payload.get("loaded"):
            return RuleOutcome.NOT_EVALUATED

        if payload.get("empty_count") or payload.get("duplicates"):
            return RuleOutcome.FAIL

        return RuleOutcome.PASS
