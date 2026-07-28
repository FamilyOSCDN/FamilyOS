from __future__ import annotations

from familyos_cli.application.specifications.specification_service import (
    SpecificationService,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class GetDomainSpecificationUseCase:
    """Retrieves a domain specification."""

    def __init__(
        self,
        specification_service: SpecificationService,
    ) -> None:
        self._specification_service = specification_service

    def execute(
        self,
        name: str,
    ) -> DomainSpecification | None:
        """Return a specification by name."""

        return self._specification_service.get(name)
