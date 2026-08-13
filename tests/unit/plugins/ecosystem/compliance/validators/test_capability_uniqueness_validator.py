"""Tests for the PLUGIN-CAP-002 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.capability_uniqueness_validator import (
    CapabilityUniquenessValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_when_no_capabilities(tmp_path: Path) -> None:
    """PASS when the plugin declares no capabilities."""

    context = make_context(
        tmp_path,
        manifest={},
        module="tests.fixtures.sample_plugin.plugin",
        class_name="SamplePlugin",
    )
    validator = CapabilityUniquenessValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_when_display_names_empty_or_duplicated(tmp_path: Path) -> None:
    """FAIL when capability display names are empty or duplicated."""

    context = make_context(
        tmp_path,
        manifest={},
        plugin_id="familyos.violation",
        module="tests.fixtures.compliance_violation_plugin.plugin",
        class_name="ViolationPlugin",
    )
    validator = CapabilityUniquenessValidator()

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
    validator = CapabilityUniquenessValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.NOT_EVALUATED
