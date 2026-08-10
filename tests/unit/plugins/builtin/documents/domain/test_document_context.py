"""Tests for DocumentContext."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.documents.domain.document_context import (
    DocumentContext,
)
from familyos_cli.plugins.builtin.documents.domain.document_level import (
    DocumentLevel,
)


def test_document_context_can_be_created() -> None:
    """Document context stores values."""

    context = DocumentContext(
        domain_name="family",
        subject="member",
        required_level=DocumentLevel.STANDARD,
    )

    assert context.domain_name == "family"
    assert context.subject == "member"
    assert context.required_level == DocumentLevel.STANDARD


def test_document_context_is_immutable() -> None:
    """Document context cannot be modified."""

    context = DocumentContext(
        domain_name="family",
        subject="member",
        required_level=DocumentLevel.BASIC,
    )

    with pytest.raises(FrozenInstanceError):
        context.subject = "other"  # type: ignore[misc]