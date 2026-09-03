"""Static repository domain imports normalized into canonical Quality results."""

from __future__ import annotations

import ast
import platform
import time
import tokenize
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from familyos_cli.application.ports.quality import QualityExecutorPort
from familyos_cli.application.quality import QualityCheckResult
from familyos_cli.application.quality.domain_boundary_quality_policy import (
    DOMAIN_FORBIDDEN_MODULES,
    DOMAIN_SOURCE_ROOT,
)
from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityEvidence,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityEvidenceType,
    QualityFinding,
    QualityFindingId,
    QualityRule,
    QualityStatus,
    QualityTarget,
)


def _raise_walk_error(error: OSError) -> None:
    raise error


def _sources(repository: Path) -> tuple[Path, ...]:
    root = repository
    for part in Path(DOMAIN_SOURCE_ROOT).parts:
        root = root / part
        if root.is_symlink():
            raise ValueError(f"Architecture source must not be a symbolic link: {root}")
    if not root.is_dir():
        raise ValueError(f"Architecture source root is missing: {DOMAIN_SOURCE_ROOT}")
    sources: list[Path] = []
    for directory, dirs, files in root.walk(on_error=_raise_walk_error):
        dirs.sort()
        files.sort()
        for name in (*dirs, *files):
            if (directory / name).is_symlink():
                raise ValueError(
                    f"Architecture source contains a symbolic link: {directory / name}"
                )
        sources.extend(
            directory / name for name in files if Path(name).suffix in (".py", ".pyi")
        )
    if not sources:
        raise ValueError("Architecture source tree contains no Python files")
    return tuple(
        sorted(sources, key=lambda path: path.relative_to(repository).as_posix())
    )


def _import_modules(
    node: ast.Import | ast.ImportFrom, package: tuple[str, ...]
) -> tuple[str, ...]:
    if isinstance(node, ast.Import):
        return tuple(alias.name for alias in node.names)
    if node.level:
        if node.level > len(package):
            raise ValueError("Relative import escapes its Python package")
        base = package[: len(package) - node.level + 1]
    else:
        base = ()
    if node.module:
        base += tuple(node.module.split("."))
    module = ".".join(base)
    return (module, *(f"{module}.{alias.name}" for alias in node.names))


def _forbidden(module: str) -> bool:
    return any(
        module == prefix or module.startswith(prefix + ".")
        for prefix in DOMAIN_FORBIDDEN_MODULES
    )


def _violations(repository: Path, source: Path) -> list[tuple[str, int, int, str]]:
    relative = source.relative_to(repository).as_posix()
    with tokenize.open(source) as stream:
        tree = ast.parse(stream.read(), filename=relative)
    module = source.relative_to(repository / "src").with_suffix("").parts
    package = module[:-1]
    violations: list[tuple[str, int, int, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        modules = _import_modules(node, package)
        # A forbidden from-module is one edge, regardless of imported symbols.
        if isinstance(node, ast.ImportFrom) and _forbidden(modules[0]):
            modules = modules[:1]
        for imported in sorted(set(modules)):
            if _forbidden(imported):
                violations.append(
                    (relative, node.lineno, node.col_offset + 1, imported)
                )
    return violations


class DomainBoundaryQualityExecutor(QualityExecutorPort):
    """Verify the frozen repository domain boundary without executing source."""

    def __init__(
        self,
        *,
        finding_id_factory: Callable[[], QualityFindingId],
        evidence_id_factory: Callable[[], QualityEvidenceId],
        clock: Callable[[], datetime] | None = None,
        monotonic_clock: Callable[[], float] | None = None,
    ) -> None:
        self._finding_id_factory = finding_id_factory
        self._evidence_id_factory = evidence_id_factory
        self._clock = clock or (lambda: datetime.now(UTC))
        self._monotonic_clock = monotonic_clock or time.monotonic

    def execute(
        self, *, check_id: QualityCheckId, rule: QualityRule, target: QualityTarget
    ) -> QualityCheckResult:
        started = self._monotonic_clock()
        evidence_id = self._evidence_id_factory()
        findings: tuple[QualityFinding, ...] = ()
        diagnostics: tuple[str, ...] = ()
        metadata: tuple[tuple[str, str], ...] = (
            ("source_root", DOMAIN_SOURCE_ROOT),
            ("forbidden_modules", "\n".join(DOMAIN_FORBIDDEN_MODULES)),
        )
        try:
            if target.target_type != "repository" or target.path is None:
                raise ValueError(
                    "Architecture check requires a repository target with a path"
                )
            repository = Path(target.path).resolve(strict=True)
            sources = _sources(repository)
            violations = sorted(
                item for source in sources for item in _violations(repository, source)
            )
        except (OSError, ValueError, SyntaxError, UnicodeError) as exc:
            status, outcome = QualityStatus.ERROR, QualityEvidenceResult.ERROR
            diagnostics = (f"Architecture scan failed: {exc}",)
            metadata += (("error_kind", "architecture_scan_failed"),)
        else:
            status = QualityStatus.FAIL if violations else QualityStatus.PASS
            outcome = (
                QualityEvidenceResult.FAIL if violations else QualityEvidenceResult.PASS
            )
            findings = tuple(
                QualityFinding(
                    id=self._finding_id_factory(),
                    rule_id=rule.id,
                    domain=rule.domain,
                    severity=rule.severity,
                    status=QualityStatus.FAIL,
                    message=f"Domain source imports forbidden outer-layer module: {module}",
                    target=target,
                    location=f"{path}:{line}:{column}",
                    evidence_ids=(str(evidence_id),),
                )
                for path, line, column, module in violations
            )
            metadata += (
                ("inspected_files", str(len(sources))),
                ("violations", str(len(findings))),
            )
        evidence = QualityEvidence(
            id=evidence_id,
            type=QualityEvidenceType("ARCHITECTURE"),
            source="quality.architecture",
            target=target,
            revision=target.revision,
            result=outcome,
            created_at=self._clock(),
            rule_id=rule.id,
            requirement_id=rule.requirement_id,
            tool="python.ast",
            tool_version=platform.python_version(),
            metadata=metadata,
        )
        return QualityCheckResult(
            check_id=check_id,
            status=status,
            findings=findings,
            evidence=(evidence,),
            diagnostics=diagnostics,
            duration_seconds=max(0.0, self._monotonic_clock() - started),
        )
