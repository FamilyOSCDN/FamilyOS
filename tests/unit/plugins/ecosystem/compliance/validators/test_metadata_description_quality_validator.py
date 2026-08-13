"""Tests for the PLUGIN-META-003 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.metadata_description_quality_validator import (
    MetadataDescriptionQualityValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_for_long_description(tmp_path: Path) -> None:
    """PASS when the description is at least 20 characters."""

    context = make_context(
        tmp_path,
        manifest={"description": "This description is definitely long enough."},
    )
    validator = MetadataDescriptionQualityValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_for_short_description(tmp_path: Path) -> None:
    """FAIL when the description is shorter than 20 characters."""

    context = make_context(tmp_path, manifest={"description": "Too short"})
    validator = MetadataDescriptionQualityValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL


def test_not_evaluated_when_manifest_missing(tmp_path: Path) -> None:
    """NOT_EVALUATED when the manifest is unavailable."""

    context = make_context(tmp_path, manifest=None)
    validator = MetadataDescriptionQualityValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.NOT_EVALUATED
