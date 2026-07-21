"""Tests for the specification registry."""

from pathlib import Path
from unittest.mock import Mock, patch

from familyos_cli.specifications.specification_registry import (
    SpecificationRegistry,
)


@patch(
    "familyos_cli.specifications.specification_registry.SpecificationLoader",
)
@patch(
    "familyos_cli.specifications.specification_registry.ArtifactRegistry",
)
def test_get_should_load_specification(
    mock_artifact_registry_class,
    mock_loader_class,
) -> None:
    """Getting a specification should load the correct YAML."""

    artifact_registry = Mock()
    loader = Mock()

    mock_artifact_registry_class.return_value = artifact_registry
    mock_loader_class.return_value = loader

    artifact = Mock()
    artifact.specification = "domain.yaml"

    artifact_registry.get.return_value = artifact

    specification = Mock()
    loader.load.return_value = specification

    registry = SpecificationRegistry()

    result = registry.get("domain")

    artifact_registry.get.assert_called_once_with(
        "domain",
    )

    loader.load.assert_called_once_with(
        Path("specifications") / "domain.yaml",
    )

    assert result is specification