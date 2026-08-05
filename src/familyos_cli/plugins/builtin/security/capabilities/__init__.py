"""Public capabilities exposed by the Security Plugin."""

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)

from .security_policy_capability import (
    SecurityPolicyCapability,
)
from .security_validation_capability import (
    SecurityValidationCapability,
)

SECURITY_POLICY_CAPABILITY = SecurityPolicyCapability.create()

SECURITY_VALIDATION_CAPABILITY = SecurityValidationCapability.create()


SECURITY_CAPABILITIES: tuple[PluginCapability, ...] = (
    SECURITY_POLICY_CAPABILITY,
    SECURITY_VALIDATION_CAPABILITY,
)


__all__ = [
    "SECURITY_CAPABILITIES",
    "SECURITY_POLICY_CAPABILITY",
    "SECURITY_VALIDATION_CAPABILITY",
    "SecurityPolicyCapability",
    "SecurityValidationCapability",
]
