"""Tests for SecurityDecision."""

from familyos_cli.plugins.builtin.security.domain.security_decision import (
    SecurityDecision,
)


def test_security_decision_values() -> None:
    """Security decisions expose expected values."""

    assert SecurityDecision.ALLOW.value == "allow"
    assert SecurityDecision.DENY.value == "deny"
    assert SecurityDecision.REVIEW.value == "review"


def test_security_decision_contains_all_decisions() -> None:
    """Security decisions contain three entries."""

    assert len(SecurityDecision) == 3
