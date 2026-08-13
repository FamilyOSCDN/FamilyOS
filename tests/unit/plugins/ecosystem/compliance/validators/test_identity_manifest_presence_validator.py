"""Tests for the PLUGIN-IDENT-001 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.identity_manifest_presence_validator import (
    IdentityManifestPresenceValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_when_manifest_present(tmp_path: Path) -> None:
    """PASS when the manifest was parsed successfully."""

    context = make_context(tmp_path, manifest={"id": "familyos.fixture"})
    validator = IdentityManifestPresenceValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_when_manifest_missing(tmp_path: Path) -> None:
    """FAIL when the manifest could not be parsed."""

    context = make_context(
        tmp_path,
        manifest=None,
        manifest_error="Manifest file not found",
    )
    validator = IdentityManifestPresenceValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL
