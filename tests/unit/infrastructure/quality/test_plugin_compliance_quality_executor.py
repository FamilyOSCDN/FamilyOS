from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import pytest

from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityDomain,
    QualityEvidenceId,
    QualityFindingId,
    QualityRequirementId,
    QualityRule,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.infrastructure.quality.plugin_compliance_quality_executor import (
    PluginComplianceQualityExecutor,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_domain import ComplianceDomain
from familyos_cli.plugins.ecosystem.compliance.compliance_engine import ComplianceEngine
from familyos_cli.plugins.ecosystem.compliance.compliance_evidence import (
    ComplianceEvidence,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_finding import (
    ComplianceFinding,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_result import ComplianceResult
from familyos_cli.plugins.ecosystem.compliance.compliance_status import ComplianceStatus
from familyos_cli.plugins.ecosystem.compliance.evidence_trust_level import (
    EvidenceTrustLevel,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_type import EvidenceType
from familyos_cli.plugins.ecosystem.compliance.finding_category import FindingCategory
from familyos_cli.plugins.ecosystem.compliance.finding_status import FindingStatus
from familyos_cli.plugins.ecosystem.compliance.severity import Severity
from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin_loader import PluginLoader


class FakeEngine:
    def __init__(self, outcome: ComplianceResult | Exception) -> None:
        self.outcome = outcome

    def evaluate(self, request: object) -> ComplianceResult:
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return self.outcome


class FakeLoader:
    def __init__(self, item: PluginDescriptor) -> None:
        self.item = item

    def discover(self, directory: Path) -> list[PluginDescriptor]:
        return [self.item]


def descriptor(tmp_path: Path) -> PluginDescriptor:
    p = tmp_path / "sample"
    p.mkdir()
    return PluginDescriptor(
        id="familyos.sample",
        name="Sample",
        version="1.0.0",
        author="FamilyOS",
        description="Sample",
        module="sample.plugin",
        class_name="SamplePlugin",
        path=p,
    )


def target(d: PluginDescriptor) -> QualityTarget:
    return QualityTarget(
        "plugin", d.id, revision="abc123", version=d.version, path=str(d.path)
    )


def rule() -> QualityRule:
    return QualityRule(
        QualityRuleId("QLT-RULE-PLUGIN-COMPLIANCE"),
        QualityRequirementId("QLT-REQ-PLUGIN-COMPLIANCE"),
        QualityDomain("QLT-DOM-CPL"),
        QualitySeverity.HIGH,
        "Official plugin compliance",
        "plugin_compliance",
    )


def evidence() -> ComplianceEvidence:
    return ComplianceEvidence(
        id="source-evidence-1",
        type=EvidenceType.QUALITY,
        source="ruff",
        producer="ruff-validator",
        producer_version="1.2.3",
        plugin_id="familyos.sample",
        plugin_version="1.0.0",
        scope="plugin",
        payload={"passed": True},
        trust_level=EvidenceTrustLevel.LOCAL,
        collected_at=datetime(2026, 9, 1, 20, 0, tzinfo=UTC),
    )


def finding(severity: Severity = Severity.ERROR) -> ComplianceFinding:
    return ComplianceFinding(
        id="source-finding-1",
        evaluation_id="evaluation-1",
        rule_id="PLUGIN-QLT-001",
        domain=ComplianceDomain.QUALITY,
        severity=severity,
        category=FindingCategory.VIOLATION,
        status=FindingStatus.OPEN,
        title="Quality violation",
        message="Plugin quality rule failed.",
        evidence_refs=("source-evidence-1",),
        location="plugin.yaml",
        remediation="Fix it.",
    )


def result(
    status: ComplianceStatus,
    *,
    findings: tuple[ComplianceFinding, ...] = (),
    evidence_items: tuple[ComplianceEvidence, ...] = (),
) -> ComplianceResult:
    now = datetime(2026, 9, 1, 20, 0, tzinfo=UTC)
    return ComplianceResult(
        "evaluation-1",
        "familyos.sample",
        "1.0.0",
        "official",
        status,
        (),
        findings,
        evidence_items,
        now,
        now,
    )


def executor(
    tmp_path: Path, outcome: ComplianceResult | Exception, d: PluginDescriptor
) -> PluginComplianceQualityExecutor:
    fids = iter(QualityFindingId(f"QLT-FIND-PLUGIN-{n}") for n in range(1, 20))
    eids = iter(QualityEvidenceId(f"QLT-EVID-PLUGIN-{n}") for n in range(1, 20))
    times = iter((10.0, 10.25))
    return PluginComplianceQualityExecutor(
        engine=cast(ComplianceEngine, FakeEngine(outcome)),
        plugin_loader=cast(PluginLoader, FakeLoader(d)),
        plugins_root=tmp_path,
        finding_id_factory=lambda: next(fids),
        evidence_id_factory=lambda: next(eids),
        monotonic_clock=lambda: next(times),
    )


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (ComplianceStatus.COMPLIANT, QualityStatus.PASS),
        (ComplianceStatus.NON_COMPLIANT, QualityStatus.FAIL),
        (ComplianceStatus.INCOMPLETE, QualityStatus.WARNING),
        (ComplianceStatus.ERROR, QualityStatus.ERROR),
    ],
)
def test_status_mapping(
    tmp_path: Path, source: ComplianceStatus, expected: QualityStatus
) -> None:
    d = descriptor(tmp_path)
    actual = executor(tmp_path, result(source), d).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-1"), rule=rule(), target=target(d)
    )
    assert actual.status is expected
    assert actual.duration_seconds == pytest.approx(0.25)


@pytest.mark.parametrize("severity", tuple(Severity))
def test_severity_and_rule_provenance(tmp_path: Path, severity: Severity) -> None:
    d = descriptor(tmp_path)
    actual = executor(
        tmp_path,
        result(
            ComplianceStatus.NON_COMPLIANT,
            findings=(finding(severity),),
            evidence_items=(evidence(),),
        ),
        d,
    ).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-2"), rule=rule(), target=target(d)
    )
    qf = actual.findings[0]
    assert qf.rule_id == rule().id
    assert qf.severity is QualitySeverity.HIGH
    assert f"plugin_severity={severity.value}" in qf.message
    assert "plugin_rule=PLUGIN-QLT-001" in qf.message
    assert qf.evidence_ids == ("QLT-EVID-PLUGIN-1",)


