from familyos_cli.plugins.builtin.documents.plugin import (
    DocumentsPlugin,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


def test_documents_plugin_registers_capabilities_in_runtime() -> None:
    runtime = PluginRuntime()

    runtime.activate(
        DocumentsPlugin(),
    )

    capabilities = (
        runtime.capabilities()
        .list()
    )

    assert len(
        capabilities,
    ) == 2


def test_documents_plugin_runtime_contains_expected_capabilities() -> None:
    runtime = PluginRuntime()

    runtime.activate(
        DocumentsPlugin(),
    )

    identifiers = {
        str(capability.id)
        for capability in (
            runtime.capabilities()
            .list()
        )
    }

    assert identifiers == {
        "familyos.documents.document",
        "familyos.documents.archive",
    }