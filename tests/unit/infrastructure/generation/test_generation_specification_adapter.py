from __future__ import annotations

from familyos_cli.application.generation.generation_artifact import (
    GenerationArtifact,
)
from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.infrastructure.generation.generation_specification_adapter import (
    GenerationSpecificationAdapter,
)


def test_generation_specification_adapter_creates_project_specification() -> None:
    specification = GenerationSpecification(
        directories=[
            "docs",
            "src",
        ],
        artifacts=[
            GenerationArtifact(
                template="entity.py.jinja",
                destination="models/person.py",
            ),
        ],
    )

    adapter = GenerationSpecificationAdapter()

    result = adapter.adapt(
        specification,
    )

    assert result.directories == [
        "docs",
        "src",
    ]

    assert len(result.files) == 1

    assert result.files[0].path == "models/person.py"

    assert result.files[0].template == "entity.py.jinja"


def test_generation_specification_adapter_handles_empty_specification() -> None:
    specification = GenerationSpecification()

    adapter = GenerationSpecificationAdapter()

    result = adapter.adapt(
        specification,
    )

    assert result.directories == []

    assert result.files == []
