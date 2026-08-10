from familyos_cli.plugins.builtin.finance.plugin import (
    FinancePlugin,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


def test_finance_plugin_registers_capabilities_in_runtime() -> None:
    runtime = PluginRuntime()

    runtime.activate(
        FinancePlugin(),
        plugin_id="familyos.finance",
    )

    capabilities = (
        runtime.capabilities()
        .list()
    )

    assert len(
        capabilities,
    ) == 5


def test_finance_plugin_runtime_contains_expected_capabilities() -> None:
    runtime = PluginRuntime()

    runtime.activate(
        FinancePlugin(),
        plugin_id="familyos.finance",
    )

    identifiers = {
        str(capability.id)
        for capability in (
            runtime.capabilities()
            .list()
        )
    }

    assert identifiers == {
        "familyos.finance.account",
        "familyos.finance.transaction",
        "familyos.finance.asset",
        "familyos.finance.liability",
        "familyos.finance.budget",
    }
