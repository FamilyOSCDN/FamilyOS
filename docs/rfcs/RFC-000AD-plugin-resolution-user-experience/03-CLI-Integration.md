
RFC-000AD — CLI Integration
Existing CLI conventions

The current CLI follows this structure:

Typer application
        |
        v
Command function
        |
        v
CommandContext
        |
        v
ApplicationContainer
        |
        v
Application use case or service

Output centralizes common Typer output behavior.

ErrorHandler converts FamilyOSError exceptions into CLI error output and a
process exit code.

Integration objective

Plugin resolution commands must display structured diagnostics without moving
Typer into the diagnostics subsystem.

The preferred command flow is:

1. Build or receive a plugin resolution request.
2. Execute the application operation.
3. Inspect the structured result.
4. Explain each relevant diagnostic.
5. Render each explanation.
6. Send rendered output to the terminal.
7. Return or raise the correct CLI exit status.
Command responsibility

The command owns interface coordination.

It may:

obtain application dependencies from CommandContext;
create a CLI renderer;
render application diagnostics;
write to stderr;
choose a Typer exit code.

It must not:

resolve dependency constraints itself;
inspect graph internals;
generate explanation text manually;
build terminal sections manually;
install missing plugins automatically.
Output transport

Rendered diagnostic output must not receive an additional generic error prefix.

For example, this is incorrect:

❌ ERROR: Missing plugin dependency

when the renderer already produces:

ERROR: Missing plugin dependency

The CLI therefore needs a raw output operation or a dedicated diagnostic output
operation.

Conceptual API:

Output.diagnostic(rendered_text)

Expected behavior:

write the text unchanged;
write to stderr;
avoid adding an icon or prefix;
preserve multiline formatting.
Exit behavior

Initial exit-code policy:

0 — command completed successfully
1 — plugin resolution failed
2 — invalid CLI usage, managed by Typer

More granular exit codes are deferred until a concrete automation requirement
exists.

Error separation

FamilyOSError and plugin resolution diagnostics represent different failure
channels.

FamilyOSError
    -> ErrorHandler
    -> generic CLI error
    -> exit code 1

Plugin resolution failure result
    -> ResolutionExplainer
    -> DiagnosticCliRenderer
    -> diagnostic terminal output
    -> exit code 1

A structured resolution failure should not be converted into a
FamilyOSError merely for display.

CommandContext policy

CommandContext may expose the existing plugin resolution application
capability when a CLI command requires it.

It must not expose:

TerminalFormatter;
DiagnosticCliRenderer;
Typer objects;
Output.
Bootstrap policy

ApplicationContainer may expose:

PluginResolutionPipeline;
future resolution use cases;
future application orchestration services.

It must not construct CLI presentation objects.

Testing boundaries

CLI integration tests must verify:

successful command output;
rendered missing-dependency output;
rendered version-conflict output;
rendered dependency-cycle output;
stderr usage;
exit code 1 for resolution failure;
absence of duplicate prefixes;
no Python traceback for expected resolution failures.
Deferred capabilities

The following remain outside the initial Typer integration:

ANSI style selection;
--output json;
--no-color;
interactive correction;
automated installation;
detailed exit-code taxonomy;
multiple diagnostics aggregation layout.

These may be introduced by later sprints after the basic integration is stable.
