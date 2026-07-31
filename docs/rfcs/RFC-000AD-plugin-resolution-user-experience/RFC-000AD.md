
RFC-000AD — Plugin Resolution User Experience
Status

Architecture Review

Summary

RFC-000AD defines the user experience for plugin resolution diagnostics in
FamilyOS CLI.

It transforms structured plugin resolution diagnostics into readable,
actionable terminal output while preserving Clean Architecture boundaries.

Accepted architecture
Plugin resolution application operation
        |
        v
PluginResolutionDiagnostic
        |
        v
ResolutionExplainer
        |
        v
ResolutionExplanation
        |
        v
TerminalFormatter
        |
        v
DiagnosticCliRenderer
        |
        v
CLI output boundary
        |
        v
Typer terminal output
Key decisions
Diagnostics remain framework-independent.
Typer remains confined to interfaces/cli.
TerminalFormatter builds terminal text.
DiagnosticCliRenderer is the CLI presentation adapter.
The renderer returns a string and does not print.
Commands coordinate application services and presentation.
CommandContext exposes application capabilities, not renderers.
ApplicationContainer does not construct CLI presentation objects.
Exit codes remain an interface policy.
DiagnosticPresentationService is rejected.
Rejected component

The proposed DiagnosticPresentationService is removed from the target design.

It provided no unique responsibility and introduced a circular dependency
between presentation and rendering.

Implemented foundations
AD.1 — Diagnostic CLI Renderer
AD.2 — Resolution Suggestion Model
AD.3 — Suggestion Generator
AD.4 — Terminal Formatter
Revised remaining sprints
AD.4R — Architecture correction
AD.5  — CLI Diagnostic Output Boundary
AD.6  — Plugin Resolution Command Integration
AD.7  — Exit Policy and Failure Aggregation
AD.8  — ANSI and Rich Terminal Styling
AD.9  — End-to-End Resolution UX
AD.10 — Public API and RFC Closure
Validation state

The architecture is not yet marked Accepted.

Before implementation resumes, the following must be confirmed:

removal of the rejected presentation-service implementation;
restoration of the last validated renderer architecture;
validation of the existing 99-test diagnostic baseline;
review of the concrete PluginResolutionPipeline input and output API;
identification of the CLI command that will expose resolution behavior.
Final acceptance criteria

RFC-000AD will be accepted when:

architecture review is validated;
all remaining sprints are implemented;
no circular imports exist;
CLI failure output is deterministic;
exit behavior is tested;
repository-wide MyPy, Ruff, and Pytest validation passes.
