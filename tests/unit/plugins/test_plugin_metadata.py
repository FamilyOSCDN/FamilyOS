from familyos_cli.plugins.plugin_metadata import PluginMetadata


def test_plugin_metadata_defaults() -> None:
    metadata = PluginMetadata(
        name="demo",
        version="1.0.0",
    )

    assert metadata.name == "demo"
    assert metadata.version == "1.0.0"
    assert metadata.author == ""
    assert metadata.description == ""
    assert metadata.homepage == ""
    assert metadata.license == ""
    assert metadata.api_version == "1.0"
