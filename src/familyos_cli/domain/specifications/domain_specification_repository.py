"""Repository abstraction for domain specifications."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class DomainSpecificationRepository(ABC):
    """Repository for domain specifications."""

    @abstractmethod
    def load(
        self,
        name: str,
    ) -> DomainSpecification:
        """Load a domain specification."""

    @abstractmethod
    def exists(
        self,
        name: str,
    ) -> bool:
        """Return whether the specification exists."""
