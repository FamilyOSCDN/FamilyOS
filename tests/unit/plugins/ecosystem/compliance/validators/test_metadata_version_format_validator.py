"""Tests for the PLUGIN-META-002 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.metadata_version_format_validator import (
    MetadataVersionFormatValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_for_valid_semver(tmp_path: Path) -> None:
    """PASS when the manifest version is a valid semantic version."""

    context = make_context(tmp_path, manifest={"version": "1.2.3"})
    validator = MetadataVersionFormatValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_for_invalid_semver(tmp_path: Path) -> None:
    """FAIL when the manifest version is not a valid semantic version."""

    context = make_context(tmp_path, manifest={"version": "not-a-version"})
    validator = MetadataVersionFormatValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL


def test_not_evaluated_when_manifest_missing(tmp_path: Path) -> None:
    """NOT_EVALUATED when the manifest is unavailable."""

    context = make_context(tmp_path, manifest=None)
    validator = MetadataVersionFormatValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.NOT_EVALUATED
