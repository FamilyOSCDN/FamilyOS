from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.generation_recipe import (
    GenerationRecipe,
)


class FakeRecipe:
    """Fake generation recipe."""

    @property
    def name(self) -> str:
        return "test_recipe"

    def build_artifacts(
        self,
    ) -> list[ArtifactDefinition]:
        return [
            ArtifactDefinition(
                kind=ArtifactKind.ENTITY,
                name="Person",
                target_path="models/person.py",
                template="entity.py.jinja",
            )
        ]


def test_generation_recipe_contract() -> None:
    recipe: GenerationRecipe = FakeRecipe()

    assert recipe.name == "test_recipe"

    artifacts = recipe.build_artifacts()

    assert len(artifacts) == 1

    assert artifacts[0].name == "Person"
