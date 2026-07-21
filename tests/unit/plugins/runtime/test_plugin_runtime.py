from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_metadata import PluginMetadata
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime


class DummyPlugin(Plugin):
    metadata = PluginMetadata(
        name="dummy",
        version="1.0.0",
    )


def test_register_plugin() -> None:
    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.register(plugin)

    assert runtime.plugins().list() == [plugin]