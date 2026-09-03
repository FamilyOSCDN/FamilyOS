"""Contracts for the retained Quality application output."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from familyos_cli.application.quality import (
    QualityAssessmentExecutionResult,
    QualityAssessmentService,
    QualityCheckResult,
)
from familyos_cli.domain.quality import (
    QualityAssessment,
    QualityAssessmentId,
    QualityAssessmentState,
    QualityCheckId,
    QualityStatus,
    QualityTarget,
)


@pytest.fixture
def assessment() -> QualityAssessment:
    return QualityAssessmentService().assess(
        assessment_id=QualityAssessmentId("QLT-ASMT-TEST"),
        target=QualityTarget(target_type="repository", identifier="test"),
        profile="QLT-PROFILE-REPOSITORY@1",
        required_check_ids=(QualityCheckId("QLT-CHECK-RUFF"),),
        check_results=(),
        blocking_finding_ids=(),
        created_at=datetime(2026, 9, 3, tzinfo=UTC),
    )


def test_output_retains_an_empty_incomplete_execution(
    assessment: QualityAssessment,
) -> None:
    output = QualityAssessmentExecutionResult(assessment, ())

    assert output.assessment is assessment
    assert output.check_results == ()
    assert output.assessment.status is QualityStatus.UNKNOWN
    assert output.assessment.quality_state is QualityAssessmentState.UNKNOWN


@pytest.mark.parametrize("field", ("assessment", "check_results"))
def test_output_fields_are_immutable(
    assessment: QualityAssessment, field: str,
) -> None:
    output = QualityAssessmentExecutionResult(assessment, ())

    with pytest.raises(FrozenInstanceError):
        setattr(output, field, ())


def test_output_rejects_an_invalid_assessment() -> None:
    with pytest.raises(TypeError, match="assessment must be a QualityAssessment"):
        QualityAssessmentExecutionResult(object(), ())  # type: ignore[arg-type]


@pytest.mark.parametrize("check_results", ([], None, (object(),)))
def test_output_rejects_invalid_result_collections(
    assessment: QualityAssessment, check_results: object,
) -> None:
    with pytest.raises(TypeError, match="check_results must"):
        QualityAssessmentExecutionResult(
            assessment, check_results,  # type: ignore[arg-type]
        )


def test_output_retains_incomplete_check_details_without_coercion(
    assessment: QualityAssessment,
) -> None:
    check = QualityCheckResult(
        check_id=QualityCheckId("QLT-CHECK-RUFF"),
        status=QualityStatus.ERROR,
        duration_seconds=1.25,
        diagnostics=("tool could not start", "tool could not start"),
    )
    checks = (check,)

    output = QualityAssessmentExecutionResult(assessment, checks)

    assert output.check_results is checks
    assert output.check_results[0] is check
    assert output.check_results[0].evidence == ()
    assert output.check_results[0].diagnostics == check.diagnostics
