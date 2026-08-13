"""Validator for PLUGIN-STRUCT-002."""

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

VALIDATOR_ID = "structure.package-layout"


class StructurePackageLayoutValidator(ComplianceValidator):
    """Validate that the plugin is a proper package with a root manifest."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Check for __init__.py and a root-level plugin.yaml."""

        builder = EvidenceBuilder(
            plugin_id=context.plugin_descriptor.id,
            plugin_version=context.plugin_descriptor.version,
            producer=VALIDATOR_ID,
        )

        plugin_root = context.plugin_descriptor.path

        has_init = (plugin_root / "__init__.py").is_file()
        manifest_at_root = (plugin_root / "plugin.yaml").is_file()

        evidence = builder.add(
            evidence_type=EvidenceType.STRUCTURE,
            source=str(plugin_root),
            scope="filesystem",
            payload={
                "has_init": has_init,
                "manifest_at_root": manifest_at_root,
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
        """Return PASS if the layout is valid, else FAIL."""

        payload = evidence[0].payload

        if payload.get("has_init") and payload.get("manifest_at_root"):
            return RuleOutcome.PASS

        return RuleOutcome.FAIL
