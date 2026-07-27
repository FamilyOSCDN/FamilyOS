from __future__ import annotations

from familyos_cli.domain.models.domain_specification import DomainSpecification
from familyos_cli.shared.exceptions.specification_already_exists_error import (
    SpecificationAlreadyExistsError,
)


class DomainSpecificationRegistry:
    """Registry for domain specifications."""

    def __init__(self) -> None:
        self._specifications: dict[str, DomainSpecification] = {}

    def register(self, specification: DomainSpecification) -> None:
        """Register a domain specification."""

        if specification.name in self._specifications:
            raise SpecificationAlreadyExistsError(
                f"Specification '{specification.name}' already exists."
            )

        self._specifications[specification.name] = specification

    def get(self, name: str) -> DomainSpecification:
        """Retrieve a domain specification."""

        return self._specifications[name]

    def contains(self, name: str) -> bool:
        """Check whether a specification exists."""

        return name in self._specifications

    def all(self) -> list[DomainSpecification]:
        """Return all registered specifications."""

        return list(self._specifications.values())