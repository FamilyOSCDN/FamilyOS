from familyos_cli.plugins.builtin.education.plugin import (
    EducationPlugin,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


def test_education_plugin_can_be_activated() -> None:
    runtime = PluginRuntime()

    plugin = EducationPlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.education",
    )

    assert runtime.state(
        plugin,
    ) == RuntimeState.ACTIVE


def test_education_plugin_is_registered_after_activation() -> None:
    runtime = PluginRuntime()

    plugin = EducationPlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.education",
    )

    plugins = runtime.plugins()

    assert plugin in plugins.all()
