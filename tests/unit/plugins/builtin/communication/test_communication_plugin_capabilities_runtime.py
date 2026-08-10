from familyos_cli.plugins.builtin.communication.plugin import (
    CommunicationPlugin,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


def test_communication_plugin_registers_capabilities_in_runtime() -> None:
    runtime = PluginRuntime()

    runtime.activate(
        CommunicationPlugin(),
    )

    capabilities = (
        runtime.capabilities()
        .list()
    )

    assert len(
        capabilities,
    ) == 2


def test_communication_plugin_runtime_contains_expected_capabilities() -> None:
    runtime = PluginRuntime()

    runtime.activate(
        CommunicationPlugin(),
    )

    identifiers = {
        str(capability.id)
        for capability in (
            runtime.capabilities()
            .list()
        )
    }

    assert identifiers == {
        "familyos.communication.messaging",
        "familyos.communication.archive",
    }