def test_evidence_provenance_and_revision(tmp_path: Path) -> None:
    d = descriptor(tmp_path)
    actual = executor(
        tmp_path, result(ComplianceStatus.COMPLIANT, evidence_items=(evidence(),)), d
    ).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-3"), rule=rule(), target=target(d)
    )
    qe = actual.evidence[0]
    md = dict(qe.metadata)
    assert qe.type.value == "COMPLIANCE"
    assert qe.revision == "abc123"
    assert qe.rule_id == rule().id
    assert md["source_evidence_id"] == "source-evidence-1"
    assert md["plugin_id"] == "familyos.sample"
    assert md["trust_level"] == "local"


def test_engine_failure_is_error(tmp_path: Path) -> None:
    d = descriptor(tmp_path)
    actual = executor(tmp_path, RuntimeError("boom"), d).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-4"), rule=rule(), target=target(d)
    )
    assert actual.status is QualityStatus.ERROR
    assert "boom" in actual.diagnostics[0]


def test_unknown_evidence_reference_is_error(tmp_path: Path) -> None:
    d = descriptor(tmp_path)
    actual = executor(
        tmp_path, result(ComplianceStatus.NON_COMPLIANT, findings=(finding(),)), d
    ).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-5"), rule=rule(), target=target(d)
    )
    assert actual.status is QualityStatus.ERROR
    assert "unknown evidence" in actual.diagnostics[0]


def test_invalid_target_type_is_error(tmp_path: Path) -> None:
    d = descriptor(tmp_path)
    actual = executor(tmp_path, result(ComplianceStatus.COMPLIANT), d).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-6"),
        rule=rule(),
        target=QualityTarget("repository", d.id, path=str(d.path)),
    )
    assert actual.status is QualityStatus.ERROR


def test_full_finding_provenance_is_preserved(tmp_path: Path) -> None:
    d = descriptor(tmp_path)
    actual = executor(
        tmp_path,
        result(
            ComplianceStatus.NON_COMPLIANT,
            findings=(finding(),),
            evidence_items=(evidence(),),
        ),
        d,
    ).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-7"),
        rule=rule(),
        target=target(d),
    )
    diagnostic = actual.diagnostics[0]
    assert "id=source-finding-1" in diagnostic
    assert "evaluation_id=evaluation-1" in diagnostic
    assert "rule_id=PLUGIN-QLT-001" in diagnostic
    assert "domain=quality" in diagnostic
    assert "severity=error" in diagnostic
    assert "category=violation" in diagnostic
    assert "status=open" in diagnostic
    assert "title=Quality violation" in diagnostic
    assert "remediation=Fix it." in diagnostic
    assert "evidence_refs=source-evidence-1" in diagnostic


