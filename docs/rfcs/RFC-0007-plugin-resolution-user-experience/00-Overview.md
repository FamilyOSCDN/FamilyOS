# RFC-0007 — Plugin Resolution User Experience

## Status

Accepted

## Context

FamilyOS CLI provides a plugin ecosystem with discovery, dependency resolution,
conflict detection, cycle detection, diagnostic explanation, formatting, and
presentation components.

RFC-0007 defines how structured plugin resolution failures are transformed into
readable and actionable CLI diagnostics without introducing terminal framework
concerns into the ecosystem diagnostic model.

The accepted diagnostic flow is:

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
CLI output boundary
        |
        v
Typer terminal output
```

The diagnostic subsystem also contains:

- diagnostic severity and kind models;
- diagnostic reports and builders;
- conflict and dependency-cycle models;
- diagnostic adapters;
- explanation rules;
- text and JSON explanation formatters;
- resolution suggestions;
- a suggestion generator;
- a diagnostic pipeline.

---

## Problem

Plugin resolution diagnostics must cross from framework-independent ecosystem
logic into a Typer-based command-line interface.

That boundary must provide useful terminal output without allowing Typer,
terminal styling, process exit behavior, or other interface concerns to leak
into diagnostic models or application behavior.

An earlier design proposed a `DiagnosticPresentationService` between the
renderer and formatter.

That design was rejected because it duplicated existing responsibilities and
created an undesirable presentation dependency cycle.

---

## Decision

The accepted architecture does not contain a
`DiagnosticPresentationService`.

`DiagnosticCliRenderer` is the CLI-oriented presentation adapter for diagnostic
explanations.

`TerminalFormatter` owns deterministic terminal text construction.

`Output` remains the CLI output boundary directly coupled to Typer.

The CLI command layer coordinates application services and presentation
adapters.

Application and ecosystem diagnostic components do not depend on Typer,
`Output`, or CLI process-exit behavior.

---

## Dependency Direction

The accepted formatter and renderer dependency direction is:

```text
ResolutionExplanation
        |
        v
TerminalFormatter
        |
        v
DiagnosticCliRenderer
```

The complete interface flow is:

```text
Plugin resolution pipeline
        |
        v
Structured diagnostics
        |
        v
Diagnostic explanation
        |
        v
Diagnostic rendering
        |
        v
CLI output boundary
        |
        v
Typer
```

Dependencies do not point back from ecosystem diagnostics toward the CLI.

---

## Goals

RFC-0007 provides:

- readable plugin resolution failures;
- actionable resolution suggestions;
- deterministic terminal formatting;
- integration with the existing Typer CLI;
- consistent CLI exit behavior;
- testable boundaries between application logic and presentation;
- optional terminal styling;
- support for environments without color;
- future support for alternative renderers without changing diagnostic models.

---

## Non-goals

RFC-0007 does not implement:

- plugin marketplace access;
- remote registry communication;
- plugin installation workflows;
- package download progress;
- interactive conflict resolution;
- automatic dependency repair;
- terminal user interfaces;
- web or REST presentation;
- plugin trust or sandboxing policies.

---

## Architectural Principles

The RFC follows these principles:

- architecture before implementation;
- dependencies point toward stable abstractions;
- Typer remains confined to the CLI interface layer;
- domain and ecosystem diagnostics contain no terminal framework concepts;
- formatters do not execute application operations;
- renderers do not resolve plugin dependencies;
- commands remain thin coordinators;
- exit codes remain an interface policy;
- styling remains optional;
- plain-text output remains deterministic;
- no abstraction is introduced without a distinct responsibility;
- public API additions are deliberate and tested.

---

## Completed Decisions

The following architecture decisions are complete:

- AD.1 — Diagnostic CLI Renderer
- AD.2 — Resolution Suggestion Model
- AD.3 — Suggestion Generator
- AD.4 — Terminal Formatter
- AD.4R — Remove rejected `DiagnosticPresentationService` design
- AD.5 — CLI Diagnostic Output Boundary
- AD.6 — Plugin Resolution Command Integration
- AD.7 — Exit Policy and Failure Aggregation
- AD.8 — ANSI and Rich Terminal Styling
- AD.9 — End-to-End Resolution UX
- AD.10 — Public API and RFC Closure

---

## Validation

Final repository validation confirms:

```text
Ruff:   PASS
MyPy:   PASS — 527 source files
Pytest: PASS — 1253 tests

Typer in ecosystem diagnostics:
NONE

ecosystem diagnostics -> CLI dependency:
NONE

DiagnosticPresentationService:
NONE

Repository diff validation:
PASS
```

---

## Final RFC Phase

```text
Architecture Review
        |
        v
Design Challenge
        |
        v
Architecture Validation
        |
        v
Implementation
        |
        v
End-to-End Validation
        |
        v
Repository Validation
        |
        v
Accepted
```

RFC-0007 has completed this lifecycle.

**Status: Accepted**