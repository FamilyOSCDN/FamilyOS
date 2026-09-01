from dataclasses import FrozenInstanceError, fields
from datetime import UTC, datetime
from typing import cast

import pytest

from familyos_cli.domain.quality import (
    INITIAL_QUALITY_EVIDENCE_TYPES,
    QualityEvidence,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityEvidenceType,
    QualityRequirementId,
    QualityRuleId,
    QualityTarget,
)


def evidence(**overrides: object) -> QualityEvidence:
    values: dict[str, object] = {
        "id": QualityEvidenceId("QLT-EVID-ARC-001"),
        "type": QualityEvidenceType("ARCHITECTURE"),
        "source": "quality.architecture",
        "target": QualityTarget(
            "repository",
            "familyos-cli",
            revision="12ec87f",
        ),
        "result": QualityEvidenceResult.PASS,
        "created_at": datetime(2026, 9, 1, 12, 0, tzinfo=UTC),
        "revision": "12ec87f",
        "rule_id": QualityRuleId("QLT-RULE-ARC-001"),
        "requirement_id": QualityRequirementId("QLT-REQ-ARC-001"),
        "tool": "familyos",
        "tool_version": "1",
        "metadata": (("profile", "canonical"),),
        "artifact": "quality-evidence.json",
    }
    values.update(overrides)
    return QualityEvidence(**values)  # type: ignore[arg-type]


def test_initial_evidence_types() -> None:
    assert tuple(item.value for item in INITIAL_QUALITY_EVIDENCE_TYPES) == (
        "TEST",
        "STATIC_ANALYSIS",
        "TYPE_VERIFICATION",
        "ARCHITECTURE",
        "SECURITY",
        "DOCUMENTATION",
        "BUILD",
        "PERFORMANCE",
        "COMPATIBILITY",
        "COMPLIANCE",
        "OBSERVABILITY",
        "MANUAL_REVIEW",
        "METRIC",
    )


def test_evidence_type_is_extensible() -> None:
    assert QualityEvidenceType("FUTURE_CATEGORY").value == "FUTURE_CATEGORY"


@pytest.mark.parametrize(
    "value",
    (
        "",
        "architecture",
        "TYPE-CHECK",
        " STATIC_ANALYSIS",
        "STATIC ANALYSIS",
    ),
)
def test_evidence_type_rejects_non_canonical_values(value: str) -> None:
    with pytest.raises(ValueError):
        QualityEvidenceType(value)


def test_evidence_type_rejects_non_string() -> None:
    with pytest.raises(TypeError):
        QualityEvidenceType(cast(str, object()))


def test_type_check_alias_is_rejected() -> None:
    assert "TYPE_CHECK" not in {item.value for item in INITIAL_QUALITY_EVIDENCE_TYPES}

    with pytest.raises(
        ValueError,
        match="TYPE_CHECK is not canonical; use TYPE_VERIFICATION",
    ):
        QualityEvidenceType("TYPE_CHECK")


def test_evidence_result_vocabulary() -> None:
    assert tuple(item.value for item in QualityEvidenceResult) == (
        "PASS",
        "WARNING",
        "FAIL",
        "ERROR",
        "SKIPPED",
        "NOT_APPLICABLE",
    )


def test_evidence_id() -> None:
    value = QualityEvidenceId("QLT-EVID-ARC-001")
    assert value.value == "QLT-EVID-ARC-001"
    assert str(value) == "QLT-EVID-ARC-001"


@pytest.mark.parametrize(
    "value",
    (
        "QLT-RULE-ARC-001",
        "QLT-EVID-",
        " QLT-EVID-ARC-001",
        "QLT-EVID-ARC 001",
    ),
)
def test_evidence_id_rejects_invalid_values(value: str) -> None:
    with pytest.raises(ValueError):
        QualityEvidenceId(value)


def test_evidence_shape_and_immutability() -> None:
    item = evidence()
    assert [field.name for field in fields(QualityEvidence)] == [
        "id",
        "type",
        "source",
        "target",
        "result",
        "created_at",
        "revision",
        "rule_id",
        "requirement_id",
        "tool",
        "tool_version",
        "metadata",
        "artifact",
    ]
    with pytest.raises(FrozenInstanceError):
        item.source = "changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field_name", "value"),
    (
        ("id", "QLT-EVID-ARC-001"),
        ("type", "ARCHITECTURE"),
        ("target", "repository"),
        ("result", "PASS"),
    ),
)
def test_evidence_rejects_non_canonical_typed_fields(
    field_name: str,
    value: object,
) -> None:
    with pytest.raises(TypeError):
        evidence(**{field_name: value})


def test_evidence_rejects_empty_source() -> None:
    with pytest.raises(ValueError, match="source must be non-empty"):
        evidence(source="")


def test_evidence_rejects_non_datetime_created_at() -> None:
    with pytest.raises(TypeError, match="created_at must be a datetime"):
        evidence(created_at="2026-09-01T12:00:00Z")


def test_evidence_rejects_naive_datetime() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        evidence(created_at=datetime(2026, 9, 1, 12, 0))


@pytest.mark.parametrize(
    "field_name",
    ("revision", "tool", "tool_version", "artifact"),
)
def test_evidence_rejects_empty_optional_text(field_name: str) -> None:
    with pytest.raises(ValueError, match=f"{field_name} must be non-empty"):
        evidence(**{field_name: ""})


def test_evidence_allows_absent_optional_traceability() -> None:
    item = evidence(
        revision=None,
        rule_id=None,
        requirement_id=None,
        tool=None,
        tool_version=None,
        artifact=None,
    )
    assert item.revision is None
    assert item.rule_id is None
    assert item.requirement_id is None


def test_evidence_rejects_invalid_rule_reference() -> None:
    with pytest.raises(TypeError, match="rule_id must be a QualityRuleId"):
        evidence(rule_id="QLT-RULE-ARC-001")


def test_evidence_rejects_invalid_requirement_reference() -> None:
    with pytest.raises(
        TypeError,
        match="requirement_id must be a QualityRequirementId",
    ):
        evidence(requirement_id="QLT-REQ-ARC-001")


def test_evidence_metadata_is_immutable_shape() -> None:
    item = evidence(metadata=(("profile", "canonical"),))
    assert item.metadata == (("profile", "canonical"),)

    with pytest.raises(TypeError, match="metadata must be a tuple"):
        evidence(
            metadata=cast(
                tuple[tuple[str, str], ...],
                {"profile": "canonical"},
            )
        )


@pytest.mark.parametrize(
    "metadata",
    (
        (("", "canonical"),),
        (("profile", ""),),
    ),
)
def test_evidence_rejects_empty_metadata_components(
    metadata: tuple[tuple[str, str], ...],
) -> None:
    with pytest.raises(ValueError, match="must be non-empty"):
        evidence(metadata=metadata)


def test_evidence_rejects_malformed_metadata_entry() -> None:
    with pytest.raises(TypeError, match="metadata entries"):
        evidence(
            metadata=cast(
                tuple[tuple[str, str], ...],
                (("profile",),),
            )
        )
