from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from familyos_cli.application.quality import (
    QualityAssessmentExecutionResult,
    QualityAssessmentService,
    QualityCheckResult,
)
from familyos_cli.application.quality.initial_merge_gate_policy import (
    INITIAL_MERGE_OBSERVATION_POLICY as POLICY,
)
from familyos_cli.application.quality.quality_gate_evaluation_service import (
    QualityGateEvaluationService,
)
from familyos_cli.domain.quality import (
    GateDecision,
    QualityAssessmentId,
    QualityAssessmentState,
    QualityDomain,
    QualityEvidence,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityEvidenceType,
    QualityFinding,
    QualityFindingId,
    QualityGate,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)

NOW = datetime(2026, 9, 3, 12, 0, tzinfo=UTC)
TARGET = QualityTarget("repository", "fixture", revision="abc123", path="/fixture")


def _output(
    status: QualityStatus = QualityStatus.PASS, *, findings: bool = False
) -> QualityAssessmentExecutionResult:
    checks = []
    for i, check_id in enumerate(POLICY.profile.required_checks):
        check_status = status if i == 0 else QualityStatus.PASS
        evidence = QualityEvidence(
            id=QualityEvidenceId(f"QLT-EVID-{i}"),
            type=QualityEvidenceType("TEST"),
            source="test",
            target=TARGET,
            revision=TARGET.revision,
            created_at=NOW,
            result=QualityEvidenceResult(check_status.value)
            if check_status is not QualityStatus.UNKNOWN
            else QualityEvidenceResult.ERROR,
            rule_id=QualityRuleId(f"QLT-RULE-{i}"),
        )
        finding = QualityFinding(
            id=QualityFindingId("QLT-FIND-0"),
            rule_id=QualityRuleId("QLT-RULE-0"),
            domain=QualityDomain("QLT-DOM-TST"),
            severity=QualitySeverity.INFO,
            status=QualityStatus.FAIL,
            message="failure",
            target=TARGET,
            evidence_ids=(str(evidence.id),),
        )
        checks.append(
            QualityCheckResult(
                check_id=check_id,
                status=check_status,
                evidence=(evidence,),
                findings=(finding,) if findings and i == 0 else (),
            )
        )
    results = tuple(checks)
    assessment = QualityAssessmentService().assess(
        assessment_id=QualityAssessmentId("QLT-ASMT-TEST"),
        target=TARGET,
        profile=POLICY.profile.reference,
        required_check_ids=POLICY.profile.required_checks,
        check_results=results,
        blocking_finding_ids=(),
        created_at=NOW,
    )
    return QualityAssessmentExecutionResult(assessment, results)


def _evaluate(
    output: QualityAssessmentExecutionResult | None, target: QualityTarget = TARGET
) -> QualityGate:
    return QualityGateEvaluationService(clock=lambda: NOW).evaluate(
        policy=POLICY, target=target, output=output
    )


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (QualityStatus.PASS, GateDecision.PASS),
        (QualityStatus.WARNING, GateDecision.FAIL),
        (QualityStatus.FAIL, GateDecision.FAIL),
        (QualityStatus.ERROR, GateDecision.ERROR),
        (QualityStatus.UNKNOWN, GateDecision.ERROR),
        (QualityStatus.SKIPPED, GateDecision.ERROR),
    ],
)
def test_explicit_policy_decisions_preserve_assessment(
    status: QualityStatus, expected: GateDecision
) -> None:
    output = _output(status)
    before = output
    result = _evaluate(output)
    assert result.decision is expected
    assert result.mode == "OBSERVE" and result.prevents_progression is False
    assert result.assessment_id is output.assessment.id
    assert result.target is TARGET and result.revision == TARGET.revision
    assert result.policy == POLICY.reference
    assert output == before
    if status is QualityStatus.FAIL:
        assert output.assessment.quality_state is QualityAssessmentState.UNKNOWN
        assert (
            result.blocking_conditions[0].check_id == POLICY.profile.required_checks[0]
        )
        assert result.blocking_conditions[0].evidence_ids == (
            QualityEvidenceId("QLT-EVID-0"),
        )


def test_failure_explanation_preserves_full_trace_without_severity_inference() -> None:
    output = _output(QualityStatus.FAIL, findings=True)
    condition = _evaluate(output).blocking_conditions[0]
    assert condition.finding_ids == (QualityFindingId("QLT-FIND-0"),)
    assert condition.rule_ids == (QualityRuleId("QLT-RULE-0"),)
    assert condition.evidence_ids == (QualityEvidenceId("QLT-EVID-0"),)
    assert output.check_results[0].findings[0].severity is QualitySeverity.INFO


def test_explicit_policy_can_accept_warning_without_mutating_initial_policy() -> None:
    policy = replace(
        POLICY, accepted_check_statuses=(QualityStatus.PASS, QualityStatus.WARNING)
    )
    result = QualityGateEvaluationService(clock=lambda: NOW).evaluate(
        policy=policy, target=TARGET, output=_output(QualityStatus.WARNING)
    )
    assert result.decision is GateDecision.PASS
    assert POLICY.accepted_check_statuses == (QualityStatus.PASS,)
    strict = replace(policy, accepted_assessment_states=(QualityAssessmentState.PASS,))
    result = QualityGateEvaluationService(clock=lambda: NOW).evaluate(
        policy=strict, target=TARGET, output=_output(QualityStatus.WARNING)
    )
    assert result.decision is GateDecision.FAIL
    assert result.blocking_conditions[0].code == "assessment_not_accepted"


