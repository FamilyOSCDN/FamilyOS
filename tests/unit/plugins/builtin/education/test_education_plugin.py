from familyos_cli.plugins.builtin.education.plugin import (
    EducationPlugin,
)
from familyos_cli.plugins.models import (
    PluginMetadata,
)


def test_education_plugin_metadata() -> None:
    plugin = EducationPlugin()

    metadata = plugin.get_metadata()

    assert isinstance(
        metadata,
        PluginMetadata,
    )

    assert metadata.name == (
        "FamilyOS Education Plugin"
    )

    assert metadata.version == "1.0.0"

    assert metadata.author == (
        "FamilyOS Team"
    )


def test_education_plugin_description() -> None:
    plugin = EducationPlugin()

    metadata = plugin.get_metadata()

    assert metadata is not None

    assert (
        "educational capabilities"
        in metadata.description
    )
