"""Tests for registry validation."""

from unittest.mock import Mock

import pytest

from familyos_cli.registry.artifact_registry import (
    ArtifactRegistry,
)
from familyos_cli.registry.models import (
    ArtifactDefinition,
    Registry,
)


def test_exists_should_return_true() -> None:
    """Existing artifact should be found."""

    registry = ArtifactRegistry()

    assert registry.exists("domain")


def test_exists_should_return_false() -> None:
    """Unknown artifact should not exist."""

    registry = ArtifactRegistry()

    assert not registry.exists("unknown")


def test_validate_should_detect_duplicates() -> None:
    """Duplicate ids should raise."""

    registry = ArtifactRegistry()

    registry._registry = Registry(
        version="1.0.0",
        artifacts=[
            ArtifactDefinition(
                id="domain",
                specification="domain.yaml",
            ),
            ArtifactDefinition(
                id="domain",
                specification="other.yaml",
            ),
        ],
    )

    with pytest.raises(ValueError):
        registry.validate()


def test_reload_should_reload_registry() -> None:
    """Reload should reload definitions."""

    registry = ArtifactRegistry()

    loader = Mock()

    loader.load.return_value = registry._registry

    registry._loader = loader

    registry.reload()

    loader.load.assert_called_once()
