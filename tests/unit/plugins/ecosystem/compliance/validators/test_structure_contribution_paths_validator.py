"""Tests for the PLUGIN-STRUCT-003 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.structure_contribution_paths_validator import (
    StructureContributionPathsValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_when_no_contributions(tmp_path: Path) -> None:
    """PASS when the plugin declares no template contributions."""

    context = make_context(
        tmp_path,
        manifest={},
        module="tests.fixtures.sample_plugin.plugin",
        class_name="SamplePlugin",
    )
    validator = StructureContributionPathsValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_when_contribution_path_missing(tmp_path: Path) -> None:
    """FAIL when a declared template directory does not exist."""

    context = make_context(
        tmp_path,
        manifest={},
        plugin_id="familyos.violation",
        module="tests.fixtures.compliance_violation_plugin.plugin",
        class_name="ViolationPlugin",
    )
    validator = StructureContributionPathsValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL


def test_not_evaluated_when_plugin_fails_to_load(tmp_path: Path) -> None:
    """NOT_EVALUATED when the plugin entry point cannot be loaded."""

    context = make_context(
        tmp_path,
        manifest={},
        module="tests.fixtures.does_not_exist.plugin",
        class_name="Nope",
    )
    validator = StructureContributionPathsValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.NOT_EVALUATED
