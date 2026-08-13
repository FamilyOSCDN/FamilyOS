"""Tests for validation context construction."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.plugin_classification import (
    PluginClassification,
)
from familyos_cli.plugins.ecosystem.compliance.validation_context_builder import (
    ValidationContextBuilder,
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


def test_build_parses_valid_manifest(tmp_path: Path) -> None:
    """A valid manifest is parsed into the context."""

    root = tmp_path / "builtin"
    plugin_path = root / "test"
    plugin_path.mkdir(parents=True)
    (plugin_path / "plugin.yaml").write_text(
        "id: familyos.test\nname: Test\nversion: 1.0.0\n",
        encoding="utf-8",
    )

    builder = ValidationContextBuilder(discovery_root=root)
    context = builder.build(_descriptor(plugin_path))

    assert context.manifest == {
        "id": "familyos.test",
        "name": "Test",
        "version": "1.0.0",
    }
    assert context.manifest_error is None
    assert context.classification is PluginClassification.OFFICIAL


def test_build_reports_missing_manifest(tmp_path: Path) -> None:
    """A missing manifest file produces a None manifest and an error."""

    root = tmp_path / "builtin"
    plugin_path = root / "test"
    plugin_path.mkdir(parents=True)

    builder = ValidationContextBuilder(discovery_root=root)
    context = builder.build(_descriptor(plugin_path))

    assert context.manifest is None
    assert context.manifest_error is not None


def test_build_reports_non_mapping_manifest(tmp_path: Path) -> None:
    """A manifest that does not parse as a mapping produces an error."""

    root = tmp_path / "builtin"
    plugin_path = root / "test"
    plugin_path.mkdir(parents=True)
    (plugin_path / "plugin.yaml").write_text("- just\n- a\n- list\n", encoding="utf-8")

    builder = ValidationContextBuilder(discovery_root=root)
    context = builder.build(_descriptor(plugin_path))

    assert context.manifest is None
    assert context.manifest_error is not None
