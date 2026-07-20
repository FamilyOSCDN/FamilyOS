"""Validation exception."""

from familyos_cli.shared.exceptions.familyos_error import (
    FamilyOSError,
)


class ValidationError(FamilyOSError):
    """Raised when validation fails."""