
RFC-000AD — Design Challenge
Purpose

This document challenges the proposed architecture before implementation.

The goal is to identify unnecessary abstractions, invalid dependency
directions, unstable APIs, and future maintenance risks.

Rejected design: DiagnosticPresentationService

A previous design introduced:

DiagnosticCliRenderer
        |
        v
DiagnosticPresentationService
        |
        v
TerminalFormatter

Another variation inverted the relationship:

DiagnosticPresentationService
        |
        v
DiagnosticCliRenderer
        |
        v
TerminalFormatter

Both variants failed the design review.

Problems

The service had no independent responsibility.

Its only operation delegated to either the renderer or formatter.

It introduced additional composition and public API surface.

One implementation produced a circular package dependency:

presentation
    |
    v
rendering
    |
    v
presentation
Decision

DiagnosticPresentationService is rejected from the target architecture.

The renderer already represents the CLI presentation boundary.

Challenge: Should the renderer depend on Typer?
Option A
DiagnosticCliRenderer -> typer.secho

Advantages:

direct output;
fewer calls in commands.

Disadvantages:

renderer becomes difficult to reuse;
terminal formatting and output transport become coupled;
tests require Typer output capture;
renderer cannot be used to build a message before output;
ecosystem diagnostics gain an indirect dependency on the CLI framework.
Option B
DiagnosticCliRenderer -> str
CLI command -> Output or Typer

Advantages:

deterministic unit tests;
renderer remains framework-independent;
CLI controls stderr and exit behavior;
alternative interfaces can reuse explanations;
Typer remains confined to interfaces/cli.
Decision

Option B is accepted.

Challenge: Should CommandContext expose the renderer?
Option A
CommandContext.diagnostic_renderer

Advantages:

centralized construction;
replaceable renderer.

Disadvantages:

CommandContext currently exposes application services;
a presentation adapter would blur its responsibility;
no configuration requirement currently exists;
renderer construction is inexpensive.
Option B

Construct the renderer in the CLI command or a CLI-specific command object.

Advantages:

correct layer ownership;
no bootstrap pollution;
no new application dependency;
simpler implementation.
Decision

Option B is accepted for RFC-000AD.

Renderer injection may be reconsidered only when a concrete requirement
exists, such as selectable output formats or application-wide presentation
configuration.

Challenge: Should suggestions be strings or models?

ResolutionExplanation currently exposes textual suggestions, while
ResolutionSuggestion provides an explicit suggestion model.

This creates possible duplication.

Risks
two sources of suggestions;
disagreement between explanation rules and suggestion generator;
renderer receiving strings while suggestion services return models;
unclear ownership of suggestion generation.
Decision for the remaining RFC

No immediate migration is performed during CLI integration.

The current APIs remain stable while AD.5 focuses on boundary integration.

A later dedicated sprint must decide whether:

explanation rules remain the sole source of textual suggestions;
SuggestionGenerator enriches explanations;
ResolutionExplanation migrates to
tuple[ResolutionSuggestion, ...].

This decision must not be hidden inside a Typer integration sprint.

Challenge: Should exit codes belong to diagnostics?
Rejected design

Adding process exit codes directly to PluginResolutionDiagnostic.

Reason

Exit codes are interface policy, not diagnostic domain data.

The same diagnostic may be exposed through:

CLI;
JSON API;
TUI;
logs;
tests.
Decision

Exit-code mapping belongs to the CLI interface layer.

Challenge: Should Output format diagnostics?

Output currently provides generic success, error, warning, and information
helpers.

Embedding full diagnostic section construction inside Output would duplicate
TerminalFormatter.

Decision

Output may transport an already rendered diagnostic string.

It must not rebuild diagnostic explanations.

Challenge: Is a new application service required?

A service is justified only when the CLI needs an application operation not
already represented by PluginResolutionPipeline.

Before implementation, the actual pipeline input and result types must be
reviewed.

Possible outcomes:

reuse the existing pipeline directly through CommandContext;
add a small application use case if command-level orchestration is otherwise
duplicated;
avoid a new service if it would only proxy one pipeline call.
Validation rule

No new application service is accepted without:

a distinct input model;
a distinct output model;
orchestration beyond simple delegation;
tests demonstrating its responsibility.
Final challenged architecture
Application services and plugin resolution pipeline
                         |
                         v
                Structured diagnostics
                         |
                         v
              ResolutionExplainer
                         |
                         v
             ResolutionExplanation
                         |
                         v
             DiagnosticCliRenderer
                         |
                         v
                 Rendered string
                         |
                         v
               CLI Output / Typer
Design review conclusion

The architecture is accepted with the following conditions:

no DiagnosticPresentationService;
no Typer dependency in ecosystem diagnostics;
no renderer in application services;
no exit codes in domain diagnostics;
no suggestion model migration during basic CLI integration;
no new application service without demonstrated orchestration value.
