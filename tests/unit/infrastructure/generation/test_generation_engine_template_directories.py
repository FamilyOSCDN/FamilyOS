"""Tests for GenerationEngine template directories."""

from pathlib import Path

from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)


def test_should_accept_multiple_template_directories() -> None:
    """GenerationEngine should expose template directories."""

    engine = GenerationEngine(
        template_directories=(
            Path("templates"),
            Path("plugins/blog/templates"),
        ),
    )

    assert engine.template_directories == (
        Path("templates"),
        Path("plugins/blog/templates"),
    )
