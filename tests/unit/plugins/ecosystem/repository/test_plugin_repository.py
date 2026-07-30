"""Tests for plugin repository model."""

from familyos_cli.plugins.ecosystem.repository import (
    PluginRepository,
)


def test_plugin_repository_creation() -> None:
    """Plugin repository should be created."""

    repository = PluginRepository(
        name="FamilyOS Official",
        url="https://plugins.familyos.dev",
        repository_type="official",
    )

    assert repository.name == "FamilyOS Official"
    assert repository.repository_type == "official"
    assert repository.identifier() == "familyos-official"
    assert repository.enabled is True
