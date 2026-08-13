"""Validator for PLUGIN-IDENT-001."""

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

VALIDATOR_ID = "identity.manifest-presence"


class IdentityManifestPresenceValidator(ComplianceValidator):
    """Validate that plugin.yaml exists and parses as a mapping."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Collect evidence of manifest presence and parseability."""

        builder = EvidenceBuilder(
            plugin_id=context.plugin_descriptor.id,
            plugin_version=context.plugin_descriptor.version,
            producer=VALIDATOR_ID,
        )

        evidence = builder.add(
            evidence_type=EvidenceType.STRUCTURE,
            source="plugin.yaml",
            scope="manifest",
            payload={
                "exists": context.manifest is not None,
                "error": context.manifest_error,
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
        """Return PASS if the manifest exists and parsed, else FAIL."""

        if evidence[0].payload.get("exists"):
            return RuleOutcome.PASS

        return RuleOutcome.FAIL
