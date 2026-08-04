from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.documents.policies.document_policy import (
    DocumentPolicy,
)


def test_document_policy_can_be_created() -> None:
    policy = DocumentPolicy(
        id="documents.policy.retention",
        name="Document Retention Policy",
        version="1.0.0",
        description=(
            "Defines document retention rules."
        ),
    )

    assert policy.id == (
        "documents.policy.retention"
    )

    assert policy.name == (
        "Document Retention Policy"
    )

    assert policy.version == "1.0.0"

    assert policy.description == (
        "Defines document retention rules."
    )


def test_document_policy_description_is_optional() -> None:
    policy = DocumentPolicy(
        id="documents.policy.basic",
        name="Basic Document Policy",
        version="1.0.0",
    )

    assert policy.description == ""


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    [
        ("id", ""),
        ("name", ""),
        ("version", ""),
        ("id", "   "),
        ("name", "   "),
        ("version", "   "),
    ],
)
def test_document_policy_rejects_empty_required_fields(
    field_name: str,
    field_value: str,
) -> None:
    values = {
        "id": "documents.policy.basic",
        "name": "Basic Document Policy",
        "version": "1.0.0",
    }

    values[field_name] = field_value

    with pytest.raises(ValueError):
        DocumentPolicy(**values)


def test_document_policy_is_immutable() -> None:
    policy = DocumentPolicy(
        id="documents.policy.basic",
        name="Basic Document Policy",
        version="1.0.0",
    )

    with pytest.raises(FrozenInstanceError):
        policy.version = "2.0.0"  # type: ignore[misc]
