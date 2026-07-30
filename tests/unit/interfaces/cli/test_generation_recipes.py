"""Tests for the generation recipes command."""

from __future__ import annotations

import familyos_cli.interfaces.cli.commands.generation_recipes as generation_recipes_module
from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class FakeGenerationRecipe:
    """Fake generation recipe used by CLI tests."""

    def __init__(
        self,
        name: str,
    ) -> None:
        """Initialize the fake recipe."""

        self._name = name

    @property
    def name(
        self,
    ) -> str:
        """Return the recipe name."""

        return self._name

    def build_artifacts(
        self,
        specification: DomainSpecification,
    ) -> list[ArtifactDefinition]:
        """Return no generated artifacts."""

        return []


class FakeRecipeCatalogService:
    """Fake recipe catalog service used by CLI tests."""

    def list_recipes(
        self,
    ) -> tuple[FakeGenerationRecipe, ...]:
        """Return fake generation recipes."""

        return (
            FakeGenerationRecipe(
                "domain_documentation",
            ),
            FakeGenerationRecipe(
                "entity_documentation",
            ),
        )


class FakeCommandContext:
    """Fake command context used by CLI tests."""

    def __init__(
        self,
    ) -> None:
        """Initialize the fake command context."""

        self.recipe_catalog = (
            FakeRecipeCatalogService()
        )


def test_generation_recipes_displays_available_recipes(
    monkeypatch,
) -> None:
    """Display all available recipe names."""

    messages: list[str] = []

    monkeypatch.setattr(
        generation_recipes_module,
        "CommandContext",
        FakeCommandContext,
    )

    monkeypatch.setattr(
        generation_recipes_module.Output,
        "info",
        messages.append,
    )

    generation_recipes_module.generation_recipes()

    assert messages == [
        "Available generation recipes:",
        "  - domain_documentation",
        "  - entity_documentation",
    ]
