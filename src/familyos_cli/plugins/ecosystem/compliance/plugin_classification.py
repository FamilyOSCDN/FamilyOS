"""Plugin classification used to resolve compliance profile applicability."""

from __future__ import annotations

from enum import StrEnum


class PluginClassification(StrEnum):
    """Represent the ecosystem classification of an evaluated plugin.

    Only ``OFFICIAL`` is produced by this implementation slice (plugins
    discovered under ``plugins/builtin`` are classified structurally, see
    :mod:`~familyos_cli.plugins.ecosystem.compliance.plugin_classification_resolver`).
    """

    OFFICIAL = "official"
    THIRD_PARTY = "third_party"
    DEVELOPMENT = "development"
