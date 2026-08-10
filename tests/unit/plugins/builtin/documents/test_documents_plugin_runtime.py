from pathlib import Path
from typing import cast

from familyos_cli.plugins.builtin.documents.plugin import (
    DocumentsPlugin,
)
from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_loader import PluginLoader


def documents_plugin_path() -> Path:
    """Return documents plugin directory."""

    return (
        Path(__file__).parents[5]
        / "src"
        / "familyos_cli"
        / "plugins"
        / "builtin"
        / "documents"
    )


def find_documents_descriptor(
    descriptors: list[PluginDescriptor],
) -> PluginDescriptor:
    """Return documents plugin descriptor."""

    return next(
        descriptor
        for descriptor in descriptors
        if descriptor.id == "documents"
    )


def test_documents_plugin_descriptor_is_discovered() -> None:
    loader = PluginLoader()

    descriptors = loader.discover(
        documents_plugin_path().parent,
    )

    documents = find_documents_descriptor(
        descriptors,
    )

    assert isinstance(
        documents,
        PluginDescriptor,
    )

    assert documents.name == (
        "FamilyOS Documents Plugin"
    )

    assert documents.module == (
        "familyos_cli.plugins.builtin.documents.plugin"
    )

    assert documents.class_name == (
        "DocumentsPlugin"
    )


def test_documents_plugin_can_be_loaded() -> None:
    loader = PluginLoader()

    descriptor = find_documents_descriptor(
        loader.discover(
            documents_plugin_path().parent,
        ),
    )

    plugin = cast(
        Plugin,
        loader.load(
            descriptor,
        ),
    )

    assert isinstance(
        plugin,
        DocumentsPlugin,
    )


def test_loaded_documents_plugin_has_metadata() -> None:
    loader = PluginLoader()

    descriptor = find_documents_descriptor(
        loader.discover(
            documents_plugin_path().parent,
        ),
    )

    plugin = cast(
        DocumentsPlugin,
        loader.load(
            descriptor,
        ),
    )

    metadata = plugin.get_metadata()

    assert metadata is not None

    assert metadata.name == (
        "FamilyOS Documents Plugin"
    )

    assert metadata.version == (
        "1.0.0"
    )