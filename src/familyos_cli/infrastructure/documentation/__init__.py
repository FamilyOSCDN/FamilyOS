"""Documentation Framework infrastructure primitives."""

from familyos_cli.infrastructure.documentation.documentation_validator import (
    DocumentationValidationResult as DocumentationValidationResult,
)
from familyos_cli.infrastructure.documentation.documentation_validator import (
    DocumentationValidator as DocumentationValidator,
)
from familyos_cli.infrastructure.documentation.documentation_validator import (
    DocumentationViolation as DocumentationViolation,
)

__all__ = [
    "DocumentationValidationResult",
    "DocumentationValidator",
    "DocumentationViolation",
]