def test_evidence_preserves_evaluation_and_profile(tmp_path: Path) -> None:
    d = descriptor(tmp_path)
    actual = executor(
        tmp_path,
        result(ComplianceStatus.COMPLIANT, evidence_items=(evidence(),)),
        d,
    ).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-8"),
        rule=rule(),
        target=target(d),
    )
    metadata = dict(actual.evidence[0].metadata)
    assert metadata["compliance_evaluation_id"] == "evaluation-1"
    assert metadata["compliance_profile_id"] == "official"


def test_plugin_not_found_is_error(tmp_path: Path) -> None:
    d = descriptor(tmp_path)
    missing = QualityTarget(
        "plugin", "familyos.missing", version="1.0.0", path=str(tmp_path / "missing")
    )
    actual = executor(tmp_path, result(ComplianceStatus.COMPLIANT), d).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-9"), rule=rule(), target=missing
    )
    assert actual.status is QualityStatus.ERROR
    assert "was not found" in actual.diagnostics[0]


def test_target_path_mismatch_is_error(tmp_path: Path) -> None:
    d = descriptor(tmp_path)
    bad = QualityTarget("plugin", d.id, version=d.version, path=str(tmp_path / "other"))
    actual = executor(tmp_path, result(ComplianceStatus.COMPLIANT), d).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-10"), rule=rule(), target=bad
    )
    assert actual.status is QualityStatus.ERROR
    assert "path" in actual.diagnostics[0]


def test_target_version_mismatch_is_error(tmp_path: Path) -> None:
    d = descriptor(tmp_path)
    bad = QualityTarget("plugin", d.id, version="9.9.9", path=str(d.path))
    actual = executor(tmp_path, result(ComplianceStatus.COMPLIANT), d).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-11"), rule=rule(), target=bad
    )
    assert actual.status is QualityStatus.ERROR
    assert "version" in actual.diagnostics[0]


@pytest.mark.parametrize(
    ("plugin_id", "plugin_version", "profile_id", "signal"),
    [
        ("familyos.other", "1.0.0", "official", "plugin id"),
        ("familyos.sample", "9.9.9", "official", "plugin version"),
        ("familyos.sample", "1.0.0", "other", "profile"),
    ],
)
def test_inconsistent_result_is_error(
    tmp_path: Path,
    plugin_id: str,
    plugin_version: str,
    profile_id: str,
    signal: str,
) -> None:
    d = descriptor(tmp_path)
    now = datetime(2026, 9, 1, 20, 0, tzinfo=UTC)
    bad_result = ComplianceResult(
        "evaluation-1",
        plugin_id,
        plugin_version,
        profile_id,
        ComplianceStatus.COMPLIANT,
        (),
        (),
        (),
        now,
        now,
    )
    actual = executor(tmp_path, bad_result, d).execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-12"), rule=rule(), target=target(d)
    )
    assert actual.status is QualityStatus.ERROR
    assert signal in actual.diagnostics[0]


def test_authoritative_engine_receives_canonical_descriptor_and_official_profile(
    tmp_path: Path,
) -> None:
    from familyos_cli.plugins.ecosystem.compliance.compliance_request import (
        ComplianceRequest,
    )

    d = descriptor(tmp_path)

    class RecordingEngine:
        def __init__(self) -> None:
            self.request: ComplianceRequest | None = None

        def evaluate(self, request: ComplianceRequest) -> ComplianceResult:
            self.request = request
            return result(ComplianceStatus.COMPLIANT)

    recording = RecordingEngine()
    times = iter((10.0, 10.25))
    adapter = PluginComplianceQualityExecutor(
        engine=cast(ComplianceEngine, recording),
        plugin_loader=cast(PluginLoader, FakeLoader(d)),
        plugins_root=tmp_path,
        finding_id_factory=lambda: QualityFindingId("QLT-FIND-PLUGIN-99"),
        evidence_id_factory=lambda: QualityEvidenceId("QLT-EVID-PLUGIN-99"),
        monotonic_clock=lambda: next(times),
    )
    adapter.execute(
        check_id=QualityCheckId("QLT-CHECK-PLUGIN-13"),
        rule=rule(),
        target=target(d),
    )
    assert recording.request is not None
    assert recording.request.plugin_descriptor is d
    assert recording.request.profile_id == "official"
