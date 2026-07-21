from familyos_cli.plugins.plugin_context import PluginContext


def test_plugin_context_stores_data() -> None:
    context = PluginContext(
        project_name="demo",
        output_directory="/tmp/demo",
        variables={"author": "Thierry"},
    )

    assert context.project_name == "demo"
    assert context.output_directory == "/tmp/demo"
    assert context.variables["author"] == "Thierry"