"""Validator for PLUGIN-QLT-002."""

from __future__ import annotations

import json
import subprocess

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

VALIDATOR_ID = "quality.mypy"

_TIMEOUT_SECONDS = 120
_TRUSTWORTHY_EXIT_CODES = (0, 1)


class QualityMypyValidator(ComplianceValidator):
    """Validate that the plugin source subtree passes MyPy with zero type errors."""

    def validate(
        self,
        context: ValidationContext,
    ) -> ValidatorRunResult:
        """Execute MyPy against the plugin source subtree."""

        plugin_root = context.plugin_descriptor.path

        if not any(plugin_root.rglob("*.py")):
            builder = EvidenceBuilder(
                plugin_id=context.plugin_descriptor.id,
                plugin_version=context.plugin_descriptor.version,
                producer=VALIDATOR_ID,
            )

            evidence = builder.add(
                evidence_type=EvidenceType.QUALITY,
                source=str(plugin_root),
                scope="mypy",
                payload={"exit_code": 0, "errors": []},
            )

            return ValidatorRunResult(
                status=ValidatorStatus.SUCCESS,
                evidence=(evidence,),
                message="No Python source files found; nothing to type-check.",
            )

        try:
            process = subprocess.run(
                ["mypy", str(plugin_root), "--output=json"],
                capture_output=True,
                text=True,
                timeout=_TIMEOUT_SECONDS,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            return ValidatorRunResult(
                status=ValidatorStatus.ERROR,
                evidence=(),
                message=f"MyPy execution failed: {error}",
            )

        if process.returncode not in _TRUSTWORTHY_EXIT_CODES:
            return ValidatorRunResult(
                status=ValidatorStatus.ERROR,
                evidence=(),
                message=(
                    f"MyPy exited with unexpected status {process.returncode}: "
                    f"{process.stderr.strip()}"
                ),
            )

        errors: list[object] = []

        try:
            for line in process.stdout.splitlines():
                line = line.strip()
                if line:
                    errors.append(json.loads(line))
        except json.JSONDecodeError as error:
            return ValidatorRunResult(
                status=ValidatorStatus.ERROR,
                evidence=(),
                message=f"MyPy produced unparseable output: {error}",
            )

        builder = EvidenceBuilder(
            plugin_id=context.plugin_descriptor.id,
            plugin_version=context.plugin_descriptor.version,
            producer=VALIDATOR_ID,
        )

        evidence = builder.add(
            evidence_type=EvidenceType.QUALITY,
            source=str(plugin_root),
            scope="mypy",
            payload={
                "exit_code": process.returncode,
                "errors": errors,
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
        """Return PASS if MyPy reported zero type errors, else FAIL."""

        if evidence[0].payload.get("exit_code") == 0:
            return RuleOutcome.PASS

        return RuleOutcome.FAIL
