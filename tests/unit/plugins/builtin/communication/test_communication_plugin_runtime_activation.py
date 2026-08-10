from familyos_cli.plugins.builtin.communication.plugin import (
    CommunicationPlugin,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


def test_communication_plugin_can_be_activated_by_runtime() -> None:
    runtime = PluginRuntime()

    plugin = CommunicationPlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.communication",
    )

    assert plugin in runtime.plugins().all()


def test_communication_plugin_reaches_active_state() -> None:
    runtime = PluginRuntime()

    plugin = CommunicationPlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.communication",
    )

    assert runtime.state(
        plugin,
    ) == RuntimeState.ACTIVE
