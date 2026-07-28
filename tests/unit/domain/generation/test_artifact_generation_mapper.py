from __future__ import annotations

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.artifact_generation_mapper import (
    ArtifactGenerationMapper,
)
from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)


def test_entity_artifact_gets_entity_template() -> None:
    artifact = ArtifactDefinition(
        kind=ArtifactKind.ENTITY,
        name="Person",
        target_path="domains/person/entities/person.py",
        template="",
    )

    mapper = ArtifactGenerationMapper()

    mapped = mapper.map(artifact)

    assert mapped.kind == ArtifactKind.ENTITY
    assert mapped.name == "Person"
    assert mapped.target_path == (
        "domains/person/entities/person.py"
    )
    assert mapped.template == "entity.py.jinja"


def test_mapper_preserves_existing_template_for_unmapped_kind() -> None:
    artifact = ArtifactDefinition(
        kind=ArtifactKind.DOCUMENTATION,
        name="Business Rules",
        target_path="docs/business-rules.md",
        template="custom-documentation.md.jinja",
    )

    mapper = ArtifactGenerationMapper()

    mapped = mapper.map(artifact)

    assert mapped.template == "custom-documentation.md.jinja"


def test_mapper_uses_injected_template_policy() -> None:
    class FakeArtifactTemplatePolicy:
        def template_for(
            self,
            kind: ArtifactKind,
            current_template: str = "",
            profile: GenerationProfile = (
                GenerationProfile.PYTHON_IMPLEMENTATION
            ),
        ) -> str:
            return f"custom/{kind.value}.jinja"

    artifact = ArtifactDefinition(
        kind=ArtifactKind.ENTITY,
        name="Person",
        target_path="models/person.py",
        template="",
    )

    mapper = ArtifactGenerationMapper(
        template_policy=FakeArtifactTemplatePolicy(),
    )

    mapped = mapper.map(artifact)

    assert mapped.template == "custom/entity.jinja"


def test_mapper_can_use_documentation_profile() -> None:
    artifact = ArtifactDefinition(
        kind=ArtifactKind.ENTITY,
        name="Person",
        target_path="docs/person",
        template="",
    )

    mapper = ArtifactGenerationMapper(
        profile=GenerationProfile.DOMAIN_DOCUMENTATION,
    )

    mapped = mapper.map(artifact)

    assert mapped.template == "entity/README.md.j2"
