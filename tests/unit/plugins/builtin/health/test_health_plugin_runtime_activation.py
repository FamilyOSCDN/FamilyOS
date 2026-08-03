from familyos_cli.plugins.builtin.health.plugin import (
    HealthPlugin,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


def test_health_plugin_can_be_activated_by_runtime() -> None:
    runtime = PluginRuntime()

    plugin = HealthPlugin()

    runtime.activate(
        plugin,
    )

    assert plugin in runtime.plugins().all()


def test_health_plugin_reaches_active_state() -> None:
    runtime = PluginRuntime()

    plugin = HealthPlugin()

    runtime.activate(
        plugin,
    )

    assert runtime.state(
        plugin,
    ) == RuntimeState.ACTIVE
