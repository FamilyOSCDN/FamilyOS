"""Integration tests for the plugin compliance validation pipeline."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.compliance_engine import (
    ComplianceEngine,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_request import (
    ComplianceRequest,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_status import (
    ComplianceStatus,
)
from familyos_cli.plugins.ecosystem.compliance.finding_category import (
    FindingCategory,
)
from familyos_cli.plugins.ecosystem.compliance.profiles.default_profile_registry import (
    build_default_profile_registry,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
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

_BUILTIN_PLUGINS_ROOT = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "familyos_cli"
    / "plugins"
    / "builtin"
)


def _build_engine(discovery_root: Path) -> ComplianceEngine:
    rule_registry = RuleRegistry()
    for rule in DEFAULT_COMPLIANCE_RULES:
        rule_registry.register(rule)

    return ComplianceEngine(
        rule_registry=rule_registry,
        profile_registry=build_default_profile_registry(),
        validator_registry=build_default_validator_registry(),
        context_builder=ValidationContextBuilder(discovery_root=discovery_root),
    )


def test_official_security_plugin_is_fully_compliant() -> None:
    """The real official security plugin passes the full official profile."""

    engine = _build_engine(_BUILTIN_PLUGINS_ROOT)

    descriptors = PluginLoader().discover(_BUILTIN_PLUGINS_ROOT)
    descriptor = next(d for d in descriptors if d.id == "familyos.security")

    result = engine.evaluate(ComplianceRequest(plugin_descriptor=descriptor))

    assert result.status is ComplianceStatus.COMPLIANT
    assert result.findings == ()

    outcomes_by_rule = {
        evaluation.rule_id: evaluation.outcome
        for evaluation in result.rule_evaluations
    }

    assert outcomes_by_rule["PLUGIN-DEP-001"] is RuleOutcome.NOT_APPLICABLE
    assert outcomes_by_rule["PLUGIN-DEP-002"] is RuleOutcome.NOT_APPLICABLE

    for rule_id, outcome in outcomes_by_rule.items():
        if rule_id in ("PLUGIN-DEP-001", "PLUGIN-DEP-002"):
            continue
        assert outcome is RuleOutcome.PASS, (rule_id, outcome)


def test_deliberately_broken_plugin_is_non_compliant(tmp_path: Path) -> None:
    """A plugin violating several rules at once is reported NON_COMPLIANT."""

    plugin_path = tmp_path / "broken"
    plugin_path.mkdir()
    # Deliberately omit __init__.py (violates PLUGIN-STRUCT-002). The id is
    # kept canonical ("acme.broken") because PluginLoader/PluginDescriptor
    # already enforce canonical Plugin Identifier format eagerly at
    # discovery time; a non-canonical id would fail discovery itself
    # rather than surfacing as a PLUGIN-IDENT-002 compliance finding
    # (that FAIL path is covered directly at the validator unit-test
    # level instead). "acme.broken" still violates the mandatory
    # PLUGIN-IDENT-003 official-namespace rule.
    (plugin_path / "plugin.yaml").write_text(
        (
            "id: acme.broken\n"  # violates PLUGIN-IDENT-003 (mandatory)
            "name: \n"  # violates PLUGIN-META-001
            "version: not-a-version\n"  # violates PLUGIN-META-002
            "author: Someone\n"
            "description: short\n"  # violates PLUGIN-META-003
            "module: tests.fixtures.does_not_exist.plugin\n"  # violates STRUCT-001
            "class: Nope\n"
            "enabled: true\n"
        ),
        encoding="utf-8",
    )

    engine = _build_engine(tmp_path)

    descriptors = PluginLoader().discover(tmp_path)
    descriptor = next(d for d in descriptors if d.id == "acme.broken")

    result = engine.evaluate(ComplianceRequest(plugin_descriptor=descriptor))

    assert result.status is ComplianceStatus.NON_COMPLIANT

    findings_by_rule = {finding.rule_id: finding for finding in result.findings}

    assert "PLUGIN-IDENT-003" in findings_by_rule
    assert findings_by_rule["PLUGIN-IDENT-003"].category is FindingCategory.VIOLATION

    assert "PLUGIN-META-001" in findings_by_rule
    assert "PLUGIN-META-002" in findings_by_rule
    assert "PLUGIN-META-003" in findings_by_rule
    assert "PLUGIN-STRUCT-001" in findings_by_rule
    assert "PLUGIN-STRUCT-002" in findings_by_rule

    # Rules depending on a successfully loaded plugin instance must not be
    # reported as ordinary violations when the entry point itself failed.
    assert findings_by_rule["PLUGIN-STRUCT-003"].category is FindingCategory.INCOMPLETE
    assert findings_by_rule["PLUGIN-CAP-001"].category is FindingCategory.INCOMPLETE
