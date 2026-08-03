from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.security.rules.security_rule import (
    SecurityRule,
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
    rule = SecurityRule(
        id="security.rule.basic",
        name="Basic Security Rule",
        version="1.0.0",
        severity="LOW",
    )

    assert rule.description == ""


def test_security_rule_is_immutable() -> None:
    rule = SecurityRule(
        id="security.rule.basic",
        name="Basic Security Rule",
        version="1.0.0",
        severity="LOW",
    )

    with pytest.raises(FrozenInstanceError):
        rule.severity = "HIGH"  # type: ignore[misc]
