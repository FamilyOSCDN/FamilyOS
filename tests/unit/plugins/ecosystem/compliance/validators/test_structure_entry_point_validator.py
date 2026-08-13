"""Tests for the PLUGIN-STRUCT-001 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.structure_entry_point_validator import (
    StructureEntryPointValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_when_entry_point_loads(tmp_path: Path) -> None:
    """PASS when the module and class both resolve to a Plugin subclass."""

    context = make_context(
        tmp_path,
        manifest={},
        module="tests.fixtures.sample_plugin.plugin",
        class_name="SamplePlugin",
    )
    validator = StructureEntryPointValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_when_module_does_not_exist(tmp_path: Path) -> None:
    """FAIL when the manifest module cannot be imported."""

    context = make_context(
        tmp_path,
        manifest={},
        module="tests.fixtures.does_not_exist.plugin",
        class_name="Nope",
    )
    validator = StructureEntryPointValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL
