"""Tests for the artifact registry."""

import pytest

from familyos_cli.registry.artifact_registry import (
    ArtifactRegistry,
)


def test_should_list_artifacts() -> None:
    """Registry should list artifacts."""

    registry = ArtifactRegistry()

    artifacts = registry.list()

    assert len(artifacts) == 5


def test_should_return_artifact() -> None:
    """Registry should return one artifact."""

    registry = ArtifactRegistry()

    artifact = registry.get("domain")

    assert artifact.id == "domain"
    assert artifact.specification == "domain.yaml"


def test_should_raise_for_unknown_artifact() -> None:
    """Unknown artifact should raise."""

    registry = ArtifactRegistry()

    with pytest.raises(ValueError):
        registry.get("unknown")