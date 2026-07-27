from pathlib import Path

from familyos_cli.application.generation.domain_generation_adapter import (
    DomainGenerationAdapter,
)
from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
)
from familyos_cli.domain.generation.artifact_generation_mapper import (
    ArtifactGenerationMapper,
)
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)


def test_domain_generation_pipeline_creates_plan(
) -> None:
    pipeline = DomainGenerationPipeline(
        planner=DomainGenerationPlanner(),
        mapper=ArtifactGenerationMapper(),
        adapter=DomainGenerationAdapter(),
        engine=GenerationEngine(),
    )

    specification = DomainSpecification(
    name="Person",
    entities=[],
    aggregates=[],
    repositories=[],
    services=[],
    )

    plan = pipeline.generate(
        specification=specification,
        destination=Path("generated"),
    )

    assert plan.domain_name == "Person"