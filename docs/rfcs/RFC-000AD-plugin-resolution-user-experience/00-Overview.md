# RFC-000AD — Plugin Resolution User Experience

## Status

Architecture Review

## Context

FamilyOS CLI provides a plugin ecosystem with discovery, dependency
resolution, conflict detection, cycle detection, diagnostic explanation,
formatting, and presentation components.

The diagnostic subsystem currently contains the foundations required to
transform plugin resolution failures into human-readable information.

The implemented flow includes:

```text
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
Terminal-compatible text
The subsystem also contains:

diagnostic severity and kind models;
diagnostic reports and builders;
conflict and dependency-cycle models;
diagnostic adapters;
explanation rules;
text and JSON explanation formatters;
resolution suggestions;
a suggestion generator;
a diagnostic pipeline.

The following components have already been implemented and validated:

AD.1 — Diagnostic CLI Renderer
AD.2 — Resolution Suggestion Model
AD.3 — Suggestion Generator
AD.4 — Terminal Formatter
Problem

The diagnostic subsystem is not yet integrated into the Typer command layer.

A previous design introduced a DiagnosticPresentationService between the
renderer and the terminal formatter. That design created an import cycle:

presentation
    |
    v
rendering
    |
    v
presentation

The service also duplicated responsibilities already owned by
DiagnosticCliRenderer.

The architecture must therefore be reviewed before any CLI integration is
implemented.

Decision summary

The target architecture does not include a diagnostic presentation service.

DiagnosticCliRenderer is the presentation adapter for terminal-oriented
diagnostic explanations.

TerminalFormatter owns terminal text construction.

Output remains the only existing general-purpose CLI helper directly coupled
to Typer.

Application services must not depend on Typer, Output, or terminal rendering.

The CLI command layer coordinates application services and presentation
adapters.

Goals

RFC-000AD must provide:

readable plugin resolution failures;
actionable resolution suggestions;
deterministic terminal formatting;
integration with the existing Typer CLI;
consistent CLI exit behavior;
testable boundaries between application logic and presentation;
future support for alternative renderers without changing domain models.
Non-goals

RFC-000AD does not implement:

plugin marketplace access;
remote registry communication;
plugin installation workflows;
package download progress;
interactive conflict resolution;
automatic dependency repair;
terminal user interfaces;
web or REST presentation;
plugin trust or sandboxing policies.
Architectural principles

The RFC follows these principles:

architecture before implementation;
dependencies point toward stable abstractions;
Typer remains confined to the CLI interface layer;
domain diagnostics contain no terminal concepts;
formatters do not execute application operations;
renderers do not resolve plugin dependencies;
commands remain thin coordinators;
no abstraction is introduced without a distinct responsibility;
public API additions are deliberate and tested.
Current RFC phase
Architecture Review
        |
        v
Design Challenge
        |
        v
Architecture Validation
        |
        v
Remaining Sprint Implementation

