"""FamilyOS Security Plugin."""

from __future__ import annotations

from familyos_cli.plugins.builtin.security.capabilities import (
    SECURITY_CAPABILITIES,
)
from familyos_cli.plugins.builtin.security.contributions import (
    SECURITY_CONTRIBUTIONS,
)
from familyos_cli.plugins.builtin.security.validation.security_validator import (
    SecurityValidator,
)
from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)
from familyos_cli.plugins.models import PluginMetadata
from familyos_cli.plugins.plugin import (
    Plugin,
)


class SecurityPlugin(Plugin):
    """Official FamilyOS security plugin."""

    metadata = PluginMetadata(
        name="FamilyOS Security Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description=(
            "Provides security capabilities, policies, "
            "validation rules, and security-related "
            "contributions for FamilyOS."
        ),
    )

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return capabilities exposed by the plugin."""

        return SECURITY_CAPABILITIES

    def validator(
        self,
    ) -> SecurityValidator:
        """Return security validator."""

        return SecurityValidator()

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return contributions exposed by the plugin."""

        return SECURITY_CONTRIBUTIONS
