"""Tests for the compliance validator registry."""

import pytest

from familyos_cli.plugins.ecosystem.compliance.compliance_evidence import (
    ComplianceEvidence,
)
from familyos_cli.plugins.ecosystem.compliance.ports.compliance_validator import (
    ComplianceValidator,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validation_context import (
    ValidationContext,
)
from familyos_cli.plugins.ecosystem.compliance.validator_registry import (
    ValidatorRegistry,
)
from familyos_cli.plugins.ecosystem.compliance.validator_run_result import (
    ValidatorRunResult,
)
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)


class _FakeValidator(ComplianceValidator):
    def validate(self, context: ValidationContext) -> ValidatorRunResult:
        return ValidatorRunResult(status=ValidatorStatus.SUCCESS, evidence=())

    def check(
        self,
        evidence: tuple[ComplianceEvidence, ...],
    ) -> RuleOutcome:
        return RuleOutcome.PASS


def test_register_and_get_validator() -> None:
    """A registered validator can be retrieved by logical id."""

    registry = ValidatorRegistry()
    validator = _FakeValidator()

    registry.register("test.validator", validator)

    assert registry.get("test.validator") is validator


def test_register_duplicate_validator_raises() -> None:
    """Registering the same validator id twice raises ValueError."""

    registry = ValidatorRegistry()
    registry.register("test.validator", _FakeValidator())

    with pytest.raises(ValueError, match="already registered"):
        registry.register("test.validator", _FakeValidator())


def test_get_missing_validator_raises() -> None:
    """Retrieving an unregistered validator id raises ValueError."""

    registry = ValidatorRegistry()

    with pytest.raises(ValueError, match="not registered"):
        registry.get("missing.validator")


def test_list_returns_all_validator_ids() -> None:
    """list() returns every registered validator id."""

    registry = ValidatorRegistry()
    registry.register("test.a", _FakeValidator())
    registry.register("test.b", _FakeValidator())

    assert set(registry.list()) == {"test.a", "test.b"}
