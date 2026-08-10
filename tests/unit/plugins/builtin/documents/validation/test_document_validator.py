"""Tests for DocumentValidator."""

from familyos_cli.plugins.builtin.documents.domain.document_context import (
    DocumentContext,
)
from familyos_cli.plugins.builtin.documents.domain.document_level import (
    DocumentLevel,
)
from familyos_cli.plugins.builtin.documents.validation.document_validator import (
    DocumentValidator,
)


def test_standard_context_is_valid() -> None:
    """Standard document context should be valid."""

    validator = DocumentValidator()

    context = DocumentContext(
        domain_name="family",
        subject="member",
        required_level=DocumentLevel.STANDARD,
    )

    result = validator.validate(
        context,
    )

    assert result.valid is True
    assert result.message == (
        "Document context validated."
    )


def test_critical_context_requires_review() -> None:
    """Critical document context should fail validation."""

    validator = DocumentValidator()

    context = DocumentContext(
        domain_name="family",
        subject="member",
        required_level=DocumentLevel.CRITICAL,
    )

    result = validator.validate(
        context,
    )

    assert result.valid is False
    assert result.message == (
        "Critical document review required."
    )