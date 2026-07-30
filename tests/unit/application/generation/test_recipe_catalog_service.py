"""Tests for the generation recipe catalog service."""

from __future__ import annotations

from familyos_cli.application.generation.recipe_catalog_service import (
    RecipeCatalogService,
)
from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class FakeGenerationRecipe:
    """Fake generation recipe used by catalog tests."""

    @property
    def name(
        self,
    ) -> str:
        """Return the fake recipe name."""

        return "fake_recipe"

    def build_artifacts(
        self,
        specification: DomainSpecification,
    ) -> list[ArtifactDefinition]:
        """Return no generated artifacts."""

        return []


def test_recipe_catalog_service_returns_registered_recipes() -> None:
    """Return recipes contained in the injected registry."""

    registry = GenerationRecipeRegistry()
    recipe = FakeGenerationRecipe()

    registry.register(
        recipe,
    )

    service = RecipeCatalogService(
        registry=registry,
    )

    recipes = service.list_recipes()

    assert recipes == (
        recipe,
    )


def test_recipe_catalog_service_returns_empty_registry() -> None:
    """Return an empty tuple when no recipes are registered."""

    service = RecipeCatalogService(
        registry=GenerationRecipeRegistry(),
    )

    recipes = service.list_recipes()

    assert recipes == ()
