"""Validator for PLUGIN-META-004."""

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

VALIDATOR_ID = "metadata.consistency"


class MetadataConsistencyValidator(ComplianceValidator):
    """Validate that manifest version matches the loaded plugin's metadata."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Collect evidence of manifest/runtime version consistency."""

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

        manifest_version = context.manifest.get("version") or ""

        try:
            plugin = load_plugin_instance(context.plugin_descriptor)
            runtime_metadata = plugin.get_metadata()
        except Exception:  # noqa: BLE001 - expected plugin-author failure path
            evidence = builder.add(
                evidence_type=EvidenceType.METADATA,
                source="runtime",
                scope="runtime",
                payload={"available": False, "loaded": False},
            )

            return ValidatorRunResult(
                status=ValidatorStatus.SUCCESS,
                evidence=(evidence,),
            )

        runtime_version = (
            runtime_metadata.version if runtime_metadata is not None else None
        )

        evidence = builder.add(
            evidence_type=EvidenceType.METADATA,
            source="runtime:metadata.version",
            scope="runtime",
            payload={
                "available": True,
                "loaded": True,
                "manifest_version": manifest_version,
                "runtime_version": runtime_version,
                "consistent": manifest_version == runtime_version,
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
        """Return the outcome of the manifest/runtime consistency check."""

        payload = evidence[0].payload

        if not payload.get("available") or not payload.get("loaded"):
            return RuleOutcome.NOT_EVALUATED

        if payload.get("consistent"):
            return RuleOutcome.PASS

        return RuleOutcome.FAIL
