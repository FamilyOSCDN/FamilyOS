"""Architecture contracts for the canonical Quality Framework package layout."""

from __future__ import annotations

import ast
from pathlib import Path

import familyos_cli

_PACKAGE_ROOT = Path(familyos_cli.__file__).resolve().parent
_DOMAIN = _PACKAGE_ROOT / "domain" / "quality"
_APPLICATION = _PACKAGE_ROOT / "application" / "quality"
_PORTS = _PACKAGE_ROOT / "application" / "ports" / "quality"
_INFRASTRUCTURE = _PACKAGE_ROOT / "infrastructure" / "quality"

_DOMAIN_FORBIDDEN = (
    "familyos_cli.application",
    "familyos_cli.infrastructure",
    "familyos_cli.interfaces",
)
_APPLICATION_FORBIDDEN = (
    "familyos_cli.infrastructure",
    "familyos_cli.interfaces",
)
_TOOL_SPECIFIC = (
    "ruff",
    "mypy",
    "pytest",
    "_pytest",
    "github",
    "gitlab",
    "jenkins",
    "circleci",
)


def _sources(package: Path) -> tuple[Path, ...]:
    return tuple(sorted(package.rglob("*.py")))


def _imports(source_file: Path) -> tuple[str, ...]:
    tree = ast.parse(
        source_file.read_text(encoding="utf-8"),
        filename=str(source_file),
    )
    modules: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)

    return tuple(modules)


def _violations(
    package: Path,
    forbidden_prefixes: tuple[str, ...],
) -> tuple[str, ...]:
    violations: list[str] = []

    for source_file in _sources(package):
        for module in _imports(source_file):
            if module.startswith(forbidden_prefixes):
                violations.append(f"{source_file.relative_to(_PACKAGE_ROOT)}: {module}")

    return tuple(violations)


def test_canonical_quality_package_locations_exist() -> None:
    for package in (_DOMAIN, _APPLICATION, _PORTS, _INFRASTRUCTURE):
        assert package.is_dir()
        assert (package / "__init__.py").is_file()


def test_quality_domain_does_not_depend_on_outer_layers() -> None:
    assert _violations(_DOMAIN, _DOMAIN_FORBIDDEN) == ()


def test_quality_application_does_not_depend_on_outer_layers() -> None:
    assert _violations(_APPLICATION, _APPLICATION_FORBIDDEN) == ()
    assert _violations(_PORTS, _APPLICATION_FORBIDDEN) == ()


def test_quality_domain_has_no_tool_specific_dependency() -> None:
    assert _violations(_DOMAIN, _TOOL_SPECIFIC) == ()


def test_phase_eleven_exposes_profile_but_not_later_quality_domain_models() -> None:
    forbidden_symbols = {
        "QualityGate",
    }
    discovered: set[str] = set()

    for source_file in _sources(_DOMAIN):
        tree = ast.parse(
            source_file.read_text(encoding="utf-8"),
            filename=str(source_file),
        )
        discovered.update(
            node.name
            for node in ast.walk(tree)
            if isinstance(
                node,
                (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
            )
        )

    assert "QualityAssessment" in discovered
    assert "QualityProfile" in discovered
    assert discovered.isdisjoint(forbidden_symbols)


def test_phase_twelve_quality_cli_is_authorized() -> None:
    commands_dir = _PACKAGE_ROOT / "interfaces" / "cli" / "commands"
    assert (commands_dir / "quality.py").is_file()
