"""Tests for SecurityRule."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.security.rules.security_rule import (
    SecurityRule,
)


def create_rule(
    **overrides: str,
) -> SecurityRule:
    """Create a security rule for tests."""

    values = {
        "id": "security.rule.basic",
        "name": "Basic Security Rule",
        "version": "1.0.0",
        "severity": "LOW",
        "description": "",
    }
    values.update(
        overrides,
    )

    return SecurityRule(
        id=values["id"],
        name=values["name"],
        version=values["version"],
        severity=values["severity"],
        description=values["description"],
    )


def test_security_rule_can_be_created() -> None:
    rule = SecurityRule(
        id="security.rule.password-policy",
        name="Password Policy Rule",
        version="1.0.0",
        severity="HIGH",
        description="Checks password requirements.",
    )

    assert rule.id == "security.rule.password-policy"
    assert rule.name == "Password Policy Rule"
    assert rule.version == "1.0.0"
    assert rule.severity == "HIGH"
    assert rule.description == (
        "Checks password requirements."
    )


def test_security_rule_description_is_optional() -> None:
    rule = create_rule()

    assert rule.description == ""


def test_security_rule_is_immutable() -> None:
    rule = create_rule()

    with pytest.raises(FrozenInstanceError):
        rule.severity = "HIGH"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "message"),
    [
        (
            "id",
            "Security rule id cannot be empty.",
        ),
        (
            "name",
            "Security rule name cannot be empty.",
        ),
        (
            "version",
            "Security rule version cannot be empty.",
        ),
        (
            "severity",
            "Security rule severity cannot be empty.",
        ),
    ],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        "",
        "   ",
    ],
)
def test_security_rule_rejects_empty_required_fields(
    field: str,
    message: str,
    invalid_value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=message,
    ):
        create_rule(
            **{
                field: invalid_value,
            },
        )
