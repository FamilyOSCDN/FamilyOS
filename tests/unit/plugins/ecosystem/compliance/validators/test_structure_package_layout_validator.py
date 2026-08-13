"""Tests for the PLUGIN-STRUCT-002 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.structure_package_layout_validator import (
    StructurePackageLayoutValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_for_proper_package_layout(tmp_path: Path) -> None:
    """PASS when __init__.py and plugin.yaml both sit at the root."""

    (tmp_path / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "plugin.yaml").write_text("id: familyos.fixture\n", encoding="utf-8")

    context = make_context(tmp_path, manifest={"id": "familyos.fixture"})
    validator = StructurePackageLayoutValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_when_init_missing(tmp_path: Path) -> None:
    """FAIL when __init__.py is missing at the plugin root."""

    (tmp_path / "plugin.yaml").write_text("id: familyos.fixture\n", encoding="utf-8")

    context = make_context(tmp_path, manifest={"id": "familyos.fixture"})
    validator = StructurePackageLayoutValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL
