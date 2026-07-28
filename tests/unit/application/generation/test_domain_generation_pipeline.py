from pathlib import Path

from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
)
from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.application.generation.mappers.generation_specification_mapper import (
    GenerationSpecificationMapper,
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


def test_domain_generation_pipeline_creates_generation_specification() -> None:
    pipeline = DomainGenerationPipeline(
        planner=DomainGenerationPlanner(),
        specification_mapper=GenerationSpecificationMapper(),
        engine=GenerationEngine(),
    )

    specification = DomainSpecification(
        name="Person",
        entities=[],
        aggregates=[],
        repositories=[],
        services=[],
    )

    result = pipeline.generate(
        specification=specification,
        destination=Path("generated"),
    )

    assert isinstance(
        result,
        GenerationSpecification,
    )

    assert result.artifacts == []
