from familyos_cli.plugins.builtin.health.plugin import (
    HealthPlugin,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


def test_health_plugin_capabilities_are_registered_in_runtime() -> None:
    runtime = PluginRuntime()

    plugin = HealthPlugin()

    runtime.activate(
        plugin,
    )

    registry = runtime.capabilities()

    assert registry.contains(
        PluginCapabilityId(
            "familyos.health.profile",
        ),
    )

    assert registry.contains(
        PluginCapabilityId(
            "familyos.health.record",
        ),
    )
