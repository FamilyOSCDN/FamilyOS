from familyos_cli.plugins.builtin.security.plugin import (
    SecurityPlugin,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


def test_security_plugin_can_be_activated_by_runtime() -> None:
    runtime = PluginRuntime()

    plugin = SecurityPlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.security",
    )

    assert plugin in runtime.plugins().all()


def test_security_plugin_reaches_active_state() -> None:
    runtime = PluginRuntime()

    plugin = SecurityPlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.security",
    )

    assert runtime.state(
        plugin,
    ) == RuntimeState.ACTIVE
