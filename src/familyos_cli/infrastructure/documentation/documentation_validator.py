"""Deterministic Documentation Framework validation primitives."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from yaml import YAMLError

_NUMBERED_DOCUMENT = re.compile(r"^(?P<number>\d{2})-.+\.md$")
_MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\((?P<target>[^)]+)\)")
_FENCE = re.compile(r"^\s*(```|~~~)")
_HEADING = re.compile(r"^(?P<marks>#{1,6})\s+\S")


@dataclass(frozen=True, slots=True)
class DocumentationViolation:
    """One actionable documentation-framework violation."""

    kind: str
    message: str
    location: str | None = None


@dataclass(frozen=True, slots=True)
class DocumentationValidationResult:
    """Structured result produced before Quality normalization."""

    violations: tuple[DocumentationViolation, ...]


class DocumentationValidator:
    """Validate deterministic EPIC documentation contracts."""

    @staticmethod
    def validate_repository_scope(epic_roots: tuple[str, ...]) -> None:
        """Reject ambiguous or empty repository scope configuration."""
        if not isinstance(epic_roots, tuple):
            raise TypeError("Repository documentation scope must be a tuple")
        if not epic_roots:
            raise ValueError("Repository documentation scope must not be empty")
        seen: set[str] = set()
        for relative in epic_roots:
            if not isinstance(relative, str):
                raise TypeError("Repository documentation roots must be strings")
            parts = relative.split("/")
            if (
                len(parts) != 3
                or parts[:2] != ["docs", "epics"]
                or parts[2] in ("", ".", "..")
                or "\\" in relative
                or any(unicodedata.category(char) == "Cc" for char in relative)
            ):
                raise ValueError(
                    "Repository documentation roots must be canonical relative "
                    f"directories immediately under docs/epics/: {relative!r}"
                )
            if relative in seen:
                raise ValueError(f"Duplicate repository documentation root: {relative}")
            seen.add(relative)

    def validate_repository(
        self, root: Path, *, epic_roots: tuple[str, ...]
    ) -> DocumentationValidationResult:
        """Aggregate the explicitly configured EPIC inventories in order."""
        self.validate_repository_scope(epic_roots)
        if not root.is_dir():
            raise ValueError(f"Repository documentation target is not a directory: {root}")
        repository_root = root.resolve()
        violations: list[DocumentationViolation] = []
        for relative in epic_roots:
            epic_root = root / relative
            if not epic_root.resolve().is_relative_to(repository_root):
                raise ValueError(
                    f"Repository documentation root resolves outside the target: {relative}"
                )
            result = self.validate(epic_root)
            violations.extend(
                DocumentationViolation(
                    kind=violation.kind,
                    message=violation.message,
                    location=(
                        f"{relative}/{violation.location}"
                        if violation.location is not None
                        else relative
                    ),
                )
                for violation in result.violations
            )
        return DocumentationValidationResult(tuple(violations))

    def validate(self, root: Path) -> DocumentationValidationResult:
        violations: list[DocumentationViolation] = []
        epic_yaml = root / "EPIC.yaml"

        if not epic_yaml.is_file():
            return DocumentationValidationResult(
                (
                    DocumentationViolation(
                        "required_file",
                        "Required documentation file is missing: EPIC.yaml",
                        "EPIC.yaml",
                    ),
                )
            )

        try:
            raw = epic_yaml.read_text(encoding="utf-8")
        except OSError:
            raise

        try:
            loaded = yaml.safe_load(raw)
        except YAMLError as exc:
            return DocumentationValidationResult(
                (
                    DocumentationViolation(
                        "epic_yaml",
                        f"EPIC.yaml is not valid YAML: {exc}",
                        "EPIC.yaml",
                    ),
                )
            )

        if not isinstance(loaded, dict):
            return DocumentationValidationResult(
                (
                    DocumentationViolation(
                        "epic_yaml",
                        "EPIC.yaml must contain a YAML mapping.",
                        "EPIC.yaml",
                    ),
                )
            )

        deliverables = loaded.get("deliverables")
        if not isinstance(deliverables, list) or not all(
            isinstance(item, str) and item for item in deliverables
        ):
            violations.append(
                DocumentationViolation(
                    "epic_yaml",
                    "EPIC.yaml deliverables must be a list of non-empty file names.",
                    "EPIC.yaml",
                )
            )
            deliverable_names: tuple[str, ...] = ()
        else:
            deliverable_names = tuple(deliverables)

        structure = loaded.get("structure")
        if not isinstance(structure, dict):
            violations.append(
                DocumentationViolation(
                    "epic_yaml",
                    "EPIC.yaml structure must be a mapping.",
                    "EPIC.yaml",
                )
            )
            structure = {}

        self._validate_declared_inventory(root, deliverable_names, violations)
        self._validate_structure(deliverable_names, structure, violations)

        markdown_files = tuple(
            root / name for name in deliverable_names if name.endswith(".md")
        )
        self._validate_markdown(markdown_files, root, violations)

        return DocumentationValidationResult(tuple(violations))

    @staticmethod
    def _validate_declared_inventory(
        root: Path,
        deliverables: tuple[str, ...],
        violations: list[DocumentationViolation],
    ) -> None:
        for name in deliverables:
            path = root / name
            if not path.is_file():
                violations.append(
                    DocumentationViolation(
                        "required_file",
                        f"Required documentation file is missing: {name}",
                        name,
                    )
                )
                continue
            try:
                if path.stat().st_size == 0:
                    violations.append(
                        DocumentationViolation(
                            "empty_file",
                            f"Required documentation file is empty: {name}",
                            name,
                        )
                    )
            except OSError:
                raise

    @staticmethod
    def _validate_structure(
        deliverables: tuple[str, ...],
        structure: dict[object, object],
        violations: list[DocumentationViolation],
    ) -> None:
        numbered = [
            name for name in deliverables if _NUMBERED_DOCUMENT.fullmatch(name)
        ]
        groups: dict[str, list[str]] = {}
        for name in numbered:
            match = _NUMBERED_DOCUMENT.fullmatch(name)
            assert match is not None
            groups.setdefault(match.group("number"), []).append(name)

        for number, names in sorted(groups.items()):
            if len(names) > 1:
                violations.append(
                    DocumentationViolation(
                        "duplicate_chapter",
                        f"Duplicate numbered chapter {number}: {', '.join(names)}",
                        ", ".join(names),
                    )
                )

        expected_count = structure.get("numbered_documents")
        if (
            isinstance(expected_count, int)
            and not isinstance(expected_count, bool)
            and len(numbered) != expected_count
        ):
            violations.append(
                DocumentationViolation(
                    "numbered_documents",
                    "Numbered document count does not match EPIC.yaml structure: "
                    f"expected {expected_count}, found {len(numbered)}.",
                    "EPIC.yaml",
                )
            )

        expected_files = structure.get("canonical_files")
        if (
            isinstance(expected_files, int)
            and not isinstance(expected_files, bool)
            and len(deliverables) != expected_files
        ):
            violations.append(
                DocumentationViolation(
                    "canonical_files",
                    "Canonical file count does not match EPIC.yaml structure: "
                    f"expected {expected_files}, found {len(deliverables)}.",
                    "EPIC.yaml",
                )
            )

        expected_controls = structure.get("control_documents")
        if isinstance(expected_controls, int) and not isinstance(expected_controls, bool):
            controls = [name for name in deliverables if not _NUMBERED_DOCUMENT.fullmatch(name)]
            if len(controls) != expected_controls:
                violations.append(
                    DocumentationViolation(
                        "control_documents",
                        "Control document count does not match EPIC.yaml structure: "
                        f"expected {expected_controls}, found {len(controls)}.",
                        "EPIC.yaml",
                    )
                )

        range_value = structure.get("canonical_document_range")
        if isinstance(range_value, str) and range_value != "none":
            match = re.fullmatch(r"(\d{2})-(\d{2})", range_value)
            if match is None:
                violations.append(
                    DocumentationViolation(
                        "canonical_range",
                        "canonical_document_range must use NN-NN or 'none'.",
                        "EPIC.yaml",
                    )
                )
            else:
                start, end = (int(match.group(1)), int(match.group(2)))
                expected_numbers = {f"{value:02d}" for value in range(start, end + 1)}
                actual_numbers = set(groups)
                missing = sorted(expected_numbers - actual_numbers)
                unexpected = sorted(actual_numbers - expected_numbers)
                if missing:
                    violations.append(
                        DocumentationViolation(
                            "canonical_range",
                            "Missing numbered chapters from canonical range: "
                            + ", ".join(missing),
                            "EPIC.yaml",
                        )
                    )
                if unexpected:
                    violations.append(
                        DocumentationViolation(
                            "canonical_range",
                            "Numbered chapters outside canonical range: "
                            + ", ".join(unexpected),
                            "EPIC.yaml",
                        )
                    )

    def _validate_markdown(
        self,
        files: tuple[Path, ...],
        root: Path,
        violations: list[DocumentationViolation],
    ) -> None:
        resolved_root = root.resolve()
        for path in files:
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                raise
            relative = path.relative_to(root).as_posix()
            self._validate_fences(text, relative, violations)
            self._validate_headings(text, relative, violations)
            self._validate_links(text, path, resolved_root, relative, violations)

    @staticmethod
    def _validate_fences(
        text: str,
        relative: str,
        violations: list[DocumentationViolation],
    ) -> None:
        active: str | None = None
        for line in text.splitlines():
            match = _FENCE.match(line)
            if match is None:
                continue
            token = match.group(1)
            marker = token[0]
            if active is None:
                active = marker
            elif active == marker:
                active = None
        if active is not None:
            violations.append(
                DocumentationViolation(
                    "markdown_fence",
                    "Markdown fenced code block is not closed.",
                    f"{relative}",
                )
            )

    @staticmethod
    def _validate_headings(
        text: str,
        relative: str,
        violations: list[DocumentationViolation],
    ) -> None:
        levels: list[tuple[int, int]] = []
        in_fence: str | None = None
        for line_number, line in enumerate(text.splitlines(), start=1):
            fence = _FENCE.match(line)
            if fence is not None:
                marker = fence.group(1)[0]
                if in_fence is None:
                    in_fence = marker
                elif in_fence == marker:
                    in_fence = None
                continue
            if in_fence is not None:
                continue
            heading = _HEADING.match(line)
            if heading is not None:
                levels.append((len(heading.group("marks")), line_number))

        h1_count = sum(level == 1 for level, _ in levels)
        if h1_count != 1:
            violations.append(
                DocumentationViolation(
                    "markdown_heading",
                    f"Markdown document must contain exactly one level-one heading; found {h1_count}.",
                    relative,
                )
            )

        previous = 0
        for level, line_number in levels:
            if previous and level > previous + 1:
                violations.append(
                    DocumentationViolation(
                        "markdown_heading",
                        f"Markdown heading level skips from {previous} to {level}.",
                        f"{relative}:{line_number}",
                    )
                )
            previous = level

    @staticmethod
    def _validate_links(
        text: str,
        path: Path,
        resolved_root: Path,
        relative: str,
        violations: list[DocumentationViolation],
    ) -> None:
        in_fence: str | None = None
        for line_number, line in enumerate(text.splitlines(), start=1):
            fence = _FENCE.match(line)
            if fence is not None:
                marker = fence.group(1)[0]
                if in_fence is None:
                    in_fence = marker
                elif in_fence == marker:
                    in_fence = None
                continue
            if in_fence is not None:
                continue
            for match in _MARKDOWN_LINK.finditer(line):
                raw_target = match.group("target").strip()
                if not raw_target or raw_target.startswith("#"):
                    continue
                split = urlsplit(raw_target)
                if split.scheme or split.netloc:
                    continue
                link_path = unquote(split.path)
                if not link_path:
                    continue
                candidate = (path.parent / link_path).resolve()
                if not candidate.is_relative_to(resolved_root) or not candidate.exists():
                    violations.append(
                        DocumentationViolation(
                            "broken_reference",
                            f"Local Markdown reference does not resolve: {raw_target}",
                            f"{relative}:{line_number}",
                        )
                    )
