"""Security context domain model."""

from __future__ import annotations

from dataclasses import dataclass

from .security_level import SecurityLevel


@dataclass(
    frozen=True,
    slots=True,
)
class SecurityContext:
    """Context used during security evaluation."""

    domain_name: str

    resource: str

    required_level: SecurityLevel
