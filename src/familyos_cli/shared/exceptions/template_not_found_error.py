"""Template not found exception."""

from familyos_cli.shared.exceptions.familyos_error import (
    FamilyOSError,
)


class TemplateNotFoundError(FamilyOSError):
    """Raised when a template cannot be found."""