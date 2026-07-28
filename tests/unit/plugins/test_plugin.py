from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_context import PluginContext


class DummyPlugin(Plugin):
    pass


def test_plugin_has_default_hooks() -> None:
    plugin = DummyPlugin()

    context = PluginContext(
        project_name="demo",
        output_directory="/tmp/demo",
    )

    plugin.before_generate(context)
    plugin.after_generate(context)
