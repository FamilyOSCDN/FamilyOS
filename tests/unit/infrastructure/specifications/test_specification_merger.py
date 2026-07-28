"""Tests for SpecificationMerger."""

from familyos_cli.application.generation.generation_artifact import (
    GenerationArtifact,
)
from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.infrastructure.specifications.specification_merger import (
    SpecificationMerger,
)


def test_should_merge_multiple_specifications() -> None:
    """Multiple specifications should be merged."""

    first = GenerationSpecification(
        directories=[
            "docs",
            "src",
        ],
        artifacts=[
            GenerationArtifact(
                destination="README.md",
                template="README.md.j2",
            ),
        ],
    )

    second = GenerationSpecification(
        directories=[
            "tests",
            "scripts",
        ],
        artifacts=[
            GenerationArtifact(
                destination="pyproject.toml",
                template="pyproject.toml.j2",
            ),
        ],
    )

    merger = SpecificationMerger()

    specification = merger.merge(
        [
            first,
            second,
        ],
    )

    assert specification.directories == [
        "docs",
        "src",
        "tests",
        "scripts",
    ]

    assert len(specification.artifacts) == 2

    assert specification.artifacts[0].destination == (
        "README.md"
    )

    assert specification.artifacts[1].destination == (
        "pyproject.toml"
    )
