"""Tests for Plugin Identifier compatibility normalization."""

from familyos_cli.plugins.identity import (
    LEGACY_PLUGIN_ID_ALIASES,
    normalize_plugin_id,
)


def test_known_legacy_plugin_ids_are_normalized() -> None:
    """Known historical identifiers should resolve canonically."""

    assert normalize_plugin_id("education") == "familyos.education"
    assert normalize_plugin_id("documents") == "familyos.documents"
    assert (
        normalize_plugin_id("communication")
        == "familyos.communication"
    )
    assert (
        normalize_plugin_id("documentation")
        == "familyos.documentation"
    )


def test_canonical_plugin_id_is_unchanged() -> None:
    """Canonical identifiers should remain unchanged."""

    assert (
        normalize_plugin_id("familyos.education")
        == "familyos.education"
    )


def test_unknown_plugin_id_is_unchanged() -> None:
    """Third-party identifiers should not be rewritten."""

    assert normalize_plugin_id("acme.calendar") == "acme.calendar"


def test_normalization_is_idempotent() -> None:
    """Normalizing an identifier repeatedly should be stable."""

    plugin_id = normalize_plugin_id("education")

    assert normalize_plugin_id(plugin_id) == plugin_id


def test_legacy_alias_table_contains_only_explicit_migrations() -> None:
    """Compatibility aliases should remain explicit and governed."""

    assert LEGACY_PLUGIN_ID_ALIASES == {
        "education": "familyos.education",
        "documents": "familyos.documents",
        "communication": "familyos.communication",
        "documentation": "familyos.documentation",
    }
