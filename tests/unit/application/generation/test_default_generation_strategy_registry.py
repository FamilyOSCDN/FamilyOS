from familyos_cli.application.generation.default_generation_strategy_registry import (
    DefaultGenerationStrategyRegistry,
)


def test_default_generation_strategy_registry_creates_default_strategies() -> None:
    registry = DefaultGenerationStrategyRegistry.create()

    strategies = registry.list()

    assert len(strategies) == 9

    assert [
        strategy.name
        for strategy in strategies
    ] == [
        "domain_documentation",
        "entity_documentation",
        "aggregate_documentation",
        "domain_context_documentation",
        "repository_documentation",
        "service_documentation",
        "full_domain_documentation",
        "domain_implementation",
        "plugin_recipe",
    ]
