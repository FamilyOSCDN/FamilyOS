
RFC-000AD — Target Architecture
Layers

The target architecture uses four relevant layers.

Domain and ecosystem diagnostics
        |
        v
Application orchestration
        |
        v
CLI presentation adapters
        |
        v
Typer terminal interface
Diagnostic domain and ecosystem layer

This layer contains structured diagnostic information.

Primary models include:

PluginResolutionDiagnostic
DiagnosticKind
DiagnosticSeverity
DiagnosticReport
ResolutionExplanation
ResolutionSuggestion

Responsibilities:

represent resolution failures and information;
preserve diagnostic details;
classify severity and diagnostic kind;
represent explanations;
represent suggested corrective actions.

This layer must not depend on:

Typer;
CLI commands;
terminal colors;
process exit codes;
stdout or stderr.
Explanation layer

The explanation layer transforms diagnostics into human-readable structured
explanations.

PluginResolutionDiagnostic
        |
        v
ResolutionExplainer
        |
        v
ExplanationRuleRegistry
        |
        v
ExplanationRule
        |
        v
ResolutionExplanation

Responsibilities:

select an explanation rule;
produce titles and summaries;
expose causes;
expose textual suggestions already supported by the explanation model;
provide deterministic fallback explanations.

The explanation layer does not render terminal output.

Suggestion layer

The suggestion layer creates explicit corrective-action models.

PluginResolutionDiagnostic
        |
        v
SuggestionGenerator
        |
        v
ResolutionSuggestion

Responsibilities:

map supported diagnostic kinds to corrective actions;
return immutable suggestions;
return no suggestion when no supported correction exists.

The suggestion generator must not modify diagnostics or execute repairs.

Formatting layer

TerminalFormatter owns terminal-oriented text construction.

ResolutionExplanation
        |
        v
TerminalFormatter
        |
        v
str

Responsibilities:

format the heading;
format the summary;
format causes;
format suggestions;
omit empty sections;
return deterministic text.

TerminalFormatter does not print output and does not depend on Typer.

Rendering layer

DiagnosticCliRenderer is the terminal presentation adapter.

ResolutionExplanation
        |
        v
DiagnosticCliRenderer
        |
        v
TerminalFormatter
        |
        v
str

Responsibilities:

accept a structured explanation;
delegate terminal formatting;
expose a stable rendering operation to the CLI layer.

The renderer does not:

call typer.echo or typer.secho;
choose exit codes;
execute plugin resolution;
generate diagnostics;
explain diagnostics;
install plugins.
Application layer

The application layer coordinates plugin resolution use cases.

The target application service must return structured resolution results rather
than terminal output.

Conceptual flow:

Plugin resolution request
        |
        v
Application service
        |
        v
PluginResolutionPipeline
        |
        v
Resolution result and diagnostics

Application services may depend on ecosystem models and ports.

Application services must not depend on:

DiagnosticCliRenderer;
TerminalFormatter;
Output;
Typer.
CLI layer

The CLI layer coordinates application execution and terminal presentation.

Typer command
        |
        +--> CommandContext
        |        |
        |        v
        |   Application service
        |
        +--> ResolutionExplainer
        |
        +--> DiagnosticCliRenderer
        |
        v
Output or Typer boundary

The command is allowed to combine application results with a CLI-specific
renderer because it belongs to the outer interface layer.

Dependency direction

Allowed dependencies:

CLI command
    -> application service
    -> ecosystem resolution models

CLI command
    -> diagnostic explainer
    -> diagnostic models

CLI command
    -> diagnostic renderer
    -> terminal formatter
    -> resolution explanation

Forbidden dependencies:

application service
    -X-> CLI command

application service
    -X-> Typer

diagnostic model
    -X-> TerminalFormatter

TerminalFormatter
    -X-> DiagnosticCliRenderer

DiagnosticCliRenderer
    -X-> Typer

presentation package
    -X-> rendering package
    -X-> presentation package
Composition

The existing ApplicationContainer remains responsible for application and
ecosystem services.

CLI-only renderers do not need to be exposed by CommandContext unless a
future requirement demonstrates a need for configurable renderer composition.

For RFC-000AD, the preferred composition is local to the CLI interface:

renderer = DiagnosticCliRenderer()

This keeps CommandContext focused on application services.

Target component diagram
+----------------------------------------------------------+
| Typer command                                            |
|                                                          |
|  +--------------------+      +-------------------------+  |
|  | CommandContext     |      | DiagnosticCliRenderer   |  |
|  +----------+---------+      +------------+------------+  |
|             |                             |               |
+-------------|-----------------------------|---------------+
              |                             |
              v                             v
+---------------------------+     +-------------------------+
| Application service       |     | TerminalFormatter       |
+-------------+-------------+     +------------+------------+
              |                                |
              v                                v
+---------------------------+     +-------------------------+
| PluginResolutionPipeline  |     | ResolutionExplanation   |
+-------------+-------------+     +-------------------------+
              |
              v
+---------------------------+
| Resolution diagnostics    |
+---------------------------+
