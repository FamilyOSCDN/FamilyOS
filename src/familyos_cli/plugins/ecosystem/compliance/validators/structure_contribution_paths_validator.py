"""Validator for PLUGIN-STRUCT-003."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.contributions.template_contribution import (
    TemplateContribution,
)
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

VALIDATOR_ID = "structure.contribution-paths"


def _find_repo_root(start: Path) -> Path | None:
    """Walk upward from start until a directory containing pyproject.toml."""

    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate

    return None


class StructureContributionPathsValidator(ComplianceValidator):
    """Validate that declared template contribution paths exist on disk."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Resolve every template contribution path and check existence."""

        builder = EvidenceBuilder(
            plugin_id=context.plugin_descriptor.id,
            plugin_version=context.plugin_descriptor.version,
            producer=VALIDATOR_ID,
        )

        try:
            plugin = load_plugin_instance(context.plugin_descriptor)
        except Exception:  # noqa: BLE001 - expected plugin-author failure path
            evidence = builder.add(
                evidence_type=EvidenceType.STRUCTURE,
                source="runtime",
                scope="runtime",
                payload={"loaded": False},
            )

            return ValidatorRunResult(
                status=ValidatorStatus.SUCCESS,
                evidence=(evidence,),
            )

        repo_root = _find_repo_root(context.plugin_descriptor.path.resolve())

        missing: list[str] = []
        checked: list[str] = []

        for contribution in plugin.contributions():
            if not isinstance(contribution, TemplateContribution):
                continue

            candidate = contribution.template_directory

            resolved = (
                candidate
                if candidate.is_absolute()
                else (repo_root or Path.cwd()) / candidate
            )

            checked.append(str(candidate))

            if not resolved.is_dir():
                missing.append(str(candidate))

        evidence = builder.add(
            evidence_type=EvidenceType.STRUCTURE,
            source="contributions",
            scope="filesystem",
            payload={
                "loaded": True,
                "checked": checked,
                "missing": missing,
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
        """Return the outcome of the contribution path check."""

        payload = evidence[0].payload

        if not payload.get("loaded"):
            return RuleOutcome.NOT_EVALUATED

        if payload.get("missing"):
            return RuleOutcome.FAIL

        return RuleOutcome.PASS
