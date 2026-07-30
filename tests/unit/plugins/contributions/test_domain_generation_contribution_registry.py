import pytest

from familyos_cli.plugins.contributions.domain_generation_contribution import (
    DomainGenerationContribution,
)
from familyos_cli.plugins.contributions.domain_generation_contribution_registry import (
    DomainGenerationContributionRegistry,
)


def test_register_domain_generation_contribution() -> None:
    registry = DomainGenerationContributionRegistry()

    contribution = DomainGenerationContribution(
        domain="Health",
        description="Health domain generation.",
        artifacts=(
            "health_documentation",
        ),
    )

    registry.register(
        contribution,
    )

    assert registry.get(
        "Health",
    ) == contribution


def test_list_domain_generation_contributions() -> None:
    registry = DomainGenerationContributionRegistry()

    contribution = DomainGenerationContribution(
        domain="Finance",
        description="Finance domain generation.",
        artifacts=(
            "finance_documentation",
        ),
    )

    registry.register(
        contribution,
    )

    assert registry.list() == (
        contribution,
    )


def test_register_duplicate_domain_generation_contribution() -> None:
    registry = DomainGenerationContributionRegistry()

    contribution = DomainGenerationContribution(
        domain="Education",
        description="Education domain generation.",
        artifacts=(
            "education_documentation",
        ),
    )

    registry.register(
        contribution,
    )

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        registry.register(
            contribution,
        )
