"""Tests for canonical runtime plugin identifiers."""

import pytest

from familyos_cli.plugins.runtime.runtime_plugin_id import (
    RuntimePluginId,
)


@pytest.mark.parametrize(
    "value",
    (
        "familyos.security",
        "familyos.finance",
        "familyos.my_plugin",
        "familyos.plugin123",
        "familyos.example.subsystem",
    ),
)
def test_runtime_plugin_id_accepts_canonical_identifiers(
    value: str,
) -> None:
    """Canonical FamilyOS plugin identifiers should be accepted."""

    plugin_id = RuntimePluginId(
        value,
    )

    assert plugin_id.value == value
    assert str(plugin_id) == value


@pytest.mark.parametrize(
    "value",
    (
        "",
        "security",
        "familyos",
        "familyos.",
        ".familyos.security",
        "familyos..security",
        "familyos.Security",
        "FamilyOS.security",
        "familyos.security!",
        "familyos security",
    ),
)
def test_runtime_plugin_id_rejects_invalid_identifiers(
    value: str,
) -> None:
    """Invalid runtime plugin identifiers should be rejected."""

    with pytest.raises(
        ValueError,
        match="Invalid runtime plugin identifier",
    ):
        RuntimePluginId(
            value,
        )


def test_runtime_plugin_id_is_immutable() -> None:
    """Runtime plugin identifiers should be immutable value objects."""

    plugin_id = RuntimePluginId(
        "familyos.security",
    )

    assert plugin_id == RuntimePluginId(
        "familyos.security",
    )


@pytest.mark.parametrize(
    "value",
    (
        "familyos.security",
        "familyos.my_plugin",
        "familyos.example.subsystem",
        "acme.calendar",
        "org.example_plugin",
    ),
)
def test_runtime_plugin_id_accepts_identifiers_accepted_by_plugin_id(
    value: str,
) -> None:
    """Runtime identifiers should follow the canonical PluginId contract."""

    from familyos_cli.plugins.identity import PluginId

    canonical_plugin_id = PluginId(
        value,
    )
    runtime_plugin_id = RuntimePluginId(
        value,
    )

    assert runtime_plugin_id.value == canonical_plugin_id.value


@pytest.mark.parametrize(
    "value",
    (
        "",
        "security",
        "familyos",
        "FamilyOS.security",
        "familyos.Security",
        "familyos-security",
        "familyos..security",
        "familyos security",
    ),
)
def test_runtime_plugin_id_rejects_identifiers_rejected_by_plugin_id(
    value: str,
) -> None:
    """Runtime identifiers should reject invalid canonical PluginIds."""

    from familyos_cli.plugins.identity import PluginId

    with pytest.raises(ValueError):
        PluginId(
            value,
        )

    with pytest.raises(
        ValueError,
        match="Invalid runtime plugin identifier",
    ):
        RuntimePluginId(
            value,
        )
