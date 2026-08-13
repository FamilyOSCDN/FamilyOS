"""Tests for the PLUGIN-IDENT-003 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.identity_namespace_validator import (
    IdentityNamespaceValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_for_official_namespace(tmp_path: Path) -> None:
    """PASS when the manifest id starts with 'familyos.'."""

    context = make_context(tmp_path, manifest={"id": "familyos.fixture"})
    validator = IdentityNamespaceValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_for_other_namespace(tmp_path: Path) -> None:
    """FAIL when the manifest id does not start with 'familyos.'."""

    context = make_context(tmp_path, manifest={"id": "acme.fixture"})
    validator = IdentityNamespaceValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL


def test_not_evaluated_when_manifest_missing(tmp_path: Path) -> None:
    """NOT_EVALUATED when the manifest is unavailable."""

    context = make_context(tmp_path, manifest=None)
    validator = IdentityNamespaceValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.NOT_EVALUATED
