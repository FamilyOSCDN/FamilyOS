"""Tests for canonical Plugin Identifier."""

import pytest

from familyos_cli.plugins.identity.plugin_id import (
    PluginId,
)


@pytest.mark.parametrize(
    "value",
    [
        "familyos.security",
        "familyos.health",
        "familyos.finance",
        "familyos.education",
        "familyos.documents",
        "familyos.communication",
        "acme.calendar",
        "org.example_plugin",
    ],
)
def test_plugin_id_accepts_canonical_identifiers(
    value: str,
) -> None:
    """Canonical Plugin Identifiers should be accepted."""

    plugin_id = PluginId(
        value,
    )

    assert plugin_id.value == value
    assert str(plugin_id) == value


@pytest.mark.parametrize(
    "value",
    [
        "",
        "education",
        "FamilyOS.security",
        "familyos.Security",
        "familyos-security",
        ".familyos.security",
        "familyos.security.",
        "familyos..security",
        "familyos security",
    ],
)
def test_plugin_id_rejects_non_canonical_identifiers(
    value: str,
) -> None:
    """Non-canonical Plugin Identifiers should be rejected."""

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        PluginId(
            value,
        )
