from dataclasses import replace
from datetime import UTC, datetime, timedelta
from unittest.mock import Mock

import pytest

from familyos_cli.application.ports.quality.quality_executor import (
    QualityExecutorPort,
)
from familyos_cli.application.quality import (
    QualityAssessmentExecutionResult,
    QualityAssessmentService,
    QualityProfileAssessmentService,
    QualityProfileRegistry,
    QualityProfileResolver,
)
from familyos_cli.application.quality.quality_assessment_execution_service import (
    QualityAssessmentExecutionService,
)
from familyos_cli.application.quality.quality_check_result import QualityCheckResult
from familyos_cli.application.quality.quality_execution_binding import (
    QualityExecutionBinding,
)
from familyos_cli.application.quality.quality_execution_service import (
    QualityExecutionService,
)
from familyos_cli.domain.quality import (
    QualityAssessmentId,
    QualityAssessmentState,
    QualityCheckId,
    QualityDomain,
    QualityEvidence,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityEvidenceType,
    QualityFinding,
    QualityFindingId,
    QualityProfile,
    QualityProfileId,
    QualityRequirementId,
    QualityRule,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)

NOW = datetime(2026, 9, 3, 9, 0, tzinfo=UTC)
TARGET = QualityTarget(
    target_type="repository",
    identifier="familyos-cli",
    revision="abc123",
    path=".",
)
CHECK = QualityCheckId("QLT-CHECK-RUFF")
RULE = QualityRule(
    id=QualityRuleId("QLT-RULE-STA-001"),
    requirement_id=None,
    domain=QualityDomain("QLT-DOM-MNT"),
    severity=QualitySeverity.MEDIUM,
    description="Ruff must pass.",
)


class Executor(QualityExecutorPort):
    def __init__(
        self, status: QualityStatus = QualityStatus.PASS,
        results: tuple[QualityCheckResult, ...] = (),
    ) -> None:
        self.status = status
        self.results = {result.check_id: result for result in results}
        self.calls: list[tuple[QualityCheckId, QualityRule, QualityTarget]] = []

    def execute(
        self,
        *,
        check_id: QualityCheckId,
        rule: QualityRule,
        target: QualityTarget,
    ) -> QualityCheckResult:
        self.calls.append((check_id, rule, target))
        if check_id in self.results:
            return self.results[check_id]
        evidence_result = (
            QualityEvidenceResult.PASS
            if self.status is QualityStatus.PASS
            else QualityEvidenceResult.FAIL
        )
        evidence = QualityEvidence(
            id=QualityEvidenceId("QLT-EVID-TEST"),
            type=QualityEvidenceType("TEST"),
            source="test",
            target=target,
            result=evidence_result,
            created_at=NOW,
            revision=target.revision,
        )
        return QualityCheckResult(
            check_id=check_id,
            status=self.status,
            evidence=(evidence,),
        )


def make_service(
    status: QualityStatus = QualityStatus.PASS,
    *, results: tuple[QualityCheckResult, ...] = (),
) -> tuple[QualityAssessmentExecutionService, Executor]:
    checks = tuple(result.check_id for result in results) or (CHECK,)
    registry = QualityProfileRegistry()
    registry.register(
        QualityProfile(
            id=QualityProfileId("QLT-PROFILE-REPOSITORY"),
            version="1",
            target_types=("repository",),
            required_checks=checks,
            required_domains=(QualityDomain("QLT-DOM-MNT"),),
            severity_policy=(),
        )
    )
    resolver = QualityProfileResolver(registry)
    executor = Executor(status, results)
    execution = QualityExecutionService(
        resolver,
        tuple(QualityExecutionBinding(check, RULE, executor) for check in checks),
    )
    service = QualityAssessmentExecutionService(
        execution_service=execution,
        assessment_service=QualityProfileAssessmentService(resolver),
        assessment_id_factory=lambda: QualityAssessmentId("QLT-ASMT-TEST"),
        clock=lambda: NOW,
    )
    return service, executor


