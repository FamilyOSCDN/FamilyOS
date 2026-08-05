from pathlib import Path
from typing import cast

from familyos_cli.plugins.builtin.finance.plugin import (
    FinancePlugin,
)
from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_loader import PluginLoader


def finance_plugin_path() -> Path:
    """Return finance plugin directory."""

    return (
        Path(__file__).parents[5]
        / "src"
        / "familyos_cli"
        / "plugins"
        / "builtin"
        / "finance"
    )


def find_finance_descriptor(
    descriptors: list[PluginDescriptor],
) -> PluginDescriptor:
    """Return finance plugin descriptor."""

    return next(
        descriptor
        for descriptor in descriptors
        if descriptor.id == "familyos.finance"
    )


def test_finance_plugin_descriptor_is_discovered() -> None:
    loader = PluginLoader()

    descriptors = loader.discover(
        finance_plugin_path().parent,
    )

    finance = find_finance_descriptor(
        descriptors,
    )

    assert isinstance(
        finance,
        PluginDescriptor,
    )

    assert finance.name == (
        "FamilyOS Finance Plugin"
    )

    assert finance.module == (
        "familyos_cli.plugins.builtin.finance.plugin"
    )

    assert finance.class_name == (
        "FinancePlugin"
    )


def test_finance_plugin_can_be_loaded() -> None:
    loader = PluginLoader()

    descriptor = find_finance_descriptor(
        loader.discover(
            finance_plugin_path().parent,
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
        FinancePlugin,
    )


def test_loaded_finance_plugin_has_metadata() -> None:
    loader = PluginLoader()

    descriptor = find_finance_descriptor(
        loader.discover(
            finance_plugin_path().parent,
        ),
    )

    plugin = cast(
        FinancePlugin,
        loader.load(
            descriptor,
        ),
    )

    metadata = plugin.get_metadata()

    assert metadata is not None

    assert metadata.name == (
        "FamilyOS Finance Plugin"
    )

    assert metadata.version == (
        "1.0.0"
    )
