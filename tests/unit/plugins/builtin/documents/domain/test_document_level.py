"""Tests for DocumentLevel."""

from familyos_cli.plugins.builtin.documents.domain.document_level import (
    DocumentLevel,
)


def test_document_level_values() -> None:
    """Document levels expose expected values."""

    assert DocumentLevel.BASIC.value == "basic"
    assert DocumentLevel.STANDARD.value == "standard"
    assert DocumentLevel.SENSITIVE.value == "sensitive"
    assert DocumentLevel.CRITICAL.value == "critical"