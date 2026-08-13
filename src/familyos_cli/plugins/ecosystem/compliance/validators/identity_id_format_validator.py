"""Validator for PLUGIN-IDENT-002."""

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
from familyos_cli.plugins.identity import PluginId

VALIDATOR_ID = "identity.id-format"


class IdentityIdFormatValidator(ComplianceValidator):
    """Validate that the manifest id is a canonical Plugin Identifier."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Collect evidence of manifest id validity."""

        builder = EvidenceBuilder(
            plugin_id=context.plugin_descriptor.id,
            plugin_version=context.plugin_descriptor.version,
            producer=VALIDATOR_ID,
        )

        if context.manifest is None:
            evidence = builder.add(
                evidence_type=EvidenceType.IDENTITY,
                source="plugin.yaml",
                scope="manifest",
                payload={"available": False},
            )

            return ValidatorRunResult(
                status=ValidatorStatus.SUCCESS,
                evidence=(evidence,),
            )

        raw_id = context.manifest.get("id") or ""

        try:
            PluginId(raw_id)
            valid = True
        except ValueError:
            valid = False

        evidence = builder.add(
            evidence_type=EvidenceType.IDENTITY,
            source="plugin.yaml:id",
            scope="manifest",
            payload={"available": True, "id": raw_id, "valid": valid},
        )

        return ValidatorRunResult(
            status=ValidatorStatus.SUCCESS,
            evidence=(evidence,),
        )

    def check(
        self,
        evidence: tuple[ComplianceEvidence, ...],
    ) -> RuleOutcome:
        """Return the outcome of the id-format check."""

        payload = evidence[0].payload

        if not payload.get("available"):
            return RuleOutcome.NOT_EVALUATED

        if payload.get("valid"):
            return RuleOutcome.PASS

        return RuleOutcome.FAIL
