"""Tests for SpecificationMerger."""

from familyos_cli.domain.models.project_file import ProjectFile
from familyos_cli.domain.models.project_specification import (
    ProjectSpecification,
)
from familyos_cli.infrastructure.specifications.specification_merger import (
    SpecificationMerger,
)


def test_should_merge_multiple_specifications() -> None:
    """Multiple specifications should be merged."""

    first = ProjectSpecification(
        directories=[
            "docs",
            "src",
        ],
        files=[
            ProjectFile(
                path="README.md",
                template="README.md.j2",
            ),
        ],
    )

    second = ProjectSpecification(
        directories=[
            "tests",
            "scripts",
        ],
        files=[
            ProjectFile(
                path="pyproject.toml",
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

    assert len(specification.files) == 2

    assert specification.files[0].path == "README.md"
    assert specification.files[1].path == "pyproject.toml"