"""Document validator."""

from __future__ import annotations

from familyos_cli.plugins.builtin.documents.domain.document_context import (
    DocumentContext,
)
from familyos_cli.plugins.builtin.documents.domain.document_level import (
    DocumentLevel,
)
from familyos_cli.plugins.builtin.documents.validation.document_validation_result import (
    DocumentValidationResult,
)


class DocumentValidator:
    """Validate document contexts."""

    def validate(
        self,
        context: DocumentContext,
    ) -> DocumentValidationResult:
        """Validate document context."""

        if (
            context.required_level
            == DocumentLevel.CRITICAL
        ):
            return DocumentValidationResult(
                valid=False,
                message="Critical document review required.",
            )

        return DocumentValidationResult(
            valid=True,
            message="Document context validated.",
        )