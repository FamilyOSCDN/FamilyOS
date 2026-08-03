"""Health plugin capabilities."""

from familyos_cli.plugins.builtin.health.capabilities.health_profile_capability import (
    HealthProfileCapability,
)
from familyos_cli.plugins.builtin.health.capabilities.health_record_capability import (
    HealthRecordCapability,
)

__all__ = [
    "HealthProfileCapability",
    "HealthRecordCapability",
]
