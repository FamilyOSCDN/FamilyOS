"""Tests for the PLUGIN-ARCH-002 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.architecture_no_wildcard_imports_validator import (
    ArchitectureNoWildcardImportsValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_when_no_wildcard_imports(tmp_path: Path) -> None:
    """PASS when no source file uses a wildcard import."""

    (tmp_path / "module.py").write_text(
        "from dataclasses import dataclass\n",
        encoding="utf-8",
    )

    context = make_context(tmp_path, manifest={})
    validator = ArchitectureNoWildcardImportsValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_when_wildcard_import_present(tmp_path: Path) -> None:
    """FAIL when a source file uses a wildcard import."""

    (tmp_path / "module.py").write_text(
        "from dataclasses import *\n",
        encoding="utf-8",
    )

    context = make_context(tmp_path, manifest={})
    validator = ArchitectureNoWildcardImportsValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL
