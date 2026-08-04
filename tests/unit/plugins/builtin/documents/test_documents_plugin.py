from familyos_cli.plugins.builtin.documents.plugin import (
    DocumentsPlugin,
)
from familyos_cli.plugins.models import (
    PluginMetadata,
)


def test_documents_plugin_metadata() -> None:
    plugin = DocumentsPlugin()

    metadata = plugin.get_metadata()

    assert isinstance(
        metadata,
        PluginMetadata,
    )

    assert metadata.name == (
        "FamilyOS Documents Plugin"
    )

    assert metadata.version == "1.0.0"

    assert metadata.author == (
        "FamilyOS Team"
    )


def test_documents_plugin_description() -> None:
    plugin = DocumentsPlugin()

    metadata = plugin.get_metadata()

    assert metadata is not None

    assert (
        "document management"
        in metadata.description
    )

    assert (
        "family digital archive"
        in metadata.description
    )


def test_documents_plugin_has_no_initial_capabilities() -> None:
    plugin = DocumentsPlugin()

    assert plugin.capabilities() == ()


def test_documents_plugin_has_no_initial_contributions() -> None:
    plugin = DocumentsPlugin()

    assert plugin.contributions() == ()
