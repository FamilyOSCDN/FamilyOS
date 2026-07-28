from __future__ import annotations

from familyos_cli.shared.exceptions.familyos_error import FamilyOSError


class SpecificationAlreadyExistsError(FamilyOSError):
    """Raised when a specification already exists."""
