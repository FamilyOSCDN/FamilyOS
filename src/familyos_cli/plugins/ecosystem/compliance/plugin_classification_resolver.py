"""Plugin classification resolution.

Neither PluginMetadata, PluginDescriptor, nor plugin.yaml carries an
explicit classification field today. This slice resolves classification
structurally, from the discovery root a plugin was found under, rather
than inventing an unverified heuristic (e.g. a path-prefix guess). Any
plugin discovered under the official plugins root is classified OFFICIAL
by construction. A real 'classification' manifest field is future work
(see docs/epics/EPIC-PLUGIN-002-plugin-compliance-framework/
05-Compliance-Domains.md).
"""

from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.plugin_classification import (
    PluginClassification,
)
from familyos_cli.plugins.models import PluginDescriptor


class PluginClassificationResolver:
    """Resolve a plugin's classification from its discovery root."""

    @staticmethod
    def classify(
        descriptor: PluginDescriptor,
        discovery_root: Path,
    ) -> PluginClassification:
        """Classify a plugin as OFFICIAL if discovered under the given root."""

        try:
            descriptor.path.resolve().relative_to(discovery_root.resolve())
        except ValueError:
            return PluginClassification.THIRD_PARTY

        return PluginClassification.OFFICIAL
