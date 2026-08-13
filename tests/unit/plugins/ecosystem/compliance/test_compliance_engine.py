"""Tests for the compliance validation engine."""

from pathlib import Path

import pytest

from familyos_cli.plugins.ecosystem.compliance.compliance_domain import (
    ComplianceDomain,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_engine import (
    ComplianceEngine,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_evidence import (
    ComplianceEvidence,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_profile import (
    ComplianceProfile,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_request import (
    ComplianceRequest,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_rule import (
    ComplianceRule,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_status import (
    ComplianceStatus,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_type import (
    EvidenceType,
)
from familyos_cli.plugins.ecosystem.compliance.plugin_classification import (
    PluginClassification,
)
from familyos_cli.plugins.ecosystem.compliance.ports.compliance_validator import (
    ComplianceValidator,
)
from familyos_cli.plugins.ecosystem.compliance.profile_registry import (
    ProfileRegistry,
)
from familyos_cli.plugins.ecosystem.compliance.rule_applicability import (
    RuleApplicability,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.rule_registry import RuleRegistry
from familyos_cli.plugins.ecosystem.compliance.severity import Severity
from familyos_cli.plugins.ecosystem.compliance.validation_context import (
    ValidationContext,
)
from familyos_cli.plugins.ecosystem.compliance.validation_context_builder import (
    ValidationContextBuilder,
)
from familyos_cli.plugins.ecosystem.compliance.validator_registry import (
    ValidatorRegistry,
)
from familyos_cli.plugins.ecosystem.compliance.validator_run_result import (
    ValidatorRunResult,
)
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)
from familyos_cli.plugins.models import PluginDescriptor


class _AlwaysPassValidator(ComplianceValidator):
    def validate(self, context: ValidationContext) -> ValidatorRunResult:
        return ValidatorRunResult(status=ValidatorStatus.SUCCESS, evidence=())

    def check(self, evidence: tuple[ComplianceEvidence, ...]) -> RuleOutcome:
        return RuleOutcome.PASS


class _AlwaysFailValidator(ComplianceValidator):
    def validate(self, context: ValidationContext) -> ValidatorRunResult:
        return ValidatorRunResult(status=ValidatorStatus.SUCCESS, evidence=())

    def check(self, evidence: tuple[ComplianceEvidence, ...]) -> RuleOutcome:
        return RuleOutcome.FAIL


class _CrashingValidator(ComplianceValidator):
    def validate(self, context: ValidationContext) -> ValidatorRunResult:
        raise RuntimeError("validator implementation bug")

    def check(self, evidence: tuple[ComplianceEvidence, ...]) -> RuleOutcome:
        raise AssertionError("check() should not be reached")


_APPLIES_TO_ALL = RuleApplicability()


def _fake_rule(
    rule_id: str,
    *,
    validator_id: str,
    mandatory: bool = False,
    applicability: RuleApplicability = _APPLIES_TO_ALL,
) -> ComplianceRule:
    return ComplianceRule(
        id=rule_id,
        domain=ComplianceDomain.IDENTITY,
        title="Fake rule",
        description="Fake rule for engine tests.",
        requirement="MUST do something.",
        rationale="Testing.",
        severity=Severity.ERROR,
        applicability=applicability,
        validator_id=validator_id,
        evidence_requirements=(EvidenceType.IDENTITY,),
        remediation="Fix it.",
        mandatory=mandatory,
    )


def _plugin_descriptor(root: Path) -> PluginDescriptor:
    plugin_path = root / "fake"
    plugin_path.mkdir(parents=True)
    (plugin_path / "plugin.yaml").write_text(
        "id: familyos.fake\nname: Fake\nversion: 1.0.0\n",
        encoding="utf-8",
    )

    return PluginDescriptor(
        id="familyos.fake",
        name="Fake",
        version="1.0.0",
        module="tests.fixtures.fake.plugin",
        class_name="FakePlugin",
        path=plugin_path,
    )


def _build_engine(
    root: Path,
    *,
    rules: tuple[ComplianceRule, ...],
    mandatory_rule_ids: tuple[str, ...] = (),
) -> ComplianceEngine:
    rule_registry = RuleRegistry()
    for rule in rules:
        rule_registry.register(rule)

    profile_registry = ProfileRegistry()
    profile_registry.register(
        ComplianceProfile(
            id="official",
            version="1.0.0",
            description="Test profile.",
            included_rule_ids=tuple(rule.id for rule in rules),
            mandatory_rule_ids=mandatory_rule_ids,
        ),
    )

    validator_registry = ValidatorRegistry()
    validator_registry.register("fake.pass", _AlwaysPassValidator())
    validator_registry.register("fake.fail", _AlwaysFailValidator())
    validator_registry.register("fake.crash", _CrashingValidator())

    return ComplianceEngine(
        rule_registry=rule_registry,
        profile_registry=profile_registry,
        validator_registry=validator_registry,
        context_builder=ValidationContextBuilder(discovery_root=root),
    )


def test_all_passing_rules_yield_compliant(tmp_path: Path) -> None:
    """A plugin passing every rule yields a COMPLIANT result with no findings."""

    rules = (_fake_rule("PLUGIN-FAKE-001", validator_id="fake.pass"),)
    engine = _build_engine(tmp_path, rules=rules)

    result = engine.evaluate(
        ComplianceRequest(plugin_descriptor=_plugin_descriptor(tmp_path)),
    )

    assert result.status is ComplianceStatus.COMPLIANT
    assert result.findings == ()


def test_mandatory_failing_rule_yields_non_compliant_with_finding(
    tmp_path: Path,
) -> None:
    """A mandatory failing rule yields NON_COMPLIANT and a finding."""

    rules = (_fake_rule("PLUGIN-FAKE-002", validator_id="fake.fail"),)
    engine = _build_engine(
        tmp_path,
        rules=rules,
        mandatory_rule_ids=("PLUGIN-FAKE-002",),
    )

    result = engine.evaluate(
        ComplianceRequest(plugin_descriptor=_plugin_descriptor(tmp_path)),
    )

    assert result.status is ComplianceStatus.NON_COMPLIANT
    assert len(result.findings) == 1
    assert result.findings[0].rule_id == "PLUGIN-FAKE-002"
    assert result.mandatory_failures()[0].rule_id == "PLUGIN-FAKE-002"


def test_rule_not_applicable_to_classification_is_skipped(
    tmp_path: Path,
) -> None:
    """A rule scoped to a non-matching classification becomes NOT_APPLICABLE."""

    rules = (
        _fake_rule(
            "PLUGIN-FAKE-003",
            validator_id="fake.fail",
            applicability=RuleApplicability(
                classifications=(PluginClassification.THIRD_PARTY,),
            ),
        ),
    )
    engine = _build_engine(tmp_path, rules=rules)

    result = engine.evaluate(
        ComplianceRequest(plugin_descriptor=_plugin_descriptor(tmp_path)),
    )

    assert result.status is ComplianceStatus.COMPLIANT
    assert result.rule_evaluations[0].outcome is RuleOutcome.NOT_APPLICABLE
    assert result.findings == ()


def test_validator_crash_yields_error_status(tmp_path: Path) -> None:
    """A validator that raises unexpectedly yields an ERROR outcome and status."""

    rules = (_fake_rule("PLUGIN-FAKE-004", validator_id="fake.crash"),)
    engine = _build_engine(tmp_path, rules=rules)

    result = engine.evaluate(
        ComplianceRequest(plugin_descriptor=_plugin_descriptor(tmp_path)),
    )

    assert result.status is ComplianceStatus.ERROR
    assert result.rule_evaluations[0].outcome is RuleOutcome.ERROR
    assert result.findings[0].rule_id == "PLUGIN-FAKE-004"


def test_unknown_profile_raises(tmp_path: Path) -> None:
    """Requesting an unregistered profile raises ValueError."""

    engine = _build_engine(tmp_path, rules=())

    with pytest.raises(ValueError, match="not registered"):
        engine.evaluate(
            ComplianceRequest(
                plugin_descriptor=_plugin_descriptor(tmp_path),
                profile_id="does-not-exist",
            ),
        )
