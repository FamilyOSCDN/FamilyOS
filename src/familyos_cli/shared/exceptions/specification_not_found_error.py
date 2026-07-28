"""Specification not found exception."""

from familyos_cli.shared.exceptions.specification_error import (
    SpecificationError,
)


class SpecificationNotFoundError(SpecificationError):
    """Raised when a specification file cannot be found."""
