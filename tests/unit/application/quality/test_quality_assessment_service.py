from datetime import UTC, datetime

from familyos_cli.application.quality import (
    QualityAssessmentService,
    QualityCheckResult,
)
from familyos_cli.domain.quality import (
    QualityAssessmentId,
    QualityAssessmentState,
    QualityCheckId,
    QualityEvidence,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityEvidenceType,
    QualityStatus,
    QualityTarget,
)

NOW = datetime(2026, 9, 2, tzinfo=UTC)
TARGET = QualityTarget("repository", "familyos-cli", revision="abc123")
CHECK = QualityCheckId("QLT-CHECK-001")


def ev(result: QualityEvidenceResult = QualityEvidenceResult.PASS) -> QualityEvidence:
    return QualityEvidence(
        id=QualityEvidenceId("QLT-EVID-001"),
        type=QualityEvidenceType("TEST"),
        source="pytest",
        target=TARGET,
        result=result,
        created_at=NOW,
        revision="abc123",
    )


def assess(result: QualityCheckResult | None):
    return QualityAssessmentService().assess(
        assessment_id=QualityAssessmentId("QLT-ASMT-001"),
        target=TARGET,
        profile="baseline",
        required_check_ids=(CHECK,),
        check_results=() if result is None else (result,),
        blocking_finding_ids=(),
        created_at=NOW,
    )


def test_pass() -> None:
    a = assess(
        QualityCheckResult(check_id=CHECK, status=QualityStatus.PASS, evidence=(ev(),))
    )
    assert a.status is QualityStatus.PASS
    assert a.quality_state is QualityAssessmentState.PASS


def test_missing_required_check_is_unknown() -> None:
    a = assess(None)
    assert a.quality_state is QualityAssessmentState.UNKNOWN


def test_missing_evidence_is_unknown() -> None:
    a = assess(QualityCheckResult(check_id=CHECK, status=QualityStatus.PASS))
    assert a.quality_state is QualityAssessmentState.UNKNOWN


def test_error_is_error_unknown() -> None:
    a = assess(
        QualityCheckResult(
            check_id=CHECK,
            status=QualityStatus.ERROR,
            evidence=(ev(QualityEvidenceResult.ERROR),),
        )
    )
    assert a.status is QualityStatus.ERROR
    assert a.quality_state is QualityAssessmentState.UNKNOWN


def test_warning_is_pass_with_warnings() -> None:
    a = assess(
        QualityCheckResult(
            check_id=CHECK,
            status=QualityStatus.WARNING,
            evidence=(ev(QualityEvidenceResult.WARNING),),
        )
    )
    assert a.status is QualityStatus.WARNING
    assert a.quality_state is QualityAssessmentState.PASS_WITH_WARNINGS


def test_explicit_blocking_finding_produces_fail() -> None:
    from familyos_cli.domain.quality import (
        QualityDomain,
        QualityFinding,
        QualityFindingId,
        QualityRuleId,
        QualitySeverity,
    )

    blocker = QualityFinding(
        id=QualityFindingId("QLT-FIND-001"),
        rule_id=QualityRuleId("QLT-RULE-001"),
        domain=QualityDomain("QLT-DOM-TST"),
        severity=QualitySeverity.HIGH,
        status=QualityStatus.FAIL,
        message="blocking quality finding",
        target=TARGET,
    )

    result = QualityCheckResult(
        check_id=CHECK,
        status=QualityStatus.FAIL,
        findings=(blocker,),
        evidence=(ev(QualityEvidenceResult.FAIL),),
    )

    assessment = QualityAssessmentService().assess(
        assessment_id=QualityAssessmentId("QLT-ASMT-001"),
        target=TARGET,
        profile="baseline",
        required_check_ids=(CHECK,),
        check_results=(result,),
        blocking_finding_ids=(blocker.id,),
        created_at=NOW,
    )

    assert assessment.status is QualityStatus.FAIL
    assert assessment.quality_state is QualityAssessmentState.FAIL
    assert assessment.finding_ids == (blocker.id,)


