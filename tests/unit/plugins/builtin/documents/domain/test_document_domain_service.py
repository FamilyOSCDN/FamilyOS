"""Tests for DocumentDomainService."""

from familyos_cli.plugins.builtin.documents.domain.document_context import (
    DocumentContext,
)
from familyos_cli.plugins.builtin.documents.domain.document_decision import (
    DocumentDecision,
)
from familyos_cli.plugins.builtin.documents.domain.document_domain_service import (
    DocumentDomainService,
)
from familyos_cli.plugins.builtin.documents.domain.document_level import (
    DocumentLevel,
)


def test_standard_document_level_allows_access() -> None:
    """Standard document levels should be allowed."""

    service = DocumentDomainService()

    context = DocumentContext(
        domain_name="family",
        subject="member",
        required_level=DocumentLevel.STANDARD,
    )

    decision = service.evaluate(
        context,
    )

    assert decision == DocumentDecision.ALLOW


def test_critical_document_level_requires_review() -> None:
    """Critical document levels should require review."""

    service = DocumentDomainService()

    context = DocumentContext(
        domain_name="family",
        subject="member",
        required_level=DocumentLevel.CRITICAL,
    )

    decision = service.evaluate(
        context,
    )

    assert decision == DocumentDecision.REVIEW