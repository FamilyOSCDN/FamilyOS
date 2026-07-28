"""Generation strategy registry."""

from __future__ import annotations

from familyos_cli.application.generation.strategies.generation_strategy import (
    GenerationStrategy,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)


class GenerationStrategyRegistry:
    """Registry of generation strategies."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._strategies: list[GenerationStrategy] = []

    def register(
        self,
        strategy: GenerationStrategy,
    ) -> None:
        """Register a generation strategy."""

        if strategy in self._strategies:
            raise ValueError(
                f"Strategy '{strategy.name}' already registered.",
            )

        self._strategies.append(
            strategy,
        )

    def resolve(
        self,
        request: GenerationRequest,
    ) -> GenerationStrategy:
        """Resolve a strategy for a request."""

        for strategy in self._strategies:
            if strategy.supports(
                request,
            ):
                return strategy

        raise ValueError(
            f"No strategy found for recipe '{request.recipe_name}'.",
        )

    def list(
        self,
    ) -> tuple[GenerationStrategy, ...]:
        """Return registered strategies."""

        return tuple(
            self._strategies,
        )