def test_reordered_inputs_produce_identical_references_and_conclusion() -> None:
    from familyos_cli.domain.quality import (
        QualityDomain,
        QualityFinding,
        QualityFindingId,
        QualityRuleId,
        QualitySeverity,
    )

    check_two = QualityCheckId("QLT-CHECK-002")

    evidence_one = ev(QualityEvidenceResult.WARNING)
    evidence_two = QualityEvidence(
        id=QualityEvidenceId("QLT-EVID-002"),
        type=QualityEvidenceType("TEST"),
        source="pytest",
        target=TARGET,
        result=QualityEvidenceResult.WARNING,
        created_at=NOW,
        revision="abc123",
    )

    finding_one = QualityFinding(
        id=QualityFindingId("QLT-FIND-002"),
        rule_id=QualityRuleId("QLT-RULE-001"),
        domain=QualityDomain("QLT-DOM-TST"),
        severity=QualitySeverity.HIGH,
        status=QualityStatus.WARNING,
        message="warning one",
        target=TARGET,
    )

    finding_two = QualityFinding(
        id=QualityFindingId("QLT-FIND-001"),
        rule_id=QualityRuleId("QLT-RULE-001"),
        domain=QualityDomain("QLT-DOM-TST"),
        severity=QualitySeverity.HIGH,
        status=QualityStatus.WARNING,
        message="warning two",
        target=TARGET,
    )

    first_result = QualityCheckResult(
        check_id=CHECK,
        status=QualityStatus.WARNING,
        findings=(finding_one,),
        evidence=(evidence_one,),
    )

    second_result = QualityCheckResult(
        check_id=check_two,
        status=QualityStatus.WARNING,
        findings=(finding_two,),
        evidence=(evidence_two,),
    )

    service = QualityAssessmentService()

    first = service.assess(
        assessment_id=QualityAssessmentId("QLT-ASMT-001"),
        target=TARGET,
        profile="baseline",
        required_check_ids=(CHECK, check_two),
        check_results=(first_result, second_result),
        blocking_finding_ids=(),
        created_at=NOW,
    )

    second = service.assess(
        assessment_id=QualityAssessmentId("QLT-ASMT-001"),
        target=TARGET,
        profile="baseline",
        required_check_ids=(check_two, CHECK),
        check_results=(second_result, first_result),
        blocking_finding_ids=(),
        created_at=NOW,
    )

    assert first.status == second.status
    assert first.quality_state == second.quality_state
    assert first.evidence_ids == second.evidence_ids
    assert first.finding_ids == second.finding_ids


def test_required_unknown_is_unknown() -> None:
    assessment = assess(
        QualityCheckResult(
            check_id=CHECK,
            status=QualityStatus.UNKNOWN,
            evidence=(ev(),),
        )
    )

    assert assessment.status is QualityStatus.UNKNOWN
    assert assessment.quality_state is QualityAssessmentState.UNKNOWN


def test_required_skipped_is_unknown() -> None:
    assessment = assess(
        QualityCheckResult(
            check_id=CHECK,
            status=QualityStatus.SKIPPED,
            evidence=(ev(QualityEvidenceResult.SKIPPED),),
        )
    )

    assert assessment.status is QualityStatus.UNKNOWN
    assert assessment.quality_state is QualityAssessmentState.UNKNOWN


def test_empty_required_check_set_is_unknown() -> None:
    assessment = QualityAssessmentService().assess(
        assessment_id=QualityAssessmentId("QLT-ASMT-001"),
        target=TARGET,
        profile="baseline",
        required_check_ids=(),
        check_results=(),
        blocking_finding_ids=(),
        created_at=NOW,
    )

    assert assessment.status is QualityStatus.UNKNOWN
    assert assessment.quality_state is QualityAssessmentState.UNKNOWN


def test_service_preserves_profile_and_target_revision() -> None:
    assessment = assess(
        QualityCheckResult(
            check_id=CHECK,
            status=QualityStatus.PASS,
            evidence=(ev(),),
        )
    )

    assert assessment.profile == "baseline"
    assert assessment.target == TARGET
    assert assessment.revision == TARGET.revision


