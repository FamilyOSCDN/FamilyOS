"""Project already exists exception."""

from familyos_cli.shared.exceptions.familyos_error import (
    FamilyOSError,
)


class ProjectAlreadyExistsError(FamilyOSError):
    """Raised when the destination project already exists."""