def test_execute_produces_canonical_assessment() -> None:
    service, executor = make_service()

    assessment = service.execute(TARGET)

    assert executor.calls == [(CHECK, RULE, TARGET)]
    assert assessment.id == QualityAssessmentId("QLT-ASMT-TEST")
    assert assessment.profile == "QLT-PROFILE-REPOSITORY@1"
    assert assessment.status is QualityStatus.PASS
    assert assessment.quality_state is QualityAssessmentState.PASS
    assert assessment.created_at == NOW


def test_fail_is_not_implicitly_blocking() -> None:
    service, _ = make_service(QualityStatus.FAIL)

    assessment = service.execute(TARGET)

    assert assessment.status is QualityStatus.UNKNOWN
    assert assessment.quality_state is QualityAssessmentState.UNKNOWN


def test_rejects_invalid_target_before_execution() -> None:
    service, executor = make_service()

    with pytest.raises(TypeError, match="target must be a QualityTarget"):
        service.execute(object())  # type: ignore[arg-type]

    assert executor.calls == []


def detailed_check(suffix: str = "Z") -> QualityCheckResult:
    evidence = QualityEvidence(
        id=QualityEvidenceId(f"QLT-EVID-{suffix}"),
        type=QualityEvidenceType("TEST"),
        source="normalized-executor",
        target=TARGET,
        result=QualityEvidenceResult.FAIL,
        created_at=NOW,
        revision=TARGET.revision,
        rule_id=RULE.id,
        requirement_id=QualityRequirementId("QLT-REQ-TEST"),
        tool="test-tool",
        tool_version="1.0",
        metadata=(("detail", "first"), ("detail", "second")),
        artifact="logs/quality.txt",
    )
    finding = QualityFinding(
        id=QualityFindingId(f"QLT-FIND-{suffix}"),
        rule_id=RULE.id,
        domain=RULE.domain,
        severity=QualitySeverity.CRITICAL,
        status=QualityStatus.FAIL,
        message="Preserve this actionable finding.",
        target=TARGET,
        location="src/example.py:17",
        evidence_ids=(str(evidence.id), str(evidence.id)),
    )
    return QualityCheckResult(
        check_id=QualityCheckId(f"QLT-CHECK-{suffix}"),
        status=QualityStatus.FAIL,
        findings=(finding, replace(finding, location=None), finding),
        evidence=(evidence, evidence),
        duration_seconds=2.5,
        diagnostics=("first diagnostic", "second diagnostic", "first diagnostic"),
    )


def test_detailed_execution_retains_order_multiplicity_and_correlated_ids() -> None:
    checks = (detailed_check("Z"), detailed_check("A"))
    service, executor = make_service(results=checks)

    output = service.execute_with_results(TARGET)

    assert executor.calls == [(check.check_id, RULE, TARGET) for check in checks]
    assert output.assessment.target is TARGET
    assert output.assessment.revision == TARGET.revision
    assert output.assessment.profile == "QLT-PROFILE-REPOSITORY@1"
    assert output.assessment.status is QualityStatus.UNKNOWN
    assert output.assessment.quality_state is QualityAssessmentState.UNKNOWN
    assert output.assessment.evidence_ids == (
        QualityEvidenceId("QLT-EVID-A"), QualityEvidenceId("QLT-EVID-Z"),
    )
    assert output.assessment.finding_ids == (
        QualityFindingId("QLT-FIND-A"), QualityFindingId("QLT-FIND-Z"),
    )
    for retained, original in zip(output.check_results, checks, strict=True):
        assert retained is original
        assert retained.findings is original.findings
        assert retained.evidence is original.evidence
        assert retained.diagnostics is original.diagnostics
        assert retained.duration_seconds == 2.5
        assert retained.findings[0].evidence_ids == (
            str(retained.evidence[0].id), str(retained.evidence[0].id),
        )


