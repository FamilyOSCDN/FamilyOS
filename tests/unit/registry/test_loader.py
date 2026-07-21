"""Tests for the registry loader."""

from familyos_cli.registry.loader import RegistryLoader


def test_should_load_registry() -> None:
    """Registry should be loaded from YAML."""

    registry = RegistryLoader().load()

    assert registry.version == "1.0.0"

    assert len(registry.artifacts) == 5

    assert registry.artifacts[0].id == "project"

    assert (
        registry.artifacts[0].specification
        == "project.yaml"
    )