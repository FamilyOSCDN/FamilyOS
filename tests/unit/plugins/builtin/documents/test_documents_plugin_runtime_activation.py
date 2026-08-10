from familyos_cli.plugins.builtin.documents.plugin import (
    DocumentsPlugin,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


def test_documents_plugin_can_be_activated_by_runtime() -> None:
    runtime = PluginRuntime()

    plugin = DocumentsPlugin()

    runtime.activate(
        plugin,
    )

    assert plugin in runtime.plugins().all()


def test_documents_plugin_reaches_active_state() -> None:
    runtime = PluginRuntime()

    plugin = DocumentsPlugin()

    runtime.activate(
        plugin,
    )

    assert runtime.state(
        plugin,
    ) == RuntimeState.ACTIVE