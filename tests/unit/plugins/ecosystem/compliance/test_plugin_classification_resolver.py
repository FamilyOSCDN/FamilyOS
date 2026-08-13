"""Tests for plugin classification resolution."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.plugin_classification import (
    PluginClassification,
)
from familyos_cli.plugins.ecosystem.compliance.plugin_classification_resolver import (
    PluginClassificationResolver,
)
from familyos_cli.plugins.models import PluginDescriptor


def _descriptor(path: Path) -> PluginDescriptor:
    return PluginDescriptor(
        id="familyos.test",
        name="Test",
        version="1.0.0",
        module="tests.fixtures.test.plugin",
        class_name="TestPlugin",
        path=path,
    )


def test_classifies_official_when_discovered_under_root(
    tmp_path: Path,
) -> None:
    """A plugin discovered under the official root is classified OFFICIAL."""

    root = tmp_path / "builtin"
    plugin_path = root / "test"
    plugin_path.mkdir(parents=True)

    classification = PluginClassificationResolver.classify(
        _descriptor(plugin_path),
        root,
    )

    assert classification is PluginClassification.OFFICIAL


def test_classifies_third_party_when_outside_root(
    tmp_path: Path,
) -> None:
    """A plugin discovered outside the official root is THIRD_PARTY."""

    root = tmp_path / "builtin"
    root.mkdir()
    outside_path = tmp_path / "elsewhere" / "test"
    outside_path.mkdir(parents=True)

    classification = PluginClassificationResolver.classify(
        _descriptor(outside_path),
        root,
    )

    assert classification is PluginClassification.THIRD_PARTY
