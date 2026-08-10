"""Document context model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.builtin.documents.domain.document_level import (
    DocumentLevel,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentContext:
    """Context used for document evaluation."""

    domain_name: str

    subject: str

    required_level: DocumentLevel