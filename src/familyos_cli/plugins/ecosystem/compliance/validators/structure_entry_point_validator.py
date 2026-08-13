"""Validator for PLUGIN-STRUCT-001."""

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

VALIDATOR_ID = "structure.entry-point"


class StructureEntryPointValidator(ComplianceValidator):
    """Validate that the plugin entry point imports and subclasses Plugin."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Attempt to load the plugin instance and record the outcome."""

        builder = EvidenceBuilder(
            plugin_id=context.plugin_descriptor.id,
            plugin_version=context.plugin_descriptor.version,
            producer=VALIDATOR_ID,
        )

        try:
            load_plugin_instance(context.plugin_descriptor)
            loaded = True
            error = None
        except Exception as caught_error:  # noqa: BLE001 - expected plugin-author failure path
            loaded = False
            error = str(caught_error)

        evidence = builder.add(
            evidence_type=EvidenceType.STRUCTURE,
            source="entry-point",
            scope="runtime",
            payload={"loaded": loaded, "error": error},
        )

        return ValidatorRunResult(
            status=ValidatorStatus.SUCCESS,
            evidence=(evidence,),
        )

    def check(
        self,
        evidence: tuple[ComplianceEvidence, ...],
    ) -> RuleOutcome:
        """Return PASS if the plugin loaded, else FAIL."""

        if evidence[0].payload.get("loaded"):
            return RuleOutcome.PASS

        return RuleOutcome.FAIL
