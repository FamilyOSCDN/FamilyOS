"""Tests for DocumentDecision."""

from familyos_cli.plugins.builtin.documents.domain.document_decision import (
    DocumentDecision,
)


def test_document_decision_values() -> None:
    """Document decisions expose expected values."""

    assert DocumentDecision.ALLOW.value == "allow"
    assert DocumentDecision.REVIEW.value == "review"
    assert DocumentDecision.DENY.value == "deny"