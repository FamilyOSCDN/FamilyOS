from dataclasses import FrozenInstanceError, fields
from typing import cast

import pytest

from familyos_cli.domain.quality import (
    INITIAL_QUALITY_DOMAINS,
    QualityDomain,
    QualityFinding,
    QualityFindingId,
    QualityRequirement,
    QualityRequirementId,
    QualityRule,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)


def test_vocabularies() -> None:
    assert tuple(x.value for x in QualitySeverity) == (
        "INFO",
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    )
    assert tuple(x.value for x in QualityStatus) == (
        "PASS",
        "WARNING",
        "FAIL",
        "ERROR",
        "SKIPPED",
        "UNKNOWN",
    )


def test_domains() -> None:
    assert len(INITIAL_QUALITY_DOMAINS) == 17
    assert QualityDomain("QLT-DOM-FUTURE").value == "QLT-DOM-FUTURE"


@pytest.mark.parametrize(
    "cls,value",
    [
        (QualityDomain, "QLT-DOM-ARC"),
        (QualityRequirementId, "QLT-REQ-ARCH-001"),
        (QualityRuleId, "QLT-RULE-ARC-001"),
        (QualityFindingId, "QLT-FIND-9812"),
    ],
)
def test_ids(cls: type, value: str) -> None:
    x = cls(value)
    assert x.value == value and str(x) == value


def test_id_validation_and_immutability() -> None:
    with pytest.raises(ValueError):
        QualityRuleId("QLT-REQ-X")
    with pytest.raises(TypeError):
        QualityRuleId(cast(str, object()))
    x = QualityRuleId("QLT-RULE-X")
    with pytest.raises(FrozenInstanceError):
        x.value = "QLT-RULE-Y"  # type: ignore[misc]


def test_target() -> None:
    assert [f.name for f in fields(QualityTarget)] == [
        "target_type",
        "identifier",
        "revision",
        "version",
        "path",
        "metadata",
    ]
    x = QualityTarget("repository", "familyos-cli", metadata=(("language", "python"),))
    assert x.metadata == (("language", "python"),)
    with pytest.raises(TypeError):
        QualityTarget(
            "repository", "x", metadata=cast(tuple[tuple[str, str], ...], {"x": "y"})
        )


def target() -> QualityTarget:
    return QualityTarget("package", "familyos_cli.domain.quality")


def test_finding() -> None:
    x = QualityFinding(
        QualityFindingId("QLT-FIND-X"),
        QualityRuleId("QLT-RULE-X"),
        QualityDomain("QLT-DOM-ARC"),
        QualitySeverity.HIGH,
        QualityStatus.FAIL,
        "message",
        target(),
        evidence_ids=("QLT-EVID-X",),
    )
    assert x.evidence_ids == ("QLT-EVID-X",)
    with pytest.raises(ValueError):
        QualityFinding(
            QualityFindingId("QLT-FIND-X"),
            QualityRuleId("QLT-RULE-X"),
            QualityDomain("QLT-DOM-ARC"),
            QualitySeverity.HIGH,
            QualityStatus.FAIL,
            "message",
            target(),
            evidence_ids=("QLT-RULE-X",),
        )


def test_requirement() -> None:
    x = QualityRequirement(
        QualityRequirementId("QLT-REQ-X"),
        "title",
        "description",
        QualityDomain("QLT-DOM-ARC"),
        "authority",
        True,
        "scope",
        "verification",
    )
    assert x.mandatory is True
    with pytest.raises(TypeError):
        QualityRequirement(
            QualityRequirementId("QLT-REQ-X"),
            "title",
            "description",
            QualityDomain("QLT-DOM-ARC"),
            "authority",
            cast(bool, 1),
            "scope",
            "verification",
        )


def test_rule() -> None:
    x = QualityRule(
        QualityRuleId("QLT-RULE-X"),
        None,
        QualityDomain("QLT-DOM-ARC"),
        QualitySeverity.HIGH,
        "description",
    )
    assert x.requirement_id is None and x.executor is None


@pytest.mark.parametrize(
    ("identifier_type", "value"),
    [
        (QualityDomain, "QLT-DOM-"),
        (QualityRequirementId, "QLT-REQ-"),
        (QualityRuleId, "QLT-RULE-"),
        (QualityFindingId, "QLT-FIND-"),
    ],
)
def test_identifiers_reject_empty_suffixes(identifier_type: type, value: str) -> None:
    with pytest.raises(ValueError, match="non-empty suffix"):
        identifier_type(value)


@pytest.mark.parametrize(
    ("identifier_type", "value"),
    [
        (QualityDomain, " QLT-DOM-ARC"),
        (QualityRequirementId, "QLT-REQ-ARC 001"),
        (QualityRuleId, "QLT-RULE-ARC-001 "),
        (QualityFindingId, "QLT-FIND-ARC\t001"),
    ],
)
def test_identifiers_reject_non_canonical_whitespace(
    identifier_type: type, value: str
) -> None:
    with pytest.raises(ValueError):
        identifier_type(value)


@pytest.mark.parametrize("field_name", ["target_type", "identifier"])
def test_target_rejects_empty_required_strings(field_name: str) -> None:
    values = {"target_type": "repository", "identifier": "familyos-cli"}
    values[field_name] = ""
    with pytest.raises(ValueError, match="must be non-empty"):
        QualityTarget(**values)


