"""Tests for the artifact generator."""

from pathlib import Path
from unittest.mock import Mock, patch

from familyos_cli.infrastructure.generation.artifact_generator import (
    ArtifactGenerator,
)


@patch(
    "familyos_cli.infrastructure.generation.artifact_generator.ArtifactRegistry",
)
@patch(
    "familyos_cli.infrastructure.generation.artifact_generator.GenerationEngine",
)
@patch(
    "familyos_cli.infrastructure.generation.artifact_generator.SpecificationLoader",
)
def test_generate_should_load_specification_and_generate(
    mock_loader_class,
    mock_engine_class,
    mock_registry_class,
) -> None:
    """Generating an artifact should load its specification."""

    loader = Mock()
    engine = Mock()
    registry = Mock()

    mock_loader_class.return_value = loader
    mock_engine_class.return_value = engine
    mock_registry_class.return_value = registry

    artifact = Mock()
    artifact.specification = "domain.yaml"

    registry.get.return_value = artifact

    specification = Mock()
    loader.load.return_value = specification

    generator = ArtifactGenerator()

    generator.generate(
        artifact_type="domain",
        name="Person",
    )

    registry.get.assert_called_once_with("domain")

    loader.load.assert_called_once_with(
        Path("specifications") / "domain.yaml",
    )

    engine.generate.assert_called_once_with(
        destination=Path("Person"),
        specification=specification,
        context={
            "name": "Person",
        },
    )
