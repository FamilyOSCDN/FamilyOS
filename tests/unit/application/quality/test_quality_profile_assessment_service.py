from datetime import UTC, datetime

import pytest

from familyos_cli.application.quality import (
    QualityAssessmentService,
    QualityCheckResult,
    QualityProfileAssessmentService,
    QualityProfileRegistry,
    QualityProfileResolver,
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
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)

NOW = datetime(2026, 9, 2, tzinfo=UTC)
TARGET = QualityTarget("repository", "familyos-cli", revision="abc123")
CHECK = QualityCheckId("QLT-CHECK-RUFF")


def profile(
    *,
    version: str = "1",
    target_types: tuple[str, ...] = ("repository",),
    required_checks: tuple[QualityCheckId, ...] = (CHECK,),
    severity_policy: tuple[tuple[QualitySeverity, bool], ...] = (
        (QualitySeverity.HIGH, True),
    ),
) -> QualityProfile:
    return QualityProfile(
        id=QualityProfileId("QLT-PROFILE-REPOSITORY"),
        version=version,
        target_types=target_types,
        required_checks=required_checks,
        required_domains=(QualityDomain("QLT-DOM-COR"),),
        severity_policy=severity_policy,
    )


def service_for(*profiles: QualityProfile) -> QualityProfileAssessmentService:
    registry = QualityProfileRegistry()
    for value in profiles:
        registry.register(value)
    return QualityProfileAssessmentService(QualityProfileResolver(registry))


def evidence(
    result: QualityEvidenceResult = QualityEvidenceResult.PASS,
) -> QualityEvidence:
    return QualityEvidence(
        id=QualityEvidenceId("QLT-EVID-001"),
        type=QualityEvidenceType("TEST"),
        source="pytest",
        target=TARGET,
        result=result,
        created_at=NOW,
        revision=TARGET.revision,
    )


def result(
    *,
    status: QualityStatus = QualityStatus.PASS,
    evidence_result: QualityEvidenceResult = QualityEvidenceResult.PASS,
    findings: tuple[QualityFinding, ...] = (),
) -> QualityCheckResult:
    return QualityCheckResult(
        check_id=CHECK,
        status=status,
        findings=findings,
        evidence=(evidence(evidence_result),),
    )


def assess(
    service: QualityProfileAssessmentService,
    *,
    check_results: tuple[QualityCheckResult, ...],
    blocking_finding_ids: tuple[QualityFindingId, ...] = (),
):
    return service.assess(
        assessment_id=QualityAssessmentId("QLT-ASMT-001"),
        target=TARGET,
        check_results=check_results,
        blocking_finding_ids=blocking_finding_ids,
        created_at=NOW,
    )


def test_resolved_profile_reference_is_stored_in_assessment() -> None:
    assessment = assess(service_for(profile()), check_results=(result(),))

    assert assessment.profile == "QLT-PROFILE-REPOSITORY@1"
    assert assessment.target == TARGET
    assert assessment.revision == TARGET.revision


def test_profile_required_checks_drive_assessment_required_set() -> None:
    required = QualityCheckId("QLT-CHECK-MYPY")
    assessment = assess(
        service_for(profile(required_checks=(required,))),
        check_results=(result(),),
    )

    assert assessment.status is QualityStatus.UNKNOWN
    assert assessment.quality_state is QualityAssessmentState.UNKNOWN


def test_profile_version_changes_stable_assessment_reference() -> None:
    first = assess(service_for(profile(version="1")), check_results=(result(),))
    second = assess(service_for(profile(version="2")), check_results=(result(),))

    assert first.profile == "QLT-PROFILE-REPOSITORY@1"
    assert second.profile == "QLT-PROFILE-REPOSITORY@2"
    assert first.profile != second.profile
    assert first.revision == second.revision == TARGET.revision


def test_unresolved_profile_fails_explicitly() -> None:
    with pytest.raises(ValueError, match="No QualityProfile applies"):
        assess(
            service_for(profile(target_types=("documentation",))),
            check_results=(result(),),
        )


def test_ambiguous_profile_resolution_fails_explicitly() -> None:
    registry = QualityProfileRegistry()
    registry.register(profile(version="1"))
    registry.register(profile(version="2"))
    service = QualityProfileAssessmentService(QualityProfileResolver(registry))

    with pytest.raises(ValueError, match="Ambiguous QualityProfile resolution"):
        assess(service, check_results=(result(),))


def test_registration_order_does_not_change_ambiguity() -> None:
    profiles = (profile(version="2"), profile(version="1"))
    messages: list[str] = []

    for ordered in (profiles, tuple(reversed(profiles))):
        registry = QualityProfileRegistry()
        for value in ordered:
            registry.register(value)
        service = QualityProfileAssessmentService(QualityProfileResolver(registry))
        with pytest.raises(ValueError) as error:
            assess(service, check_results=(result(),))
        messages.append(str(error.value))

    assert messages[0] == messages[1]


def test_explicit_blocking_classification_is_preserved() -> None:
    blocker = QualityFinding(
        id=QualityFindingId("QLT-FIND-001"),
        rule_id=QualityRuleId("QLT-RULE-001"),
        domain=QualityDomain("QLT-DOM-TST"),
        severity=QualitySeverity.HIGH,
        status=QualityStatus.FAIL,
        message="explicit blocker",
        target=TARGET,
    )
    assessment = assess(
        service_for(profile()),
        check_results=(
            result(
                status=QualityStatus.FAIL,
                evidence_result=QualityEvidenceResult.FAIL,
                findings=(blocker,),
            ),
        ),
        blocking_finding_ids=(blocker.id,),
    )

    assert assessment.status is QualityStatus.FAIL
    assert assessment.quality_state is QualityAssessmentState.FAIL


def test_severity_policy_does_not_implicitly_create_blocking_finding() -> None:
    finding = QualityFinding(
        id=QualityFindingId("QLT-FIND-001"),
        rule_id=QualityRuleId("QLT-RULE-001"),
        domain=QualityDomain("QLT-DOM-TST"),
        severity=QualitySeverity.HIGH,
        status=QualityStatus.FAIL,
        message="high severity but not explicitly blocking",
        target=TARGET,
    )
    assessment = assess(
        service_for(profile(severity_policy=((QualitySeverity.HIGH, True),))),
        check_results=(
            result(
                status=QualityStatus.FAIL,
                evidence_result=QualityEvidenceResult.FAIL,
                findings=(finding,),
            ),
        ),
        blocking_finding_ids=(),
    )

    assert assessment.status is QualityStatus.UNKNOWN
    assert assessment.quality_state is QualityAssessmentState.UNKNOWN
    assert finding.id in assessment.finding_ids


def test_phase_ten_warning_semantics_are_preserved() -> None:
    assessment = assess(
        service_for(profile()),
        check_results=(
            result(
                status=QualityStatus.WARNING,
                evidence_result=QualityEvidenceResult.WARNING,
            ),
        ),
    )

    assert assessment.status is QualityStatus.WARNING
    assert assessment.quality_state is QualityAssessmentState.PASS_WITH_WARNINGS


def test_constructor_rejects_invalid_dependencies() -> None:
    resolver = QualityProfileResolver(QualityProfileRegistry())

    with pytest.raises(TypeError, match="profile_resolver"):
        QualityProfileAssessmentService(object())  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="assessment_service"):
        QualityProfileAssessmentService(
            resolver,
            object(),  # type: ignore[arg-type]
        )

    assert isinstance(
        QualityProfileAssessmentService(
            resolver,
            QualityAssessmentService(),
        ),
        QualityProfileAssessmentService,
    )
