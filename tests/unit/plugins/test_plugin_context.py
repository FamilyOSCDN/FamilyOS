from familyos_cli.plugins.plugin_context import PluginContext


def test_plugin_context_default_variables() -> None:
    """Plugin context should initialize empty variables."""

    context = PluginContext(
        project_name="FamilyOS",
        output_directory="/tmp/output",
    )

    assert context.project_name == "FamilyOS"
    assert context.output_directory == "/tmp/output"
    assert context.variables == {}


def test_plugin_context_custom_variables() -> None:
    """Plugin context should keep provided variables."""

    context = PluginContext(
        project_name="FamilyOS",
        output_directory="/tmp/output",
        variables={
            "environment": "test",
        },
    )

    assert context.variables["environment"] == "test"
