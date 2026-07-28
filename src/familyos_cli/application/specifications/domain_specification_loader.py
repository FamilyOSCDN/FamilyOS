"""Domain specification loader port."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class DomainSpecificationLoader(Protocol):
    """Loads domain specifications."""

    def load(
        self,
        path: Path,
    ) -> DomainSpecification:
        """Load a domain specification."""
        ...
