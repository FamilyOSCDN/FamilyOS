"""Validator for PLUGIN-META-003."""

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

VALIDATOR_ID = "metadata.description-quality"

_MINIMUM_DESCRIPTION_LENGTH = 20


class MetadataDescriptionQualityValidator(ComplianceValidator):
    """Validate that the manifest description is meaningful."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Collect evidence of manifest description length."""

        builder = EvidenceBuilder(
            plugin_id=context.plugin_descriptor.id,
            plugin_version=context.plugin_descriptor.version,
            producer=VALIDATOR_ID,
        )

        if context.manifest is None:
            evidence = builder.add(
                evidence_type=EvidenceType.METADATA,
                source="plugin.yaml",
                scope="manifest",
                payload={"available": False},
            )

            return ValidatorRunResult(
                status=ValidatorStatus.SUCCESS,
                evidence=(evidence,),
            )

        description = context.manifest.get("description") or ""

        evidence = builder.add(
            evidence_type=EvidenceType.METADATA,
            source="plugin.yaml:description",
            scope="manifest",
            payload={
                "available": True,
                "length": len(description.strip()),
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
        """Return the outcome of the description-quality check."""

        payload = evidence[0].payload

        if not payload.get("available"):
            return RuleOutcome.NOT_EVALUATED

        if payload.get("length", 0) >= _MINIMUM_DESCRIPTION_LENGTH:
            return RuleOutcome.PASS

        return RuleOutcome.FAIL
