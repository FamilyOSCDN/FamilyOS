from __future__ import annotations

from pathlib import Path

from familyos_cli.application.specifications.specification_service import (
    SpecificationService,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.infrastructure.specifications.domain_specification_loader import (
    DomainSpecificationLoader,
)


class DomainSpecificationLoaderService:
    """Loads and registers domain specifications."""

    def __init__(
        self,
        loader: DomainSpecificationLoader,
        service: SpecificationService,
    ) -> None:
        self._loader = loader
        self._service = service

    def load(
        self,
        path: Path,
    ) -> DomainSpecification:
        specification = self._loader.load(path)

        self._service.register(specification)

        return specification