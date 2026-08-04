import pytest

from familyos_cli.plugins.builtin.documents.rules.document_rule import (
    DocumentRule,
)
from familyos_cli.plugins.builtin.documents.rules.document_rule_set import (
    DocumentRuleSet,
)


def create_rule(
    rule_id: str,
) -> DocumentRule:
    return DocumentRule(
        id=rule_id,
        name="Document Rule",
        version="1.0.0",
        severity="LOW",
    )


def test_document_rule_set_is_empty_by_default() -> None:
    rule_set = DocumentRuleSet()

    assert rule_set.list() == ()


def test_document_rule_set_preserves_order() -> None:
    first = create_rule(
        "documents.rule.first",
    )

    second = create_rule(
        "documents.rule.second",
    )

    rule_set = DocumentRuleSet(
        rules=(
            first,
            second,
        ),
    )

    assert rule_set.list() == (
        first,
        second,
    )


def test_document_rule_set_returns_rule_by_id() -> None:
    rule = create_rule(
        "documents.rule.required-metadata",
    )

    rule_set = DocumentRuleSet(
        rules=(rule,),
    )

    assert rule_set.get(
        "documents.rule.required-metadata",
    ) is rule


def test_document_rule_set_returns_none_for_unknown_id() -> None:
    rule_set = DocumentRuleSet()

    assert rule_set.get(
        "documents.rule.unknown",
    ) is None


def test_document_rule_set_rejects_duplicate_ids() -> None:
    first = create_rule(
        "documents.rule.required-metadata",
    )

    duplicate = create_rule(
        "documents.rule.required-metadata",
    )

    with pytest.raises(
        ValueError,
        match="must be unique",
    ):
        DocumentRuleSet(
            rules=(
                first,
                duplicate,
            ),
        )
