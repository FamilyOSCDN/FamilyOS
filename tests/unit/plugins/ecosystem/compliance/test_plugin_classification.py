"""Tests for plugin classification."""

from familyos_cli.plugins.ecosystem.compliance.plugin_classification import (
    PluginClassification,
)


def test_plugin_classification_values() -> None:
    """Plugin classifications expose stable serialized values."""

    assert PluginClassification.OFFICIAL.value == "official"
    assert PluginClassification.THIRD_PARTY.value == "third_party"
    assert PluginClassification.DEVELOPMENT.value == "development"
