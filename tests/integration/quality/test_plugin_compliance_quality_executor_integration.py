"""Real integration tests for Quality normalization of Plugin Compliance."""

from __future__ import annotations

from itertools import count
from pathlib import Path

from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityDomain,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityFindingId,
    QualityRule,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.infrastructure.quality.plugin_compliance_quality_executor import (
    PluginComplianceQualityExecutor,
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

_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
_BUILTIN_PLUGINS_ROOT = (
    _REPOSITORY_ROOT / "src" / "familyos_cli" / "plugins" / "builtin"
)


def _build_engine(discovery_root: Path) -> ComplianceEngine:
    """Compose the authoritative Plugin Compliance implementation."""

    rule_registry = RuleRegistry()
    for rule in DEFAULT_COMPLIANCE_RULES:
        rule_registry.register(rule)

    return ComplianceEngine(
        rule_registry=rule_registry,
        profile_registry=build_default_profile_registry(),
        validator_registry=build_default_validator_registry(),
        context_builder=ValidationContextBuilder(discovery_root=discovery_root),
    )


def _rule() -> QualityRule:
    return QualityRule(
        id=QualityRuleId("QLT-RULE-PLUGIN-COMPLIANCE-INTEGRATION"),
        requirement_id=None,
        domain=QualityDomain("QLT-DOM-PLUGIN"),
        severity=QualitySeverity.HIGH,
        description="Plugin must satisfy authoritative official compliance policy",
        executor="plugin_compliance",
    )


def _executor(plugins_root: Path) -> PluginComplianceQualityExecutor:
    finding_ids = count(1)
    evidence_ids = count(1)
    return PluginComplianceQualityExecutor(
        engine=_build_engine(plugins_root),
        plugin_loader=PluginLoader(),
        plugins_root=plugins_root,
        finding_id_factory=lambda: QualityFindingId(
            f"QLT-FIND-PLUGIN-INT-{next(finding_ids):03d}"
        ),
        evidence_id_factory=lambda: QualityEvidenceId(
            f"QLT-EVID-PLUGIN-INT-{next(evidence_ids):03d}"
        ),
    )


def _target(
    *,
    identifier: str,
    version: str,
    path: Path,
    revision: str,
) -> QualityTarget:
    return QualityTarget(
        target_type="plugin",
        identifier=identifier,
        version=version,
        path=str(path),
        revision=revision,
    )


def test_real_official_security_plugin_normalizes_compliance_pass() -> None:
    """A real official builtin passes through the authoritative engine."""

    descriptors = PluginLoader().discover(_BUILTIN_PLUGINS_ROOT)
    descriptor = next(d for d in descriptors if d.id == "familyos.security")
    rule = _rule()
    target = _target(
        identifier=descriptor.id,
        version=descriptor.version,
        path=descriptor.path,
        revision="integration-security-revision",
    )

    result = _executor(_BUILTIN_PLUGINS_ROOT).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-INTEGRATION-PASS"),
        rule=rule,
        target=target,
    )

    assert result.status is QualityStatus.PASS
    assert result.findings == ()
    assert result.diagnostics == ()
    assert result.evidence

    for evidence in result.evidence:
        metadata = dict(evidence.metadata)
        assert evidence.type.value == "COMPLIANCE"
        assert evidence.source == "quality.plugin_compliance"
        assert evidence.result is QualityEvidenceResult.PASS
        assert evidence.target == target
        assert evidence.revision == "integration-security-revision"
        assert evidence.rule_id == rule.id
        assert evidence.requirement_id == rule.requirement_id
        assert metadata["compliance_profile_id"] == "official"
        assert metadata["plugin_id"] == descriptor.id
        assert metadata["plugin_version"] == descriptor.version
        assert metadata["source_evidence_id"]
        assert metadata["source_evidence_type"]
        assert metadata["producer"]
        assert metadata["scope"]
        assert metadata["trust_level"]
        assert metadata["compliance_evaluation_id"]

    assert result.duration_seconds >= 0.0


def test_real_non_compliant_plugin_normalizes_findings_and_evidence(
    tmp_path: Path,
) -> None:
    """A genuinely non-compliant plugin is normalized without policy replay."""

    plugin_path = tmp_path / "broken"
    plugin_path.mkdir()
    (plugin_path / "plugin.yaml").write_text(
        (
            "id: acme.broken\n"
            "name: \n"
            "version: not-a-version\n"
            "author: Someone\n"
            "description: short\n"
            "module: tests.fixtures.does_not_exist.plugin\n"
            "class: Nope\n"
            "enabled: true\n"
        ),
        encoding="utf-8",
    )

    descriptors = PluginLoader().discover(tmp_path)
    descriptor = next(d for d in descriptors if d.id == "acme.broken")
    rule = _rule()
    target = _target(
        identifier=descriptor.id,
        version=descriptor.version,
        path=descriptor.path,
        revision="integration-broken-revision",
    )

    result = _executor(tmp_path).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-INTEGRATION-FAIL"),
        rule=rule,
        target=target,
    )

    assert result.status is QualityStatus.FAIL
    assert result.findings
    assert result.evidence
    assert result.diagnostics

    evidence_ids = {str(evidence.id) for evidence in result.evidence}
    source_rule_ids: set[str] = set()

    for evidence in result.evidence:
        metadata = dict(evidence.metadata)
        assert evidence.type.value == "COMPLIANCE"
        assert evidence.source == "quality.plugin_compliance"
        assert evidence.result is QualityEvidenceResult.FAIL
        assert evidence.target == target
        assert evidence.revision == "integration-broken-revision"
        assert evidence.rule_id == rule.id
        assert metadata["compliance_profile_id"] == "official"
        assert metadata["plugin_id"] == descriptor.id
        assert metadata["plugin_version"] == descriptor.version
        assert metadata["compliance_evaluation_id"]
        assert metadata["source_evidence_id"]

    for finding in result.findings:
        assert finding.rule_id == rule.id
        assert finding.domain == rule.domain
        assert finding.severity == rule.severity
        assert finding.status is QualityStatus.FAIL
        assert finding.target == target
        assert set(finding.evidence_ids).issubset(evidence_ids)
        assert "[plugin_rule=PLUGIN-" in finding.message

    for diagnostic in result.diagnostics:
        assert diagnostic.startswith("plugin_compliance_finding:")
        marker = "rule_id="
        start = diagnostic.index(marker) + len(marker)
        end = diagnostic.index(";", start)
        source_rule_ids.add(diagnostic[start:end])

    assert "PLUGIN-IDENT-003" in source_rule_ids
    assert "PLUGIN-META-001" in source_rule_ids
    assert "PLUGIN-META-002" in source_rule_ids
    assert "PLUGIN-META-003" in source_rule_ids
    assert "PLUGIN-STRUCT-001" in source_rule_ids
    assert "PLUGIN-STRUCT-002" in source_rule_ids
    assert result.duration_seconds >= 0.0
