"""Tests for GenerationResult."""

from pathlib import Path

from familyos_cli.application.generation.generation_result import (
    GenerationResult,
)


def test_generation_result_should_store_generation_information() -> None:
    """GenerationResult should expose generation information."""

    result = GenerationResult(
        success=True,
        generated_files=(
            Path("README.md"),
            Path("pyproject.toml"),
        ),
        warnings=(),
        duration=0.42,
    )

    assert result.success
    assert len(result.generated_files) == 2
    assert result.duration == 0.42
    assert result.warnings == ()