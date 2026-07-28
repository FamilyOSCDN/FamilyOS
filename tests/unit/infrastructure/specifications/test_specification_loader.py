"""Tests for SpecificationLoader."""

from pathlib import Path

from familyos_cli.infrastructure.specifications.specification_loader import (
    SpecificationLoader,
)


def test_load_generation_specification() -> None:
    """Load the default generation specification."""

    loader = SpecificationLoader()

    specification = loader.load(
        Path("specifications/project.yaml"),
    )

    assert specification.directories == [
        "docs",
        "src",
        "tests",
        "scripts",
    ]

    assert len(specification.artifacts) == 1

    assert specification.artifacts[0].destination == (
        "README.md"
    )

    assert specification.artifacts[0].template == (
        "project/README.md.j2"
    )
