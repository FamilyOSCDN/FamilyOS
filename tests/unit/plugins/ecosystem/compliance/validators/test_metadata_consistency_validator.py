"""Tests for the PLUGIN-META-004 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.metadata_consistency_validator import (
    MetadataConsistencyValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_when_versions_match(tmp_path: Path) -> None:
    """PASS when manifest version matches the loaded plugin's metadata."""

    context = make_context(
        tmp_path,
        manifest={"version": "1.0.0"},
        module="tests.fixtures.sample_plugin.plugin",
        class_name="SamplePlugin",
    )
    validator = MetadataConsistencyValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_when_versions_differ(tmp_path: Path) -> None:
    """FAIL when manifest version differs from the loaded plugin's metadata."""

    context = make_context(
        tmp_path,
        manifest={"version": "9.9.9"},
        module="tests.fixtures.sample_plugin.plugin",
        class_name="SamplePlugin",
    )
    validator = MetadataConsistencyValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL


def test_not_evaluated_when_manifest_missing(tmp_path: Path) -> None:
    """NOT_EVALUATED when the manifest is unavailable."""

    context = make_context(tmp_path, manifest=None)
    validator = MetadataConsistencyValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.NOT_EVALUATED


def test_not_evaluated_when_plugin_fails_to_load(tmp_path: Path) -> None:
    """NOT_EVALUATED when the plugin entry point cannot be loaded."""

    context = make_context(
        tmp_path,
        manifest={"version": "1.0.0"},
        module="tests.fixtures.does_not_exist.plugin",
        class_name="Nope",
    )
    validator = MetadataConsistencyValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.NOT_EVALUATED
