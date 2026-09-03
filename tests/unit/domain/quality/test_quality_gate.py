from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime
from typing import Any

import pytest

from familyos_cli.domain.quality import (
    GateDecision,
    QualityAssessmentId,
    QualityAssessmentState,
    QualityCheckId,
    QualityEvidenceId,
    QualityGate,
    QualityGateCondition,
    QualityGateId,
    QualityGatePolicy,
    QualityProfile,
    QualityProfileId,
    QualityStatus,
    QualityTarget,
)


def _policy() -> QualityGatePolicy:
    return QualityGatePolicy(
        QualityGateId("QLT-GATE-MERGE-001"),
        "1.0.0",
        "governed authority",
        QualityProfile(
            QualityProfileId("QLT-PROFILE-TEST"),
            "1",
            ("repository",),
            (QualityCheckId("QLT-CHECK-TEST"),),
            (),
            (),
        ),
        (QualityStatus.PASS,),
        (QualityAssessmentState.PASS,),
    )


def _gate() -> QualityGate:
    return QualityGate(
        QualityGateId("QLT-GATE-MERGE-001"),
        QualityTarget("repository", "test", revision="abc"),
        "abc",
        "QLT-GATE-MERGE-001@1",
        QualityAssessmentId("QLT-ASMT-TEST"),
        GateDecision.PASS,
        (),
        datetime(2026, 9, 3, tzinfo=UTC),
    )


@pytest.mark.parametrize(
    "identifier", ["", "QLT-GATE-", "QLT-CHECK-001", " QLT-GATE-X", "QLT-GATE-A B"]
)
def test_gate_identity_uses_its_canonical_namespace(identifier: str) -> None:
    with pytest.raises((TypeError, ValueError)):
        QualityGateId(identifier)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("version", ""),
        ("authority", " "),
        ("gate_id", "QLT-GATE-X"),
        ("accepted_check_statuses", ()),
        ("accepted_check_statuses", [QualityStatus.PASS]),
        ("accepted_check_statuses", (QualityStatus.PASS, QualityStatus.PASS)),
        ("accepted_check_statuses", (QualityStatus.ERROR,)),
        ("accepted_assessment_states", (QualityAssessmentState.UNKNOWN,)),
        (
            "accepted_assessment_states",
            (QualityAssessmentState.PASS, QualityAssessmentState.PASS),
        ),
    ],
)
def test_policy_rejects_invalid_or_nonpositive_acceptance(
    field: str, value: Any
) -> None:
    with pytest.raises((TypeError, ValueError)):
        replace(_policy(), **{field: value})


def test_policy_cannot_create_an_empty_success_gate() -> None:
    policy = _policy()
    with pytest.raises(ValueError, match="required checks"):
        replace(policy, profile=replace(policy.profile, required_checks=()))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("code", ""),
        ("message", " "),
        ("check_id", "QLT-CHECK-X"),
        ("finding_ids", []),
        ("rule_ids", ("QLT-RULE-X",)),
        (
            "evidence_ids",
            (QualityEvidenceId("QLT-EVID-X"), QualityEvidenceId("QLT-EVID-X")),
        ),
    ],
)
def test_condition_requires_canonical_explanation_and_references(
    field: str, value: Any
) -> None:
    with pytest.raises((TypeError, ValueError)):
        replace(
            QualityGateCondition("missing", "Required input missing"), **{field: value}
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("revision", "other"),
        ("policy", ""),
        ("assessment_id", None),
        ("decision", "PASS"),
        ("decision", GateDecision.FAIL),
        ("blocking_conditions", (QualityGateCondition("failed", "failure"),)),
        ("evaluated_at", datetime(2026, 9, 3)),
        ("blocking_conditions", []),
    ],
)
def test_gate_rejects_inconsistent_decisions(field: str, value: Any) -> None:
    with pytest.raises((TypeError, ValueError)):
        replace(_gate(), **{field: value})


def test_models_are_immutable_and_observation_cannot_enable_enforcement() -> None:
    gate = _gate()
    policy = _policy()
    with pytest.raises(FrozenInstanceError):
        gate.policy = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        policy.version = "changed"  # type: ignore[misc]
    assert gate.mode == policy.mode == "OBSERVE"
    assert gate.prevents_progression is False
    assert policy.reference == "QLT-GATE-MERGE-001@1.0.0"
