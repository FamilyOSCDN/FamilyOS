"""Build-owned adapter for official builtin Plugin Compliance."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from familyos_cli.application.use_cases.check_plugin_compliance import (
    CheckPluginComplianceUseCase,
)
from familyos_cli.application.validation.ci_validation import (
    GateResult,
    PluginRuleSummary,
    PluginValidationSummary,
    ValidationStatus,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_status import (
    ComplianceStatus,
)
from familyos_cli.plugins.plugin_loader import PluginLoader

OFFICIAL_PROFILE_ID: Final = "official"
BUILTIN_PLUGIN_COMPLIANCE_GATE_ID: Final = "builtin-plugin-compliance"


@dataclass(frozen=True, slots=True)
class BuiltinPluginComplianceGate:
    """Evaluate every dynamically discovered builtin with official semantics."""

    use_case: CheckPluginComplianceUseCase
    plugin_loader: PluginLoader
    plugins_root: Path
    gate_id: str = BUILTIN_PLUGIN_COMPLIANCE_GATE_ID

    def execute(self) -> GateResult:
        """Discover, sort, evaluate, and aggregate all builtin plugins."""

        try:
            descriptors = sorted(
                self.plugin_loader.discover(self.plugins_root),
                key=lambda descriptor: descriptor.id,
            )
        except Exception as error:  # noqa: BLE001 - discovery boundary
            return self._error_result(f"Builtin plugin discovery failed: {error}")

        if not descriptors:
            return self._error_result("No builtin plugins were discovered.")

        plugins: list[PluginValidationSummary] = []
        gate_status = ValidationStatus.PASSED

        for descriptor in descriptors:
            try:
                report = self.use_case.execute(
                    plugin_id=descriptor.id,
                    profile_id=OFFICIAL_PROFILE_ID,
                )
            except Exception as error:  # noqa: BLE001 - application boundary
                plugins.append(
                    PluginValidationSummary(
                        plugin_id=descriptor.id,
                        plugin_version=descriptor.version,
                        status=ComplianceStatus.ERROR.value,
                        rule_outcomes=(),
                        diagnostic=f"Compliance evaluation failed: {error}",
                    ),
                )
                gate_status = ValidationStatus.ERROR
                continue

            result = report.result
            plugins.append(
                PluginValidationSummary(
                    plugin_id=result.plugin_id,
                    plugin_version=result.plugin_version,
                    status=result.status.value,
                    rule_outcomes=tuple(
                        PluginRuleSummary(
                            rule_id=evaluation.rule_id,
                            outcome=evaluation.outcome.value,
                            severity=evaluation.severity.value,
                        )
                        for evaluation in result.rule_evaluations
                    ),
                ),
            )

            if result.status is ComplianceStatus.ERROR:
                gate_status = ValidationStatus.ERROR
            elif (
                result.status is not ComplianceStatus.COMPLIANT
                and gate_status is ValidationStatus.PASSED
            ):
                gate_status = ValidationStatus.FAILED

        return GateResult(
            gate_id=self.gate_id,
            status=gate_status,
            profile_id=OFFICIAL_PROFILE_ID,
            plugins=tuple(plugins),
        )

    def _error_result(self, diagnostic: str) -> GateResult:
        return GateResult(
            gate_id=self.gate_id,
            status=ValidationStatus.ERROR,
            diagnostic=diagnostic,
            profile_id=OFFICIAL_PROFILE_ID,
        )
