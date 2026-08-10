"""Plugin Identifier compatibility normalization."""


LEGACY_PLUGIN_ID_ALIASES: dict[str, str] = {
    "education": "familyos.education",
    "documents": "familyos.documents",
    "communication": "familyos.communication",
    "documentation": "familyos.documentation",
}


def normalize_plugin_id(
    plugin_id: str,
) -> str:
    """Return the canonical Plugin Identifier for a known legacy alias.

    Canonical and unknown Plugin Identifiers are returned unchanged.
    """

    return LEGACY_PLUGIN_ID_ALIASES.get(
        plugin_id,
        plugin_id,
    )
