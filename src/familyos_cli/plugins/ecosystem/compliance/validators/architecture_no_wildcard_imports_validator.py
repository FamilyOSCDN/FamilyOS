"""Validator for PLUGIN-ARCH-002."""

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

VALIDATOR_ID = "architecture.no-wildcard-imports"


class ArchitectureNoWildcardImportsValidator(ComplianceValidator):
    """Validate that no plugin source file uses wildcard imports."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Scan the plugin package tree for wildcard imports."""

        builder = EvidenceBuilder(
            plugin_id=context.plugin_descriptor.id,
            plugin_version=context.plugin_descriptor.version,
            producer=VALIDATOR_ID,
        )

        plugin_root = context.plugin_descriptor.path

        violations: list[str] = []

        for source_file in sorted(plugin_root.rglob("*.py")):
            tree = ast.parse(
                source_file.read_text(encoding="utf-8"),
                filename=str(source_file),
            )

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and any(
                    alias.name == "*" for alias in node.names
                ):
                    violations.append(f"{source_file}: from {node.module} import *")

        evidence = builder.add(
            evidence_type=EvidenceType.ARCHITECTURE,
            source=str(plugin_root),
            scope="filesystem",
            payload={"violations": violations},
        )

        return ValidatorRunResult(
            status=ValidatorStatus.SUCCESS,
            evidence=(evidence,),
        )

    def check(
        self,
        evidence: tuple[ComplianceEvidence, ...],
    ) -> RuleOutcome:
        """Return the outcome of the wildcard import check."""

        if evidence[0].payload.get("violations"):
            return RuleOutcome.FAIL

        return RuleOutcome.PASS
