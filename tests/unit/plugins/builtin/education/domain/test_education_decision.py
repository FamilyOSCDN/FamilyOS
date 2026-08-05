"""Tests for EducationDecision."""

from familyos_cli.plugins.builtin.education.domain.education_decision import (
    EducationDecision,
)


def test_education_decisions_exist() -> None:
    """Education decisions are available."""

    assert EducationDecision.ALLOW.value == "allow"
    assert EducationDecision.REVIEW.value == "review"
    assert EducationDecision.DENY.value == "deny"
