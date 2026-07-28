"""Tests for SpecificationLoader."""

from pathlib import Path

from familyos_cli.infrastructure.specifications.specification_loader import (
    SpecificationLoader,
)


def test_should_merge_multiple_specifications(
    tmp_path: Path,
) -> None:
    """Multiple specifications should be merged."""

    first = tmp_path / "first.yaml"
    second = tmp_path / "second.yaml"

    first.write_text(
        """
version: 1

project:
  directories:
    - docs

  files:
    - README.md
""",
        encoding="utf-8",
    )

    second.write_text(
        """
project:
  directories:
    - src

  files:
    - pyproject.toml
""",
        encoding="utf-8",
    )

    loader = SpecificationLoader()

    specification = loader.load_all(
        [
            first,
            second,
        ],
    )

    assert specification.directories == [
        "docs",
        "src",
    ]

    assert [
        artifact.destination
        for artifact in specification.artifacts
    ] == [
        "README.md",
        "pyproject.toml",
    ]
