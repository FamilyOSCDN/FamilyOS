"""Plugin verification service."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.verification.verification_result import (
    VerificationResult,
)


class PluginVerifier:
    """Verify plugin packages."""

    def verify(
        self,
        package: PluginPackage,
    ) -> VerificationResult:
        """Verify a plugin package.

        Args:
            package: Plugin package to verify.

        Returns:
            Package verification result.
        """

        if not package.plugin_id:
            return VerificationResult(
                valid=False,
                reason="Plugin identifier is missing.",
            )

        if not package.version:
            return VerificationResult(
                valid=False,
                reason="Plugin version is missing.",
            )

        return VerificationResult(
            valid=True,
            reason="Package verified.",
        )
