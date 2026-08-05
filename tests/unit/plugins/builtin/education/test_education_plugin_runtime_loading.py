from pathlib import Path

from familyos_cli.plugins.plugin import (
    Plugin,
)
from familyos_cli.plugins.plugin_loader import (
    PluginLoader,
)


def education_plugin_path() -> Path:
    return (
        Path(__file__)
        .parents[5]
        / "src"
        / "familyos_cli"
        / "plugins"
        / "builtin"
        / "education"
    )


def test_education_plugin_can_be_loaded() -> None:
    loader = PluginLoader()

    descriptors = loader.discover(
        education_plugin_path().parent,
    )

    descriptor = next(
        descriptor
        for descriptor in descriptors
        if descriptor.id == "education"
    )

    loaded_plugin = loader.load(
        descriptor,
    )

    assert isinstance(
        loaded_plugin,
        Plugin,
    )

    metadata = loaded_plugin.get_metadata()

    assert metadata is not None

    assert metadata.name == (
        "FamilyOS Education Plugin"
    )

    assert metadata.version == "1.0.0"

    assert metadata.author == (
        "FamilyOS Team"
    )
