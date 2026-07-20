"""Specification related exceptions."""

from familyos_cli.shared.exceptions.familyos_error import (
    FamilyOSError,
)


class SpecificationError(FamilyOSError):
    """Base class for specification errors."""