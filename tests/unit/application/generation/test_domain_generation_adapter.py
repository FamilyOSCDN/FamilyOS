from familyos_cli.application.generation.domain_generation_adapter import (
    DomainGenerationAdapter,
)
from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)


def test_domain_generation_adapter_creates_project_specification() -> None:
    plan = DomainGenerationPlan(
        domain_name="Person",
        artifacts=[
            ArtifactDefinition(
                artifact_type="entity",
                name="Person",
                target_path="person/entities/person.py",
                template="entity.py.jinja",
            )
        ],
    )

    adapter = DomainGenerationAdapter()

    specification = adapter.adapt(plan)

    assert len(specification.files) == 1
    assert specification.files[0].path == (
        "person/entities/person.py"
    )
    assert specification.files[0].template == (
        "entity.py.jinja"
    )