"""Check plugin compliance use case."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.compliance_engine import (
    ComplianceEngine,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_request import (
    ComplianceRequest,
)
from familyos_cli.plugins.ecosystem.compliance.profile_registry import (
    ProfileRegistry,
)
from familyos_cli.plugins.ecosystem.compliance.reporting.compliance_report import (
    COMPLIANCE_FRAMEWORK_VERSION,
    REPORT_SCHEMA_VERSION,
    ComplianceReport,
)
from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin_loader import PluginLoader


class CheckPluginComplianceUseCase:
    """Evaluate one plugin's compliance and produce a report."""

    def __init__(
        self,
        *,
        engine: ComplianceEngine,
        profile_registry: ProfileRegistry,
        plugin_loader: PluginLoader,
        plugins_root: Path,
    ) -> None:
        """Initialize the use case."""

        self._engine = engine
        self._profile_registry = profile_registry
        self._plugin_loader = plugin_loader
        self._plugins_root = plugins_root

    def execute(
        self,
        *,
        plugin_id: str,
        profile_id: str = "official",
    ) -> ComplianceReport:
        """Evaluate the named plugin and return its compliance report."""

        descriptor = self._find_descriptor(plugin_id)

        profile = self._profile_registry.get(profile_id)

        result = self._engine.evaluate(
            ComplianceRequest(
                plugin_descriptor=descriptor,
                profile_id=profile_id,
            ),
        )

        return ComplianceReport(
            schema_version=REPORT_SCHEMA_VERSION,
            framework_version=COMPLIANCE_FRAMEWORK_VERSION,
            profile_version=profile.version,
            result=result,
        )

    def _find_descriptor(
        self,
        plugin_id: str,
    ) -> PluginDescriptor:
        """Find the descriptor for a plugin id under the discovery root."""

        for descriptor in self._plugin_loader.discover(self._plugins_root):
            if descriptor.id == plugin_id:
                return descriptor

        raise ValueError(
            f"Plugin '{plugin_id}' was not found under {self._plugins_root}",
        )