@pytest.mark.parametrize(
    "change",
    [
        "missing-input",
        "missing-revision",
        "target",
        "target-type",
        "profile",
        "future",
        "missing-check",
        "check-order",
        "missing-evidence",
        "evidence-target",
        "evidence-revision",
        "finding-target",
        "finding-ids",
        "evidence-ids",
        "finding-reference",
        "conflicting-evidence",
        "conflicting-finding",
    ],
)
def test_incomplete_stale_or_ambiguous_inputs_never_pass(change: str) -> None:
    output = _output(findings=True)
    target = TARGET
    assessment = output.assessment
    checks = list(output.check_results)
    first = checks[0]
    evidence = first.evidence[0]
    finding = first.findings[0]
    if change == "missing-input":
        assert _evaluate(None).decision is GateDecision.ERROR
        return
    if change == "missing-revision":
        target = replace(TARGET, revision=None)
    elif change == "target":
        target = replace(TARGET, identifier="different")
    elif change == "target-type":
        target = replace(TARGET, target_type="plugin")
    elif change == "profile":
        assessment = replace(assessment, profile="old-profile")
    elif change == "future":
        assessment = replace(assessment, created_at=NOW + timedelta(seconds=1))
    elif change == "missing-check":
        checks.pop()
    elif change == "check-order":
        checks.reverse()
    elif change == "missing-evidence":
        checks[0] = replace(first, evidence=())
    elif change == "evidence-target":
        checks[0] = replace(
            first,
            evidence=(replace(evidence, target=replace(TARGET, identifier="other")),),
        )
    elif change == "evidence-revision":
        checks[0] = replace(first, evidence=(replace(evidence, revision="stale"),))
    elif change == "finding-target":
        checks[0] = replace(
            first,
            findings=(replace(finding, target=replace(TARGET, identifier="other")),),
        )
    elif change == "finding-ids":
        assessment = replace(assessment, finding_ids=())
    elif change == "evidence-ids":
        assessment = replace(assessment, evidence_ids=())
    elif change == "finding-reference":
        checks[0] = replace(
            first, findings=(replace(finding, evidence_ids=("QLT-EVID-ABSENT",)),)
        )
    elif change == "conflicting-evidence":
        checks[0] = replace(
            first, evidence=(evidence, replace(evidence, source="different"))
        )
    elif change == "conflicting-finding":
        checks[0] = replace(
            first, findings=(finding, replace(finding, message="different"))
        )
    result = _evaluate(
        QualityAssessmentExecutionResult(assessment, tuple(checks)), target
    )
    assert result.decision is GateDecision.ERROR
    assert result.blocking_conditions


def test_identical_repeated_identities_are_not_ambiguous() -> None:
    output = _output()
    first = output.check_results[0]
    duplicated = replace(first, evidence=first.evidence * 2)
    result = _evaluate(
        QualityAssessmentExecutionResult(
            output.assessment, (duplicated, *output.check_results[1:])
        )
    )
    assert result.decision is GateDecision.PASS


def test_error_precedes_failure_and_keeps_both_explanations() -> None:
    output = _output(QualityStatus.FAIL)
    errored = replace(output.check_results[1], status=QualityStatus.ERROR)
    mixed = QualityAssessmentExecutionResult(
        output.assessment, (output.check_results[0], errored, *output.check_results[2:])
    )
    result = _evaluate(mixed)
    assert result.decision is GateDecision.ERROR
    assert {condition.code for condition in result.blocking_conditions} >= {
        "check_unavailable",
        "check_not_accepted",
    }


@pytest.mark.parametrize(
    ("status", "state", "expected"),
    [
        (QualityStatus.UNKNOWN, QualityAssessmentState.UNKNOWN, GateDecision.ERROR),
        (QualityStatus.ERROR, QualityAssessmentState.UNKNOWN, GateDecision.ERROR),
        (QualityStatus.SKIPPED, QualityAssessmentState.UNKNOWN, GateDecision.ERROR),
        (
            QualityStatus.PASS,
            QualityAssessmentState.PASS_WITH_WARNINGS,
            GateDecision.ERROR,
        ),
        (QualityStatus.FAIL, QualityAssessmentState.FAIL, GateDecision.FAIL),
    ],
)
def test_assessment_state_is_not_replaced_by_check_success(
    status: QualityStatus, state: QualityAssessmentState, expected: GateDecision
) -> None:
    output = _output()
    assessment = replace(output.assessment, status=status, quality_state=state)
    assert (
        _evaluate(
            QualityAssessmentExecutionResult(assessment, output.check_results)
        ).decision
        is expected
    )


def test_equal_inputs_produce_equal_gate_evaluations() -> None:
    assert _evaluate(_output(QualityStatus.FAIL)) == _evaluate(
        _output(QualityStatus.FAIL)
    )


def test_naive_evaluation_clock_is_rejected() -> None:
    with pytest.raises(ValueError, match="aware datetime"):
        QualityGateEvaluationService(clock=lambda: datetime(2026, 9, 3)).evaluate(
            policy=POLICY, target=TARGET, output=_output()
        )
