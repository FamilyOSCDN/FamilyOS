"""Domain specification loader service."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.specifications.domain_specification_loader import (
    DomainSpecificationLoader,
)
from familyos_cli.application.specifications.specification_service import (
    SpecificationService,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class DomainSpecificationLoaderService:
    """Load and register domain specifications."""

    def __init__(
        self,
        loader: DomainSpecificationLoader,
        service: SpecificationService,
    ) -> None:
        """Initialize the loader service."""

        self._loader = loader
        self._service = service

    def load(
        self,
        path: Path,
    ) -> DomainSpecification:
        """Load and register a domain specification."""

        specification = self._loader.load(
            path,
        )

        self._service.register(
            specification,
        )

        return specification
