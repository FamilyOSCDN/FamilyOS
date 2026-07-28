from __future__ import annotations

from familyos_cli.domain.models.domain_specification import DomainSpecification
from familyos_cli.domain.specifications.domain_specification_registry import (
    DomainSpecificationRegistry,
)


class SpecificationService:
    """Application service managing domain specifications."""

    def __init__(
        self,
        registry: DomainSpecificationRegistry,
    ) -> None:
        self._registry = registry

    def register(
        self,
        specification: DomainSpecification,
    ) -> None:
        """Register a domain specification."""
        self._registry.register(specification)

    def get(
        self,
        name: str,
    ) -> DomainSpecification | None:
        """Retrieve a specification by name."""
        return self._registry.get(name)

    def contains(
        self,
        name: str,
    ) -> bool:
        """Check if a specification exists."""
        return self._registry.contains(name)
