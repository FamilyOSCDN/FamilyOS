"""Tests for EducationDomainService."""

from familyos_cli.plugins.builtin.education.domain.education_context import (
    EducationContext,
)
from familyos_cli.plugins.builtin.education.domain.education_decision import (
    EducationDecision,
)
from familyos_cli.plugins.builtin.education.domain.education_domain_service import (
    EducationDomainService,
)
from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)


def test_standard_education_context_is_allowed() -> None:
    """Standard context should be allowed."""

    service = EducationDomainService()

    context = EducationContext(
        domain_name="family_learning",
        subject="student",
        required_level=EducationLevel.STANDARD,
    )

    assert service.evaluate(
        context,
    ) == EducationDecision.ALLOW


def test_critical_education_context_requires_review() -> None:
    """Critical context should require review."""

    service = EducationDomainService()

    context = EducationContext(
        domain_name="family_learning",
        subject="student",
        required_level=EducationLevel.CRITICAL,
    )

    assert service.evaluate(
        context,
    ) == EducationDecision.REVIEW
