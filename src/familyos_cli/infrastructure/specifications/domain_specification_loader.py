from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class DomainSpecificationLoader:
    """Contract for domain specification loaders."""

    def load(
        self,
        path: Path,
    ) -> DomainSpecification:
        """Load a domain specification."""

        raise NotImplementedError