def test_duplicate_check_results_are_rejected() -> None:
    first = QualityCheckResult(
        check_id=CHECK,
        status=QualityStatus.PASS,
        evidence=(ev(),),
    )
    second = QualityCheckResult(
        check_id=CHECK,
        status=QualityStatus.ERROR,
        evidence=(ev(QualityEvidenceResult.ERROR),),
    )

    import pytest

    with pytest.raises(ValueError, match="unique check_ids"):
        QualityAssessmentService().assess(
            assessment_id=QualityAssessmentId("QLT-ASMT-001"),
            target=TARGET,
            profile="baseline",
            required_check_ids=(CHECK,),
            check_results=(first, second),
            blocking_finding_ids=(),
            created_at=NOW,
        )


def test_evidence_for_different_target_is_rejected() -> None:
    different_target = QualityTarget(
        "repository", "other-repository", revision="abc123"
    )
    evidence = QualityEvidence(
        id=QualityEvidenceId("QLT-EVID-002"),
        type=QualityEvidenceType("TEST"),
        source="pytest",
        target=different_target,
        result=QualityEvidenceResult.PASS,
        created_at=NOW,
        revision="abc123",
    )
    result = QualityCheckResult(
        check_id=CHECK, status=QualityStatus.PASS, evidence=(evidence,)
    )

    import pytest

    with pytest.raises(ValueError, match="evidence target must match"):
        assess(result)


def test_finding_for_different_target_is_rejected() -> None:
    from familyos_cli.domain.quality import (
        QualityDomain,
        QualityFinding,
        QualityFindingId,
        QualityRuleId,
        QualitySeverity,
    )

    different_target = QualityTarget(
        "repository", "other-repository", revision="abc123"
    )
    finding = QualityFinding(
        id=QualityFindingId("QLT-FIND-001"),
        rule_id=QualityRuleId("QLT-RULE-001"),
        domain=QualityDomain("QLT-DOM-TST"),
        severity=QualitySeverity.HIGH,
        status=QualityStatus.WARNING,
        message="finding for another target",
        target=different_target,
    )
    result = QualityCheckResult(
        check_id=CHECK,
        status=QualityStatus.WARNING,
        findings=(finding,),
        evidence=(ev(QualityEvidenceResult.WARNING),),
    )

    import pytest

    with pytest.raises(ValueError, match="finding target must match"):
        assess(result)


def test_explicit_evidence_revision_mismatch_is_rejected() -> None:
    evidence = QualityEvidence(
        id=QualityEvidenceId("QLT-EVID-002"),
        type=QualityEvidenceType("TEST"),
        source="pytest",
        target=TARGET,
        result=QualityEvidenceResult.PASS,
        created_at=NOW,
        revision="different-revision",
    )
    result = QualityCheckResult(
        check_id=CHECK, status=QualityStatus.PASS, evidence=(evidence,)
    )

    import pytest

    with pytest.raises(ValueError, match="evidence revision must match"):
        assess(result)


def test_evidence_without_revision_remains_acceptable() -> None:
    evidence = QualityEvidence(
        id=QualityEvidenceId("QLT-EVID-002"),
        type=QualityEvidenceType("TEST"),
        source="pytest",
        target=TARGET,
        result=QualityEvidenceResult.PASS,
        created_at=NOW,
        revision=None,
    )
    assessment = assess(
        QualityCheckResult(
            check_id=CHECK,
            status=QualityStatus.PASS,
            evidence=(evidence,),
        )
    )

    assert assessment.status is QualityStatus.PASS
    assert assessment.quality_state is QualityAssessmentState.PASS
    assert assessment.evidence_ids == (evidence.id,)


