from __future__ import annotations

from familyos_cli.domain.models.domain_descriptor import (
    DomainDescriptor,
)
from familyos_cli.domain.registry.domain_registry import (
    DomainRegistry,
)


def test_should_register_domain() -> None:
    registry = DomainRegistry()

    descriptor = DomainDescriptor(
        name="Person",
        title="Person Domain",
        description="Manages person identities and profiles.",
    )

    registry.register(descriptor)

    assert registry.exists("Person")
    assert registry.get("Person") is descriptor


def test_should_return_all_domains() -> None:
    registry = DomainRegistry()

    registry.register(
        DomainDescriptor(
            name="Person",
            title="Person Domain",
            description="Manages person identities and profiles.",
        )
    )

    registry.register(
        DomainDescriptor(
            name="Family",
            title="Family Domain",
            description="Manages family structures and relationships.",
        )
    )

    assert len(registry.all()) == 2


def test_should_clear_registry() -> None:
    registry = DomainRegistry()

    registry.register(
        DomainDescriptor(
            name="Person",
            title="Person Domain",
            description="Manages person identities and profiles.",
        )
    )

    registry.clear()

    assert registry.all() == ()