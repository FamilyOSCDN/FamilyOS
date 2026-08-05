"""Health context model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.builtin.health.domain.health_level import (
    HealthLevel,
)


@dataclass(
    frozen=True,
    slots=True,
)
class HealthContext:
    """Context used for health evaluation."""

    domain_name: str

    subject: str

    required_level: HealthLevel
