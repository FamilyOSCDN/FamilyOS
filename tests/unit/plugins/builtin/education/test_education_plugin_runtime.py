from pathlib import Path

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
        / "familyos.education"
    )


def test_education_plugin_descriptor_is_discovered() -> None:
    loader = PluginLoader()

    descriptors = loader.discover(
        education_plugin_path().parent,
    )

    descriptor = next(
        descriptor
        for descriptor in descriptors
        if descriptor.id == "familyos.education"
    )

    assert descriptor.id == "familyos.education"

    assert descriptor.name == (
        "FamilyOS Education Plugin"
    )

    assert descriptor.version == "1.0.0"

    assert descriptor.module == (
        "familyos_cli.plugins.builtin.education.plugin"
    )

    assert descriptor.class_name == (
        "EducationPlugin"
    )

    assert descriptor.enabled is True
