"""Tests for CommunicationRule."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.communication.rules import (
    CommunicationRule,
)


def test_communication_rule_can_be_created() -> None:
    rule = CommunicationRule(
        id="communication.rule.retention",
        name="Communication Retention Rule",
        version="1.0.0",
        severity="HIGH",
        description=(
            "Defines communication retention rules."
        ),
    )

    assert rule.id == (
        "communication.rule.retention"
    )

    assert rule.name == (
        "Communication Retention Rule"
    )

    assert rule.version == "1.0.0"

    assert rule.severity == "HIGH"

    assert rule.description == (
        "Defines communication retention rules."
    )


def test_communication_rule_description_is_optional() -> None:
    rule = CommunicationRule(
        id="communication.rule.basic",
        name="Basic Communication Rule",
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
def test_communication_rule_rejects_empty_required_fields(
    field_name: str,
    field_value: str,
) -> None:
    values = {
        "id": "communication.rule.basic",
        "name": "Basic Communication Rule",
        "version": "1.0.0",
        "severity": "LOW",
    }

    values[field_name] = field_value

    with pytest.raises(ValueError):
        CommunicationRule(**values)


def test_communication_rule_is_immutable() -> None:
    rule = CommunicationRule(
        id="communication.rule.basic",
        name="Basic Communication Rule",
        version="1.0.0",
        severity="LOW",
    )

    with pytest.raises(FrozenInstanceError):
        rule.severity = "HIGH"  # type: ignore[misc]