@pytest.mark.parametrize("method", ("execute", "execute_with_results"))
def test_each_entry_point_uses_one_execution_and_one_assessment(
    monkeypatch: pytest.MonkeyPatch, method: str,
) -> None:
    checks = (detailed_check(),)
    expected = QualityAssessmentService().assess(
        assessment_id=QualityAssessmentId("QLT-ASMT-TEST"), target=TARGET,
        profile="QLT-PROFILE-REPOSITORY@1",
        required_check_ids=(checks[0].check_id,), check_results=checks,
        blocking_finding_ids=(), created_at=NOW,
    )
    service, _ = make_service(results=checks)
    execute = Mock(return_value=checks)
    assess = Mock(return_value=expected)
    identity = Mock(return_value=expected.id)
    clock = Mock(return_value=NOW)
    monkeypatch.setattr(service._execution_service, "execute", execute)
    monkeypatch.setattr(service._assessment_service, "assess", assess)
    monkeypatch.setattr(service, "_assessment_id_factory", identity)
    monkeypatch.setattr(service, "_clock", clock)

    output = getattr(service, method)(TARGET)

    if method == "execute":
        assert output is expected
    else:
        assert isinstance(output, QualityAssessmentExecutionResult)
        assert output.assessment is expected
        assert output.check_results is checks
    execute.assert_called_once_with(TARGET)
    assess.assert_called_once_with(
        assessment_id=expected.id, target=TARGET, check_results=checks,
        blocking_finding_ids=(), created_at=NOW,
    )
    assert assess.call_args.kwargs["check_results"] is checks
    assert assess.call_args.kwargs["target"] is TARGET
    identity.assert_called_once_with()
    clock.assert_called_once_with()


@pytest.mark.parametrize(
    ("status", "has_evidence", "expected_status", "expected_state"),
    (
        (QualityStatus.PASS, True, QualityStatus.PASS, QualityAssessmentState.PASS),
        (
            QualityStatus.WARNING, True, QualityStatus.WARNING,
            QualityAssessmentState.PASS_WITH_WARNINGS,
        ),
        (QualityStatus.FAIL, True, QualityStatus.UNKNOWN, QualityAssessmentState.UNKNOWN),
        (QualityStatus.ERROR, True, QualityStatus.ERROR, QualityAssessmentState.UNKNOWN),
        (QualityStatus.ERROR, False, QualityStatus.ERROR, QualityAssessmentState.UNKNOWN),
        (QualityStatus.SKIPPED, True, QualityStatus.UNKNOWN, QualityAssessmentState.UNKNOWN),
        (QualityStatus.UNKNOWN, True, QualityStatus.UNKNOWN, QualityAssessmentState.UNKNOWN),
        (QualityStatus.PASS, False, QualityStatus.UNKNOWN, QualityAssessmentState.UNKNOWN),
    ),
)
def test_detailed_execution_preserves_assessment_policy(
    status: QualityStatus, has_evidence: bool,
    expected_status: QualityStatus, expected_state: QualityAssessmentState,
) -> None:
    original = detailed_check()
    check = replace(
        original, status=status,
        findings=original.findings if status is QualityStatus.FAIL else (),
        evidence=original.evidence if has_evidence else (),
    )
    service, executor = make_service(results=(check,))

    output = service.execute_with_results(TARGET)

    assert len(executor.calls) == 1
    assert output.check_results[0] is check
    assert output.assessment.status is expected_status
    assert output.assessment.quality_state is expected_state


def test_invocations_are_fresh_and_previous_output_remains_stable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, executor = make_service()
    ids = (QualityAssessmentId("QLT-ASMT-FIRST"), QualityAssessmentId("QLT-ASMT-SECOND"))
    identity = Mock(side_effect=ids)
    clock = Mock(side_effect=(NOW, NOW + timedelta(seconds=1)))
    monkeypatch.setattr(service, "_assessment_id_factory", identity)
    monkeypatch.setattr(service, "_clock", clock)

    first = service.execute_with_results(TARGET)
    executor.status = QualityStatus.WARNING
    second = service.execute(TARGET)

    assert first.assessment.id == ids[0]
    assert first.assessment.status is QualityStatus.PASS
    assert first.check_results[0].status is QualityStatus.PASS
    assert first.assessment.created_at == NOW
    assert second.id == ids[1]
    assert second.status is QualityStatus.WARNING
    assert second.created_at == NOW + timedelta(seconds=1)
    assert executor.calls == [(CHECK, RULE, TARGET), (CHECK, RULE, TARGET)]
    assert identity.call_count == clock.call_count == 2


