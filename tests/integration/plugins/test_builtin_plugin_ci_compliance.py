"""Integration tests for builtin Plugin Compliance in canonical CI validation."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.validation import ValidationStatus
from familyos_cli.application.validation.builtin_plugin_compliance_gate import (
    BuiltinPluginComplianceGate,
)
from familyos_cli.bootstrap.container import ApplicationContainer
from familyos_cli.plugins.ecosystem.compliance.compliance_status import (
    ComplianceStatus,
)
from familyos_cli.plugins.plugin_loader import PluginLoader

_BUILTIN_PLUGINS_ROOT = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "familyos_cli"
    / "plugins"
    / "builtin"
)


def test_ci_gate_matches_direct_official_compliance_for_every_builtin() -> None:
    container = ApplicationContainer()
    use_case = container.check_plugin_compliance_use_case()
    loader = PluginLoader()
    descriptors = sorted(
        loader.discover(_BUILTIN_PLUGINS_ROOT),
        key=lambda descriptor: descriptor.id,
    )
    gate = BuiltinPluginComplianceGate(
        use_case=use_case,
        plugin_loader=loader,
        plugins_root=_BUILTIN_PLUGINS_ROOT,
    )

    gate_result = gate.execute()

    assert descriptors
    assert gate_result.status is ValidationStatus.PASSED
    assert gate_result.profile_id == "official"
    assert [plugin.plugin_id for plugin in gate_result.plugins] == [
        descriptor.id for descriptor in descriptors
    ]

    for plugin_summary in gate_result.plugins:
        direct_report = use_case.execute(
            plugin_id=plugin_summary.plugin_id,
            profile_id="official",
        )
        assert direct_report.result.status is ComplianceStatus.COMPLIANT
        assert plugin_summary.status == direct_report.result.status.value
        assert [
            (rule.rule_id, rule.outcome, rule.severity)
            for rule in plugin_summary.rule_outcomes
        ] == [
            (
                evaluation.rule_id,
                evaluation.outcome.value,
                evaluation.severity.value,
            )
            for evaluation in direct_report.result.rule_evaluations
        ]
