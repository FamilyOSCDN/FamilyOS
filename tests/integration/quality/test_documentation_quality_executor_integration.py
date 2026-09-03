from __future__ import annotations

from datetime import UTC, datetime
from itertools import count
from pathlib import Path

from familyos_cli.application.quality.initial_repository_documentation_scope import (
    INITIAL_REPOSITORY_DOCUMENTATION_ROOTS,
)
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
from familyos_cli.infrastructure.documentation import DocumentationValidator
from familyos_cli.infrastructure.quality import DocumentationQualityExecutor

_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
_PASS_EPIC = _REPOSITORY_ROOT / "docs/epics/EPIC-COM-001-communication-plugin"
_QUALITY_EPIC = _REPOSITORY_ROOT / "docs/epics/EPIC-QLT-001-quality-framework"


def _rule() -> QualityRule:
    return QualityRule(
        id=QualityRuleId("QLT-RULE-DOC-INTEGRATION"),
        requirement_id=None,
        domain=QualityDomain("QLT-DOM-DOC"),
        severity=QualitySeverity.HIGH,
        description="Canonical documentation must satisfy Documentation Framework rules",
        executor="documentation",
    )


def _executor(
    *, repository_epic_roots: tuple[str, ...] | None = None,
) -> DocumentationQualityExecutor:
    finding_ids = count(1)
    evidence_ids = count(1)
    return DocumentationQualityExecutor(
        finding_id_factory=lambda: QualityFindingId(
            f"QLT-FIND-DOC-INT-{next(finding_ids):03d}"
        ),
        evidence_id_factory=lambda: QualityEvidenceId(
            f"QLT-EVID-DOC-INT-{next(evidence_ids):03d}"
        ),
        clock=lambda: datetime(2026, 9, 1, 20, 0, tzinfo=UTC),
        repository_epic_roots=repository_epic_roots,
    )


def _target(path: Path, *, identifier: str, revision: str) -> QualityTarget:
    return QualityTarget(
        target_type="repository",
        identifier=identifier,
        revision=revision,
        path=str(path),
    )


def test_real_canonical_epic_produces_documentation_pass() -> None:
    rule = _rule()
    target = _target(
        _PASS_EPIC,
        identifier="EPIC-COM-001",
        revision="integration-pass-revision",
    )

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-DOC-INTEGRATION-PASS"),
        rule=rule,
        target=target,
    )

    assert result.status is QualityStatus.PASS
    assert result.findings == ()
    assert result.diagnostics == ()
    assert len(result.evidence) == 1

    evidence = result.evidence[0]
    assert evidence.result is QualityEvidenceResult.PASS
    assert evidence.type.value == "DOCUMENTATION"
    assert evidence.source == "quality.documentation"
    assert evidence.tool == "familyos-documentation-validator"
    assert evidence.revision == "integration-pass-revision"
    assert evidence.rule_id == rule.id
    assert evidence.requirement_id == rule.requirement_id
    assert ("violations", "0") in evidence.metadata
    assert result.duration_seconds >= 0.0


def test_quality_framework_self_validation_produces_real_findings() -> None:
    rule = _rule()
    target = _target(
        _QUALITY_EPIC,
        identifier="EPIC-QLT-001",
        revision="integration-self-validation-revision",
    )

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-DOC-INTEGRATION-SELF"),
        rule=rule,
        target=target,
    )

    assert result.status is QualityStatus.FAIL
    assert result.diagnostics == ()
    assert len(result.findings) == 32
    assert len(result.evidence) == 1

    evidence = result.evidence[0]
    assert evidence.result is QualityEvidenceResult.FAIL
    assert evidence.type.value == "DOCUMENTATION"
    assert evidence.source == "quality.documentation"
    assert evidence.tool == "familyos-documentation-validator"
    assert evidence.revision == "integration-self-validation-revision"
    assert evidence.rule_id == rule.id
    assert evidence.requirement_id == rule.requirement_id
    assert ("violations", "32") in evidence.metadata

    evidence_id = str(evidence.id)

    assert all(finding.rule_id == rule.id for finding in result.findings)
    assert all(finding.domain == rule.domain for finding in result.findings)
    assert all(finding.severity == rule.severity for finding in result.findings)
    assert all(finding.status is QualityStatus.FAIL for finding in result.findings)
    assert all(finding.target == target for finding in result.findings)
    assert all(finding.evidence_ids == (evidence_id,) for finding in result.findings)
    assert all(
        finding.message.startswith("Markdown document must contain exactly one level-one heading")
        for finding in result.findings
    )
    assert all(finding.location is not None for finding in result.findings)
    assert result.duration_seconds >= 0.0


def test_repository_scope_preserves_real_epic_findings_and_provenance() -> None:
    roots = INITIAL_REPOSITORY_DOCUMENTATION_ROOTS
    validator = DocumentationValidator()
    expected = [
        (violation.message, f"{relative}/{violation.location}" if violation.location is not None else relative)
        for relative in roots
        for violation in validator.validate(_REPOSITORY_ROOT / relative).violations
    ]
    target = _target(
        _REPOSITORY_ROOT, identifier="familyos-cli",
        revision="integration-repository-revision",
    )

    result = _executor(repository_epic_roots=roots).execute(
        check_id=QualityCheckId("QLT-CHECK-DOC-INTEGRATION-REPOSITORY"),
        rule=_rule(), target=target,
    )

    assert [(f.message, f.location) for f in result.findings] == expected
    assert result.status is (QualityStatus.FAIL if expected else QualityStatus.PASS)
    assert result.diagnostics == ()
    assert len(result.evidence) == 1
    assert result.evidence[0].target is target
    assert result.evidence[0].revision == target.revision
    assert result.evidence[0].metadata == (
        ("violations", str(len(expected))),
        ("scope", "repository_epics"),
        ("epic_roots", "\n".join(roots)),
    )
    assert all(f.target is target for f in result.findings)
    assert all(f.evidence_ids == (str(result.evidence[0].id),) for f in result.findings)
