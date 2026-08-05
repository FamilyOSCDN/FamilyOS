from familyos_cli.plugins.builtin.finance.plugin import (
    FinancePlugin,
)


def test_finance_plugin_has_metadata() -> None:
    plugin = FinancePlugin()

    metadata = plugin.get_metadata()

    assert metadata is not None

    assert metadata.name == (
        "FamilyOS Finance Plugin"
    )

    assert metadata.version == (
        "1.0.0"
    )
