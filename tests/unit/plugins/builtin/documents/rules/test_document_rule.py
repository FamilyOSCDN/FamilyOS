from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.documents.rules.document_rule import (
    DocumentRule,
)


def test_document_rule_can_be_created() -> None:
    rule = DocumentRule(
        id="documents.rule.required-metadata",
        name="Required Metadata Rule",
        version="1.0.0",
        severity="HIGH",
        description=(
            "Requires mandatory document metadata."
        ),
    )

    assert rule.id == (
        "documents.rule.required-metadata"
    )

    assert rule.name == (
        "Required Metadata Rule"
    )

    assert rule.version == "1.0.0"

    assert rule.severity == "HIGH"

    assert rule.description == (
        "Requires mandatory document metadata."
    )


def test_document_rule_description_is_optional() -> None:
    rule = DocumentRule(
        id="documents.rule.basic",
        name="Basic Document Rule",
        version="1.0.0",
        severity="LOW",
    )

    assert rule.description == ""


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    [
        ("id", ""),
        ("name", ""),
        ("version", ""),
        ("severity", ""),
        ("id", "   "),
        ("name", "   "),
        ("version", "   "),
        ("severity", "   "),
    ],
)
def test_document_rule_rejects_empty_required_fields(
    field_name: str,
    field_value: str,
) -> None:
    values = {
        "id": "documents.rule.basic",
        "name": "Basic Document Rule",
        "version": "1.0.0",
        "severity": "LOW",
    }

    values[field_name] = field_value

    with pytest.raises(ValueError):
        DocumentRule(**values)


def test_document_rule_is_immutable() -> None:
    rule = DocumentRule(
        id="documents.rule.basic",
        name="Basic Document Rule",
        version="1.0.0",
        severity="LOW",
    )

    with pytest.raises(FrozenInstanceError):
        rule.severity = "HIGH"  # type: ignore[misc]
