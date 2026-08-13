"""Tests for the default compliance validator registry factory."""

from familyos_cli.plugins.ecosystem.compliance.rules.default_rule_catalog import (
    DEFAULT_COMPLIANCE_RULES,
)
from familyos_cli.plugins.ecosystem.compliance.validators.default_validator_registry import (
    build_default_validator_registry,
)


def test_registry_has_eighteen_validators() -> None:
    """The default registry registers one validator per rule."""

    registry = build_default_validator_registry()

    assert len(registry.list()) == 18


def test_registry_covers_every_rule_validator_id() -> None:
    """Every rule's validator_id resolves in the default registry."""

    registry = build_default_validator_registry()

    for rule in DEFAULT_COMPLIANCE_RULES:
        registry.get(rule.validator_id)
