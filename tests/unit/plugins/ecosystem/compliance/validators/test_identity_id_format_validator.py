"""Tests for the PLUGIN-IDENT-002 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.identity_id_format_validator import (
    IdentityIdFormatValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_for_canonical_id(tmp_path: Path) -> None:
    """PASS when the manifest id is a canonical Plugin Identifier."""

    context = make_context(tmp_path, manifest={"id": "familyos.fixture"})
    validator = IdentityIdFormatValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_for_noncanonical_id(tmp_path: Path) -> None:
    """FAIL when the manifest id is not a canonical Plugin Identifier."""

    context = make_context(tmp_path, manifest={"id": "Not Valid!"})
    validator = IdentityIdFormatValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL


def test_not_evaluated_when_manifest_missing(tmp_path: Path) -> None:
    """NOT_EVALUATED when the manifest is unavailable."""

    context = make_context(tmp_path, manifest=None)
    validator = IdentityIdFormatValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.NOT_EVALUATED
