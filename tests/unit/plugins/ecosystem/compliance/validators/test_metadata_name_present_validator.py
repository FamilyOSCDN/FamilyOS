"""Tests for the PLUGIN-META-001 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.metadata_name_present_validator import (
    MetadataNamePresentValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_when_name_present(tmp_path: Path) -> None:
    """PASS when the manifest name is non-empty."""

    context = make_context(tmp_path, manifest={"name": "Fixture"})
    validator = MetadataNamePresentValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_when_name_empty(tmp_path: Path) -> None:
    """FAIL when the manifest name is empty."""

    context = make_context(tmp_path, manifest={"name": "  "})
    validator = MetadataNamePresentValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL


def test_fail_when_name_is_yaml_null(tmp_path: Path) -> None:
    """FAIL (not a validator crash) when the manifest name is YAML null.

    A 'name:' key with no value parses as None, not an absent key, so
    naive dict.get(key, default) does not protect against it.
    """

    context = make_context(tmp_path, manifest={"name": None})
    validator = MetadataNamePresentValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL


def test_not_evaluated_when_manifest_missing(tmp_path: Path) -> None:
    """NOT_EVALUATED when the manifest is unavailable."""

    context = make_context(tmp_path, manifest=None)
    validator = MetadataNamePresentValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.NOT_EVALUATED
