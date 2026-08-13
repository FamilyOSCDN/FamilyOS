"""Tests for the check plugin compliance use case."""

from __future__ import annotations

from pathlib import Path

import pytest

from familyos_cli.application.use_cases.check_plugin_compliance import (
    CheckPluginComplianceUseCase,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_engine import (
    ComplianceEngine,
)
from familyos_cli.plugins.ecosystem.compliance.profiles.default_profile_registry import (
    build_default_profile_registry,
)
from familyos_cli.plugins.ecosystem.compliance.rule_registry import RuleRegistry
from familyos_cli.plugins.ecosystem.compliance.rules.default_rule_catalog import (
    DEFAULT_COMPLIANCE_RULES,
)
from familyos_cli.plugins.ecosystem.compliance.validation_context_builder import (
    ValidationContextBuilder,
)
from familyos_cli.plugins.ecosystem.compliance.validators.default_validator_registry import (
    build_default_validator_registry,
)
from familyos_cli.plugins.plugin_loader import PluginLoader


def _build_use_case(plugins_root: Path) -> CheckPluginComplianceUseCase:
    rule_registry = RuleRegistry()
    for rule in DEFAULT_COMPLIANCE_RULES:
        rule_registry.register(rule)

    profile_registry = build_default_profile_registry()

    engine = ComplianceEngine(
        rule_registry=rule_registry,
        profile_registry=profile_registry,
        validator_registry=build_default_validator_registry(),
        context_builder=ValidationContextBuilder(discovery_root=plugins_root),
    )

    return CheckPluginComplianceUseCase(
        engine=engine,
        profile_registry=profile_registry,
        plugin_loader=PluginLoader(),
        plugins_root=plugins_root,
    )


def _write_plugin(plugins_root: Path) -> None:
    plugin_path = plugins_root / "sample"
    plugin_path.mkdir(parents=True)
    (plugin_path / "__init__.py").write_text("", encoding="utf-8")
    (plugin_path / "plugin.yaml").write_text(
        (
            "id: familyos.sample\n"
            "name: Sample\n"
            "version: 1.0.0\n"
            "author: FamilyOS Team\n"
            "description: A sample plugin used for use case tests.\n"
            "module: tests.fixtures.sample_plugin.plugin\n"
            "class: SamplePlugin\n"
            "enabled: true\n"
        ),
        encoding="utf-8",
    )


def test_execute_raises_for_unknown_plugin(tmp_path: Path) -> None:
    """execute() raises ValueError when the plugin id is not discoverable."""

    use_case = _build_use_case(tmp_path)

    with pytest.raises(ValueError, match="was not found"):
        use_case.execute(plugin_id="familyos.does-not-exist")


def test_execute_returns_report_for_known_plugin(tmp_path: Path) -> None:
    """execute() returns a ComplianceReport for a discoverable plugin."""

    _write_plugin(tmp_path)

    use_case = _build_use_case(tmp_path)

    report = use_case.execute(plugin_id="familyos.sample")

    assert report.result.plugin_id == "familyos.sample"
    assert report.profile_version == "1.0.0"
