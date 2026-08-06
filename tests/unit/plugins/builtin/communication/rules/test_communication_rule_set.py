"""Tests for CommunicationRuleSet."""

import pytest

from familyos_cli.plugins.builtin.communication.rules import (
    CommunicationRule,
    CommunicationRuleSet,
)


def create_rule(
    rule_id: str,
) -> CommunicationRule:
    return CommunicationRule(
        id=rule_id,
        name="Communication Rule",
        version="1.0.0",
        severity="LOW",
    )


def test_communication_rule_set_is_empty_by_default() -> None:
    rule_set = CommunicationRuleSet()

    assert rule_set.list() == ()


def test_communication_rule_set_preserves_order() -> None:
    first = create_rule(
        "communication.rule.first",
    )

    second = create_rule(
        "communication.rule.second",
    )

    rule_set = CommunicationRuleSet(
        rules=(
            first,
            second,
        ),
    )

    assert rule_set.list() == (
        first,
        second,
    )


def test_communication_rule_set_returns_rule_by_id() -> None:
    rule = create_rule(
        "communication.rule.retention",
    )

    rule_set = CommunicationRuleSet(
        rules=(rule,),
    )

    assert rule_set.get(
        "communication.rule.retention",
    ) is rule


def test_communication_rule_set_returns_none_for_unknown_id() -> None:
    rule_set = CommunicationRuleSet()

    assert rule_set.get(
        "communication.rule.unknown",
    ) is None


def test_communication_rule_set_rejects_duplicate_ids() -> None:
    first = create_rule(
        "communication.rule.retention",
    )

    duplicate = create_rule(
        "communication.rule.retention",
    )

    with pytest.raises(
        ValueError,
        match="must be unique",
    ):
        CommunicationRuleSet(
            rules=(
                first,
                duplicate,
            ),
        )
