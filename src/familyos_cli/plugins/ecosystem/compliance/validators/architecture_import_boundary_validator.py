"""Validator for PLUGIN-ARCH-001."""

from __future__ import annotations

import ast

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

VALIDATOR_ID = "architecture.import-boundary"

_FORBIDDEN_PREFIXES = (
    "familyos_cli.interfaces",
    "familyos_cli.application",
)


def _imported_modules(tree: ast.Module) -> list[str]:
    """Return every module name imported by the given AST module."""

    modules: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)

    return modules


class ArchitectureImportBoundaryValidator(ComplianceValidator):
    """Validate that plugin domain code does not import outer layers."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Scan the plugin's domain/ subpackage for forbidden imports."""

        builder = EvidenceBuilder(
            plugin_id=context.plugin_descriptor.id,
            plugin_version=context.plugin_descriptor.version,
            producer=VALIDATOR_ID,
        )

        domain_dir = context.plugin_descriptor.path / "domain"

        if not domain_dir.is_dir():
            evidence = builder.add(
                evidence_type=EvidenceType.ARCHITECTURE,
                source=str(domain_dir),
                scope="filesystem",
                payload={"applicable": False},
            )

            return ValidatorRunResult(
                status=ValidatorStatus.SUCCESS,
                evidence=(evidence,),
            )

        violations: list[str] = []

        for source_file in sorted(domain_dir.rglob("*.py")):
            tree = ast.parse(
                source_file.read_text(encoding="utf-8"),
                filename=str(source_file),
            )

            for module in _imported_modules(tree):
                if module.startswith(_FORBIDDEN_PREFIXES):
                    violations.append(f"{source_file}: {module}")

        evidence = builder.add(
            evidence_type=EvidenceType.ARCHITECTURE,
            source=str(domain_dir),
            scope="filesystem",
            payload={"applicable": True, "violations": violations},
        )

        return ValidatorRunResult(
            status=ValidatorStatus.SUCCESS,
            evidence=(evidence,),
        )

    def check(
        self,
        evidence: tuple[ComplianceEvidence, ...],
    ) -> RuleOutcome:
        """Return the outcome of the import boundary check."""

        payload = evidence[0].payload

        if not payload.get("applicable"):
            return RuleOutcome.NOT_APPLICABLE

        if payload.get("violations"):
            return RuleOutcome.FAIL

        return RuleOutcome.PASS
