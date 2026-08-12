
RFC-0007 — Testing Strategy and Roadmap
Testing strategy

RFC-0007 uses layered tests.

Model tests

Models must be tested independently.

Covered models include:

PluginResolutionDiagnostic;
DiagnosticReport;
ResolutionExplanation;
ResolutionSuggestion;
conflict models;
dependency-cycle models.

Tests verify:

immutability where required;
defaults;
severity helpers;
diagnostic classification;
empty and non-empty behavior.
Explanation tests

Explanation rules and registries must verify:

supported diagnostic matching;
fallback behavior;
titles;
summaries;
causes;
suggestions;
deterministic rule selection.
Suggestion tests

SuggestionGenerator tests must verify:

missing dependency suggestions;
dependency-cycle suggestions;
version-conflict suggestions;
unsupported diagnostic behavior.
Formatting tests

TerminalFormatter tests must verify:

complete explanations;
summary-only output;
omitted causes;
omitted suggestions;
multiple causes;
multiple suggestions;
exact newline behavior.
Renderer tests

DiagnosticCliRenderer tests must verify:

delegation to terminal formatting;
deterministic rendered output;
framework independence;
custom formatter injection if retained by the implementation.
CLI output tests

Output tests must verify:

raw diagnostic output;
stderr behavior;
no generic prefix;
multiline preservation.
Command tests

Command tests must verify:

success output;
diagnostic failure output;
failure exit code;
expected application interactions;
no duplicated formatting responsibility.
End-to-end tests

End-to-end tests must cover at least:

Successful resolution
Missing dependency
Version conflict
Dependency cycle

Each failure case must verify:

command invocation;
terminal output;
process exit code;
absence of traceback.
Quality gates

Every implementation sprint must pass:

mypy src/familyos_cli

ruff check \
    src/familyos_cli \
    tests

pytest tests -q

Focused validation may be run during development, but the RFC cannot close
without the complete repository validation.

Revised roadmap
Completed
AD.1 — Diagnostic CLI Renderer
AD.2 — Resolution Suggestion Model
AD.3 — Suggestion Generator
AD.4 — Terminal Formatter
Architecture correction
AD.4R — Remove rejected DiagnosticPresentationService design

This correction restores the validated AD.4 dependency direction:

ResolutionExplanation
        |
        v
TerminalFormatter
        |
        v
DiagnosticCliRenderer
Remaining implementation
AD.5 — CLI Diagnostic Output Boundary
AD.6 — Plugin Resolution Command Integration
AD.7 — Exit Policy and Failure Aggregation
AD.8 — ANSI and Rich Terminal Styling
AD.9 — End-to-End Resolution UX
AD.10 — Public API and RFC Closure
Sprint AD.5 — CLI Diagnostic Output Boundary

Responsibilities:

add raw multiline diagnostic output to the CLI output boundary;
preserve stderr behavior;
add focused unit tests;
avoid plugin-resolution command changes.

Expected files:

src/familyos_cli/interfaces/cli/output.py
tests/unit/interfaces/cli/test_output.py
Sprint AD.6 — Plugin Resolution Command Integration

Responsibilities:

expose the required application resolution capability;
create or update the relevant command;
explain and render structured diagnostics;
preserve thin-command design.

The exact files depend on the selected plugin resolution command and existing
pipeline input API.

Sprint AD.7 — Exit Policy and Failure Aggregation

Responsibilities:

define CLI failure policy;
aggregate multiple rendered diagnostics;
ensure stable ordering;
return exit code 1 for resolution failures.
Sprint AD.8 — ANSI and Rich Terminal Styling

Responsibilities:

introduce optional styling without changing diagnostic models;
preserve plain-text deterministic tests;
support environments without color.

This sprint must not require a DiagnosticPresentationService.

Sprint AD.9 — End-to-End Resolution UX

Responsibilities:

validate real command execution;
cover success and primary failure kinds;
verify output and exit codes;
eliminate tracebacks for expected resolution failures.
Sprint AD.10 — Public API and RFC Closure

Responsibilities:

review package exports;
remove rejected or unused components;
validate import boundaries;
run repository-wide quality checks;
update RFC status to Accepted or Implemented.
Completion criteria

RFC-0007 is complete when:

plugin resolution failures are readable in the CLI;
suggestions are actionable;
Typer remains outside ecosystem diagnostics;
no circular dependency exists;
no rejected presentation service remains;
exit behavior is tested;
end-to-end scenarios pass;
MyPy, Ruff, and Pytest are green for the complete repository.
