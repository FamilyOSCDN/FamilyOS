"""Tests for plugin dependency."""

from familyos_cli.plugins.ecosystem.resolution import (
    PluginDependency,
)


def test_dependency_identifier() -> None:
    """Dependency identifier should be generated."""

    dependency = PluginDependency(
        name="notification",
        minimum_version="1.0.0",
    )

    assert dependency.identifier() == "notification>=1.0.0"