def test_detailed_execution_rejects_invalid_target_before_any_dependency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, executor = make_service()
    identity, clock = Mock(), Mock()
    monkeypatch.setattr(service, "_assessment_id_factory", identity)
    monkeypatch.setattr(service, "_clock", clock)

    with pytest.raises(TypeError, match="target must be a QualityTarget"):
        service.execute_with_results(object())  # type: ignore[arg-type]

    assert executor.calls == []
    identity.assert_not_called()
    clock.assert_not_called()


@pytest.mark.parametrize("method", ("execute", "execute_with_results"))
@pytest.mark.parametrize("stage", ("execute", "identity", "clock", "assess"))
def test_dependency_errors_propagate_without_retry_or_later_steps(
    monkeypatch: pytest.MonkeyPatch, method: str, stage: str,
) -> None:
    service, _ = make_service()
    execute = Mock(wraps=service._execution_service.execute)
    assess = Mock(wraps=service._assessment_service.assess)
    identity = Mock(return_value=QualityAssessmentId("QLT-ASMT-TEST"))
    clock = Mock(return_value=NOW)
    steps = {"execute": execute, "identity": identity, "clock": clock, "assess": assess}
    failure = RuntimeError(f"{stage} failed")
    steps[stage].side_effect = failure
    monkeypatch.setattr(service._execution_service, "execute", execute)
    monkeypatch.setattr(service._assessment_service, "assess", assess)
    monkeypatch.setattr(service, "_assessment_id_factory", identity)
    monkeypatch.setattr(service, "_clock", clock)

    with pytest.raises(RuntimeError) as error:
        getattr(service, method)(TARGET)

    assert error.value is failure
    failed_index = tuple(steps).index(stage)
    assert [step.call_count for step in steps.values()] == [
        1 if index <= failed_index else 0 for index in range(len(steps))
    ]


@pytest.mark.parametrize(
    ("dependency", "value", "error", "message"),
    (
        ("_assessment_id_factory", "invalid-id", TypeError, "id must"),
        ("_clock", "invalid-time", TypeError, "created_at must"),
        ("_clock", NOW.replace(tzinfo=None), ValueError, "timezone-aware"),
    ),
)
def test_invalid_identity_or_time_is_rejected_by_assessment(
    monkeypatch: pytest.MonkeyPatch, dependency: str,
    value: object, error: type[Exception], message: str,
) -> None:
    service, executor = make_service()
    monkeypatch.setattr(service, dependency, Mock(return_value=value))

    with pytest.raises(error, match=message):
        service.execute_with_results(TARGET)

    assert len(executor.calls) == 1


@pytest.mark.parametrize("mismatch", ("evidence_target", "evidence_revision", "finding_target"))
def test_detailed_execution_preserves_assessment_consistency_validation(
    mismatch: str,
) -> None:
    check = detailed_check()
    different_target = replace(TARGET, identifier="another-repository")
    if mismatch == "evidence_target":
        check = replace(check, evidence=(replace(check.evidence[0], target=different_target),))
    elif mismatch == "evidence_revision":
        check = replace(check, evidence=(replace(check.evidence[0], revision="another-revision"),))
    else:
        check = replace(check, findings=(replace(check.findings[0], target=different_target),))
    service, executor = make_service(results=(check,))

    with pytest.raises(ValueError, match="must match assessment target"):
        service.execute_with_results(TARGET)

    assert len(executor.calls) == 1
