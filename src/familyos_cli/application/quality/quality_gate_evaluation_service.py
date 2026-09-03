"""Evaluate explicit observation policy over retained canonical Quality results."""

from collections.abc import Callable
from datetime import UTC, datetime

from familyos_cli.application.quality.quality_assessment_execution_result import (
    QualityAssessmentExecutionResult,
)
from familyos_cli.application.quality.quality_check_result import QualityCheckResult
from familyos_cli.domain.quality import (
    QualityAssessmentState,
    QualityCheckId,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.domain.quality.gate_decision import GateDecision
from familyos_cli.domain.quality.quality_gate import QualityGate
from familyos_cli.domain.quality.quality_gate_condition import QualityGateCondition
from familyos_cli.domain.quality.quality_gate_policy import QualityGatePolicy


def _condition(
    code: str,
    message: str,
    checks: tuple[QualityCheckResult, ...] = (),
    check_id: QualityCheckId | None = None,
) -> QualityGateCondition:
    findings = tuple(finding for check in checks for finding in check.findings)
    evidence = tuple(item for check in checks for item in check.evidence)
    return QualityGateCondition(
        code=code,
        message=message,
        check_id=check_id,
        finding_ids=tuple(sorted({item.id for item in findings}, key=str)),
        rule_ids=tuple(
            sorted(
                {item.rule_id for item in findings}
                | {item.rule_id for item in evidence if item.rule_id is not None},
                key=str,
            )
        ),
        evidence_ids=tuple(sorted({item.id for item in evidence}, key=str)),
    )


def _input_errors(
    policy: QualityGatePolicy,
    target: QualityTarget,
    output: QualityAssessmentExecutionResult | None,
    now: datetime,
) -> list[QualityGateCondition]:
    errors: list[QualityGateCondition] = []

    def error(code: str, message: str) -> None:
        errors.append(_condition(code, message))

    if not policy.profile.applies_to(target.target_type):
        error("target_not_supported", "Gate policy does not apply to this target type.")
    if target.revision is None:
        error("revision_missing", "Gate observation requires an exact target revision.")
    if output is None:
        error(
            "assessment_missing",
            "Canonical assessment and retained results are unavailable.",
        )
        return errors
    assessment, checks = output.assessment, output.check_results
    if assessment.target != target or assessment.revision != target.revision:
        error(
            "target_mismatch",
            "Assessment target/revision does not match the gate target.",
        )
    if assessment.profile != policy.profile.reference:
        error(
            "profile_mismatch",
            "Assessment does not use the policy's exact profile version.",
        )
    if assessment.created_at > now:
        error(
            "assessment_from_future", "Assessment time is later than gate evaluation."
        )
    if tuple(check.check_id for check in checks) != policy.profile.required_checks:
        error(
            "required_checks_mismatch",
            "Retained checks do not match the policy's required identities/order.",
        )
    findings = tuple(finding for check in checks for finding in check.findings)
    evidence = tuple(item for check in checks for item in check.evidence)
    if any(item.target != target for item in findings) or any(
        item.target != target
        or (item.revision is not None and item.revision != target.revision)
        for item in evidence
    ):
        error(
            "detail_target_mismatch",
            "Finding/evidence target or revision does not match the gate target.",
        )
    evidence_by_id = {item.id: item for item in evidence}
    findings_by_id = {item.id: item for item in findings}
    if any(evidence_by_id[item.id] != item for item in evidence) or any(
        findings_by_id[item.id] != item for item in findings
    ):
        error(
            "ambiguous_identity",
            "Repeated finding/evidence identities have conflicting content.",
        )
    if set(assessment.evidence_ids) != set(evidence_by_id) or set(
        assessment.finding_ids
    ) != set(findings_by_id):
        error(
            "detail_ids_mismatch",
            "Assessment identifiers do not match retained finding/evidence details.",
        )
    references = {str(item.id) for item in evidence}
    if any(
        reference not in references
        for finding in findings
        for reference in finding.evidence_ids
    ):
        error(
            "evidence_reference_missing",
            "A finding refers to evidence absent from retained results.",
        )
    for check in checks:
        if not check.evidence:
            errors.append(
                _condition(
                    "check_evidence_missing",
                    f"Required check {check.check_id} has no evidence.",
                    (check,),
                    check.check_id,
                )
            )
    return errors


class QualityGateEvaluationService:
    def __init__(self, *, clock: Callable[[], datetime] | None = None) -> None:
        self._clock = clock or (lambda: datetime.now(UTC))

    def evaluate(
        self,
        *,
        policy: QualityGatePolicy,
        target: QualityTarget,
        output: QualityAssessmentExecutionResult | None,
    ) -> QualityGate:
        if not isinstance(policy, QualityGatePolicy) or not isinstance(
            target, QualityTarget
        ):
            raise TypeError("Gate evaluation requires canonical policy and target")
        if output is not None and not isinstance(
            output, QualityAssessmentExecutionResult
        ):
            raise TypeError(
                "Gate input must be a retained canonical execution result or None"
            )
        now = self._clock()
        if (
            not isinstance(now, datetime)
            or now.tzinfo is None
            or now.utcoffset() is None
        ):
            raise ValueError("Gate evaluation clock must return an aware datetime")
        errors = _input_errors(policy, target, output, now)
        failures: list[QualityGateCondition] = []
        if output is not None:
            for check in output.check_results:
                if check.status in (
                    QualityStatus.ERROR,
                    QualityStatus.UNKNOWN,
                    QualityStatus.SKIPPED,
                ):
                    errors.append(
                        _condition(
                            "check_unavailable",
                            f"Required check {check.check_id} is {check.status.value}.",
                            (check,),
                            check.check_id,
                        )
                    )
                elif check.status not in policy.accepted_check_statuses:
                    failures.append(
                        _condition(
                            "check_not_accepted",
                            f"Required check {check.check_id} is {check.status.value}; policy accepts {', '.join(status.value for status in policy.accepted_check_statuses)}.",
                            (check,),
                            check.check_id,
                        )
                    )
            assessment = output.assessment
            if assessment.status in (QualityStatus.ERROR, QualityStatus.SKIPPED):
                errors.append(
                    _condition(
                        "assessment_unavailable",
                        f"Assessment is {assessment.status.value}.",
                        output.check_results,
                    )
                )
            elif (
                assessment.status is QualityStatus.FAIL
                or assessment.quality_state is QualityAssessmentState.FAIL
            ):
                failures.append(
                    _condition(
                        "assessment_failed",
                        "Canonical assessment reports FAIL.",
                        output.check_results,
                    )
                )
            elif not failures:
                pair = (assessment.status, assessment.quality_state)
                if pair not in (
                    (QualityStatus.PASS, QualityAssessmentState.PASS),
                    (QualityStatus.WARNING, QualityAssessmentState.PASS_WITH_WARNINGS),
                ):
                    errors.append(
                        _condition(
                            "assessment_unresolved",
                            "Assessment status/state is unknown or inconsistent.",
                            output.check_results,
                        )
                    )
                elif assessment.quality_state not in policy.accepted_assessment_states:
                    failures.append(
                        _condition(
                            "assessment_not_accepted",
                            "Assessment state is outside the policy's accepted states.",
                            output.check_results,
                        )
                    )
        decision = (
            GateDecision.ERROR
            if errors
            else GateDecision.FAIL
            if failures
            else GateDecision.PASS
        )
        return QualityGate(
            id=policy.gate_id,
            target=target,
            revision=target.revision,
            policy=policy.reference,
            assessment_id=output.assessment.id if output is not None else None,
            decision=decision,
            blocking_conditions=tuple(errors + failures),
            evaluated_at=now,
        )
