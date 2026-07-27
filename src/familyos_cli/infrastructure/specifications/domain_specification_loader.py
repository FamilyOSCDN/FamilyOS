from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class DomainSpecificationLoader:
    """Loads domain specifications."""

    def load(self, path: Path) -> DomainSpecification:
        raise NotImplementedError