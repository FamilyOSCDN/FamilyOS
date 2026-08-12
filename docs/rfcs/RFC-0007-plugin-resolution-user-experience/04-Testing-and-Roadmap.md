# RFC-0007 — Testing Strategy and Roadmap

## Status

Accepted

## Testing Strategy

RFC-0007 uses layered testing from diagnostic models through real CLI
execution.

---

## Model Tests

Models are tested independently.

Covered models include:

- `PluginResolutionDiagnostic`;
- `DiagnosticReport`;
- `ResolutionExplanation`;
- `ResolutionSuggestion`;
- conflict models;
- dependency-cycle models.

Tests verify:

- immutability where required;
- defaults;
- severity helpers;
- diagnostic classification;
- empty and non-empty behavior.

---

## Explanation Tests

Explanation rules and registries verify:

- supported diagnostic matching;
- fallback behavior;
- titles;
- summaries;
- causes;
- suggestions;
- deterministic rule selection.

---

## Suggestion Tests

`SuggestionGenerator` tests verify:

- missing dependency suggestions;
- dependency-cycle suggestions;
- version-conflict suggestions;
- unsupported diagnostic behavior.

---

## Formatting Tests

`TerminalFormatter` tests verify:

- complete explanations;
- summary-only output;
- omitted causes;
- omitted suggestions;
- multiple causes;
- multiple suggestions;
- exact newline behavior;
- deterministic plain-text formatting.

---

## Renderer Tests

`DiagnosticCliRenderer` tests verify:

- delegation to terminal formatting;
- deterministic rendered output;
- framework independence;
- formatter boundaries.

---

## CLI Output Tests

`Output` tests verify:

- raw diagnostic output;
- stderr behavior;
- no generic diagnostic prefix;
- multiline preservation;
- optional styling behavior;
- deterministic plain-text behavior;
- support for output without color.

---

## Command Tests

Command tests verify:

- canonical dependency parsing;
- rejection of non-canonical plugin identifiers;
- success output;
- diagnostic failure output;
- failure exit policy;
- expected application interactions;
- diagnostic pipeline integration;
- no duplicated formatting responsibility.

---

## End-to-End Tests

End-to-end plugin resolution tests cover the primary CLI scenarios, including:

- successful resolution;
- missing dependency;
- version conflict;
- invalid or non-canonical plugin identifier.

Failure scenarios verify:

- real command invocation;
- terminal diagnostic output;
- process exit code;
- actionable suggestions where applicable;
- absence of traceback.

Plugin ecosystem integration coverage additionally validates lifecycle behavior
across:

```text
Discovery
    |
    v
Resolution
    |
    v
Verification
    |
    v
Installation
    |
    v
Runtime activation
```

Canonical plugin identity is preserved across these boundaries.

---

## Quality Gates

RFC-0007 requires repository-wide validation before closure.

Final validation completed successfully:

```text
ruff check .
All checks passed.

mypy src
Success: no issues found in 527 source files

pytest -q
1253 passed in 1.04s
```

Architecture boundary validation also completed successfully:

```text
PASS: Typer absent from ecosystem diagnostics
PASS: diagnostics do not import CLI
PASS: no rejected presentation service
```

Repository integrity validation completed successfully:

```text
git diff --check
PASS

git diff --cached --check
PASS

working tree before closure
clean
```

---

## Completed Roadmap

### AD.1 — Diagnostic CLI Renderer

Status: **Completed**

Provides the CLI-oriented rendering adapter for resolution explanations.

### AD.2 — Resolution Suggestion Model

Status: **Completed**

Provides structured actionable resolution suggestions.

### AD.3 — Suggestion Generator

Status: **Completed**

Generates suggestions for supported plugin resolution failures.

### AD.4 — Terminal Formatter

Status: **Completed**

Provides deterministic terminal-oriented diagnostic text.

### AD.4R — Architecture Correction

Status: **Completed**

The rejected `DiagnosticPresentationService` design was removed from the
target architecture.

The accepted dependency direction is:

```text
ResolutionExplanation
        |
        v
TerminalFormatter
        |
        v
DiagnosticCliRenderer
```

No rejected presentation service remains in the repository.

### AD.5 — CLI Diagnostic Output Boundary

Status: **Completed**

Implemented responsibilities:

- raw multiline diagnostic output through the CLI output boundary;
- stderr behavior;
- focused unit coverage;
- separation from resolution logic.

### AD.6 — Plugin Resolution Command Integration

Status: **Completed**

Implemented responsibilities:

- plugin resolution exposed through the CLI;
- canonical dependency parsing;
- application resolution capability accessed through `CommandContext`;
- structured diagnostics explained and rendered;
- thin command coordination preserved.

### AD.7 — Exit Policy and Failure Aggregation

Status: **Completed**

Implemented responsibilities:

- CLI failure policy defined;
- rendered diagnostics handled consistently;
- deterministic diagnostic behavior preserved;
- plugin resolution failures return exit code `1`;
- successful resolution returns exit code `0`.

### AD.8 — ANSI and Rich Terminal Styling

Status: **Completed**

Implemented responsibilities:

- optional diagnostic styling;
- no diagnostic model changes;
- deterministic plain-text tests preserved;
- environments without color supported;
- no `DiagnosticPresentationService` introduced.

### AD.9 — End-to-End Resolution UX

Status: **Completed**

Implemented responsibilities:

- real CLI command execution validated;
- successful resolution covered;
- primary failure scenarios covered;
- terminal output verified;
- exit codes verified;
- expected resolution failures produce no traceback.

### AD.10 — Public API and RFC Closure

Status: **Completed**

Completed responsibilities:

- package exports reviewed;
- rejected component absence verified;
- import boundaries validated;
- Typer isolation validated;
- repository-wide quality checks completed;
- RFC status updated to `Accepted`.

---

## Completion Criteria

RFC-0007 completion criteria are satisfied:

- plugin resolution failures are readable in the CLI;
- suggestions are actionable;
- Typer remains outside ecosystem diagnostics;
- no circular dependency exists;
- no rejected presentation service remains;
- exit behavior is tested;
- end-to-end scenarios pass;
- optional styling preserves deterministic plain text;
- MyPy is green for the complete source tree;
- Ruff is green for the complete repository;
- Pytest is green for the complete repository.

---

## Final Validation Snapshot

```text
MyPy
527 source files validated

Ruff
All checks passed

Pytest
1253 passed

Architecture
Typer leak: none
diagnostics -> CLI dependency: none
rejected presentation service: none

Repository
diff checks: clean
working tree before closure: clean
```

---

## Final State

All RFC-0007 architecture decisions are complete.

RFC-0007 — Plugin Resolution User Experience is **Accepted**.