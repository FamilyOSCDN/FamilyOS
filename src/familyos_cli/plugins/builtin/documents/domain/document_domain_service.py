"""Document domain service."""

from __future__ import annotations

from familyos_cli.plugins.builtin.documents.domain.document_context import (
    DocumentContext,
)
from familyos_cli.plugins.builtin.documents.domain.document_decision import (
    DocumentDecision,
)
from familyos_cli.plugins.builtin.documents.domain.document_level import (
    DocumentLevel,
)


class DocumentDomainService:
    """Domain service for document decisions."""

    def evaluate(
        self,
        context: DocumentContext,
    ) -> DocumentDecision:
        """Evaluate document context."""

        if (
            context.required_level
            == DocumentLevel.CRITICAL
        ):
            return DocumentDecision.REVIEW

        return DocumentDecision.ALLOW