def test_required_fail_cannot_be_promoted_to_pass_with_warnings() -> None:
    failed_check = QualityCheckId("QLT-CHECK-002")
    warning_check = QualityCheckId("QLT-CHECK-003")
    failed_result = QualityCheckResult(
        check_id=failed_check,
        status=QualityStatus.FAIL,
        evidence=(
            QualityEvidence(
                id=QualityEvidenceId("QLT-EVID-010"),
                type=QualityEvidenceType("TEST"),
                source="pytest",
                target=TARGET,
                result=QualityEvidenceResult.FAIL,
                created_at=NOW,
                revision=TARGET.revision,
            ),
        ),
    )
    warning_result = QualityCheckResult(
        check_id=warning_check,
        status=QualityStatus.WARNING,
        evidence=(
            QualityEvidence(
                id=QualityEvidenceId("QLT-EVID-011"),
                type=QualityEvidenceType("TEST"),
                source="pytest",
                target=TARGET,
                result=QualityEvidenceResult.WARNING,
                created_at=NOW,
                revision=TARGET.revision,
            ),
        ),
    )
    assessment = QualityAssessmentService().assess(
        assessment_id=QualityAssessmentId("QLT-ASMT-001"),
        target=TARGET,
        profile="profile-ref",
        required_check_ids=(failed_check, warning_check),
        check_results=(failed_result, warning_result),
        blocking_finding_ids=(),
        created_at=NOW,
    )
    assert assessment.status is QualityStatus.UNKNOWN
    assert assessment.quality_state is QualityAssessmentState.UNKNOWN


def test_non_required_warning_does_not_change_required_assessment_state() -> None:
    optional_check = QualityCheckId("QLT-CHECK-002")
    required_result = QualityCheckResult(
        check_id=CHECK,
        status=QualityStatus.PASS,
        evidence=(ev(QualityEvidenceResult.PASS),),
    )
    optional_result = QualityCheckResult(
        check_id=optional_check,
        status=QualityStatus.WARNING,
        evidence=(
            QualityEvidence(
                id=QualityEvidenceId("QLT-EVID-012"),
                type=QualityEvidenceType("TEST"),
                source="pytest",
                target=TARGET,
                result=QualityEvidenceResult.WARNING,
                created_at=NOW,
                revision=TARGET.revision,
            ),
        ),
    )
    assessment = QualityAssessmentService().assess(
        assessment_id=QualityAssessmentId("QLT-ASMT-001"),
        target=TARGET,
        profile="profile-ref",
        required_check_ids=(CHECK,),
        check_results=(required_result, optional_result),
        blocking_finding_ids=(),
        created_at=NOW,
    )
    assert assessment.status is QualityStatus.PASS
    assert assessment.quality_state is QualityAssessmentState.PASS
    assert QualityEvidenceId("QLT-EVID-012") in assessment.evidence_ids


def test_non_required_blocking_finding_does_not_fail_required_assessment() -> None:
    from familyos_cli.domain.quality import (
        QualityDomain,
        QualityFinding,
        QualityFindingId,
        QualityRuleId,
        QualitySeverity,
    )

    optional_check = QualityCheckId("QLT-CHECK-002")
    optional_finding = QualityFinding(
        id=QualityFindingId("QLT-FIND-010"),
        rule_id=QualityRuleId("QLT-RULE-010"),
        domain=QualityDomain("QLT-DOM-TST"),
        severity=QualitySeverity.HIGH,
        status=QualityStatus.FAIL,
        message="non-required blocking finding",
        target=TARGET,
    )
    required_result = QualityCheckResult(
        check_id=CHECK,
        status=QualityStatus.PASS,
        evidence=(ev(QualityEvidenceResult.PASS),),
    )
    optional_result = QualityCheckResult(
        check_id=optional_check,
        status=QualityStatus.FAIL,
        findings=(optional_finding,),
        evidence=(
            QualityEvidence(
                id=QualityEvidenceId("QLT-EVID-013"),
                type=QualityEvidenceType("TEST"),
                source="pytest",
                target=TARGET,
                result=QualityEvidenceResult.FAIL,
                created_at=NOW,
                revision=TARGET.revision,
            ),
        ),
    )
    assessment = QualityAssessmentService().assess(
        assessment_id=QualityAssessmentId("QLT-ASMT-001"),
        target=TARGET,
        profile="profile-ref",
        required_check_ids=(CHECK,),
        check_results=(required_result, optional_result),
        blocking_finding_ids=(optional_finding.id,),
        created_at=NOW,
    )
    assert assessment.status is QualityStatus.PASS
    assert assessment.quality_state is QualityAssessmentState.PASS
    assert optional_finding.id in assessment.finding_ids
