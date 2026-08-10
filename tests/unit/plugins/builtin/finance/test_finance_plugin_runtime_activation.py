from familyos_cli.plugins.builtin.finance.plugin import (
    FinancePlugin,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


def test_finance_plugin_can_be_activated_by_runtime() -> None:
    runtime = PluginRuntime()

    plugin = FinancePlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.finance",
    )

    assert plugin in runtime.plugins().all()


def test_finance_plugin_reaches_active_state() -> None:
    runtime = PluginRuntime()

    plugin = FinancePlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.finance",
    )

    assert runtime.state(
        plugin,
    ) == RuntimeState.ACTIVE
