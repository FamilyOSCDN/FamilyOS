from __future__ import annotations

from familyos_cli.domain.models.domain_descriptor import (
    DomainDescriptor,
)


class DomainRegistry:
    """Registry of available domains."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self._domains: dict[str, DomainDescriptor] = {}

    def register(
        self,
        descriptor: DomainDescriptor,
    ) -> None:
        """Register a domain."""
        self._domains[descriptor.name] = descriptor

    def get(
        self,
        name: str,
    ) -> DomainDescriptor:
        """Return a registered domain."""
        return self._domains[name]

    def exists(
        self,
        name: str,
    ) -> bool:
        """Return whether a domain exists."""
        return name in self._domains

    def all(
        self,
    ) -> tuple[DomainDescriptor, ...]:
        """Return all registered domains."""
        return tuple(self._domains.values())

    def clear(
        self,
    ) -> None:
        """Clear the registry."""
        self._domains.clear()
