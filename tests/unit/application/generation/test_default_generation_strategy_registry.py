from familyos_cli.application.generation.default_generation_strategy_registry import (
    DefaultGenerationStrategyRegistry,
)


def test_default_generation_strategy_registry_creates_default_strategies() -> None:
    registry = DefaultGenerationStrategyRegistry.create()

    strategies = registry.list()

    assert len(strategies) == 2

    strategy_names = {
        strategy.name
        for strategy in strategies
    }

    assert strategy_names == {
        "domain_documentation",
        "domain_implementation",
    }
