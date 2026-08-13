"""Compliance validator registry."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.ecosystem.compliance.ports.compliance_validator import (
    ComplianceValidator,
)


@dataclass(slots=True)
class ValidatorRegistry:
    """Registry of governed compliance validators, keyed by logical id.

    Rules reference validators through this registry via a plain string
    (``ComplianceRule.validator_id``) rather than importing validator
    implementation modules directly.
    """

    _validators: dict[str, ComplianceValidator] = field(default_factory=dict)

    def register(
        self,
        validator_id: str,
        validator: ComplianceValidator,
    ) -> None:
        """Register a compliance validator by its logical identifier."""

        if validator_id in self._validators:
            raise ValueError(
                f"Compliance validator '{validator_id}' is already registered",
            )

        self._validators[validator_id] = validator

    def get(
        self,
        validator_id: str,
    ) -> ComplianceValidator:
        """Retrieve a compliance validator by logical identifier."""

        if validator_id not in self._validators:
            raise ValueError(
                f"Compliance validator '{validator_id}' is not registered",
            )

        return self._validators[validator_id]

    def list(
        self,
    ) -> list[str]:
        """Return all registered validator logical identifiers."""

        return list(self._validators.keys())