@pytest.mark.parametrize("field_name", ["revision", "version", "path"])
def test_target_rejects_empty_optional_strings(field_name: str) -> None:
    values: dict[str, object] = {
        "target_type": "repository",
        "identifier": "familyos-cli",
        field_name: "",
    }
    with pytest.raises(ValueError, match="must be non-empty"):
        QualityTarget(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize("metadata", [(("", "python"),), (("language", ""),)])
def test_target_rejects_empty_metadata_components(
    metadata: tuple[tuple[str, str], ...],
) -> None:
    with pytest.raises(ValueError, match="must be non-empty"):
        QualityTarget("repository", "familyos-cli", metadata=metadata)


def test_target_rejects_malformed_metadata_entry() -> None:
    with pytest.raises(TypeError, match="metadata entries"):
        QualityTarget(
            "repository",
            "familyos-cli",
            metadata=cast(tuple[tuple[str, str], ...], (("language",),)),
        )


def _finding_for_validation(**overrides: object) -> QualityFinding:
    values: dict[str, object] = {
        "id": QualityFindingId("QLT-FIND-ARC-001"),
        "rule_id": QualityRuleId("QLT-RULE-ARC-001"),
        "domain": QualityDomain("QLT-DOM-ARC"),
        "severity": QualitySeverity.HIGH,
        "status": QualityStatus.FAIL,
        "message": "Architecture boundary violated",
        "target": target(),
        "location": "quality_rule.py",
        "evidence_ids": ("QLT-EVID-ARC-001",),
    }
    values.update(overrides)
    return QualityFinding(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("id", "QLT-FIND-ARC-001"),
        ("rule_id", "QLT-RULE-ARC-001"),
        ("domain", "QLT-DOM-ARC"),
        ("severity", "HIGH"),
        ("status", "FAIL"),
        ("target", "package"),
    ],
)
def test_finding_rejects_non_canonical_typed_fields(
    field_name: str, value: object
) -> None:
    with pytest.raises(TypeError):
        _finding_for_validation(**{field_name: value})


def test_finding_rejects_empty_message_and_location() -> None:
    with pytest.raises(ValueError, match="message must be non-empty"):
        _finding_for_validation(message="")
    with pytest.raises(ValueError, match="location must be non-empty"):
        _finding_for_validation(location="")


def test_finding_rejects_non_tuple_evidence_ids() -> None:
    with pytest.raises(TypeError, match="evidence_ids must be a tuple"):
        _finding_for_validation(
            evidence_ids=cast(tuple[str, ...], ["QLT-EVID-ARC-001"])
        )


@pytest.mark.parametrize("evidence_ids", [("QLT-EVID-",), ("QLT-EVID-ARC 001",)])
def test_finding_rejects_invalid_evidence_identifiers(
    evidence_ids: tuple[str, ...],
) -> None:
    with pytest.raises(ValueError):
        _finding_for_validation(evidence_ids=evidence_ids)


def _requirement_for_validation(**overrides: object) -> QualityRequirement:
    values: dict[str, object] = {
        "id": QualityRequirementId("QLT-REQ-ARC-001"),
        "title": "Architecture",
        "description": "Preserve dependency direction",
        "domain": QualityDomain("QLT-DOM-ARC"),
        "authority": "Quality Framework",
        "mandatory": True,
        "applicability": "Python packages",
        "verification": "Validate imports",
    }
    values.update(overrides)
    return QualityRequirement(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    ["title", "description", "authority", "applicability", "verification"],
)
def test_requirement_rejects_empty_required_text(field_name: str) -> None:
    with pytest.raises(ValueError, match=f"{field_name} must be non-empty"):
        _requirement_for_validation(**{field_name: ""})


def test_requirement_rejects_non_canonical_domain() -> None:
    with pytest.raises(TypeError, match="domain must be a QualityDomain"):
        _requirement_for_validation(domain="QLT-DOM-ARC")


def _rule_for_validation(**overrides: object) -> QualityRule:
    values: dict[str, object] = {
        "id": QualityRuleId("QLT-RULE-ARC-001"),
        "requirement_id": QualityRequirementId("QLT-REQ-ARC-001"),
        "domain": QualityDomain("QLT-DOM-ARC"),
        "severity": QualitySeverity.HIGH,
        "description": "Reject outward dependencies",
        "executor": "quality.architecture.import-boundary",
    }
    values.update(overrides)
    return QualityRule(**values)  # type: ignore[arg-type]


def test_rule_rejects_non_canonical_requirement_reference() -> None:
    with pytest.raises(
        TypeError, match="requirement_id must be a QualityRequirementId"
    ):
        _rule_for_validation(requirement_id="QLT-REQ-ARC-001")


def test_rule_rejects_non_canonical_severity() -> None:
    with pytest.raises(TypeError, match="severity must be a QualitySeverity"):
        _rule_for_validation(severity="HIGH")


def test_rule_rejects_empty_description() -> None:
    with pytest.raises(ValueError, match="description must be non-empty"):
        _rule_for_validation(description="")


def test_rule_rejects_invalid_executor_reference() -> None:
    with pytest.raises(TypeError, match="executor must be a str"):
        _rule_for_validation(executor=object())
    with pytest.raises(ValueError, match="executor must be non-empty"):
        _rule_for_validation(executor="")
