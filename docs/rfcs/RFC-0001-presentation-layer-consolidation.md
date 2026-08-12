# RFC-0001 — Presentation Layer Consolidation

| Field | Value |
|---|---|
| RFC | RFC-0001 |
| Title | Presentation Layer Consolidation |
| Status | Accepted |
| Authors | FamilyOS Architecture Team |
| Created | 2026-07-28 |
| Updated | 2026-08-12 |
| Target Release | Architecture Baseline |
| Supersedes | None |
| Superseded By | None |

---

# Executive Summary

RFC-0001 defines the consolidated presentation architecture for FamilyOS.

FamilyOS already contained the essential presentation-layer building blocks:

- CLI application;
- command implementations;
- command context;
- output helpers;
- centralized error handling.

The objective of this RFC is not to introduce a new presentation framework.

Instead, it formalizes how presentation components collaborate with the
application layer and establishes clear responsibility boundaries between
external interfaces, application orchestration, domain behavior, and
user-facing output.

The implementation has now converged on this architecture.

Presentation components receive and translate external input, invoke
application capabilities, and present results.

Application orchestration is kept outside presentation components.

The architecture preserves the existing Typer-based CLI while allowing future
interfaces to follow the same principles.

---

# Context

FamilyOS has evolved from a command-line application into a
specification-driven platform with generation, plugin, runtime, validation, and
diagnostic capabilities.

During the original architecture assessment, FamilyOS already provided:

- a centralized CLI entry point;
- shared command context;
- common output helpers;
- centralized error handling;
- application use cases;
- dependency-injection composition through the application container.

These components collectively formed a presentation layer, but their use was
not initially consistent.

Some commands delegated directly to application use cases.

Other commands:

- instantiated application services directly;
- manipulated domain value objects;
- constructed plugin resolution models;
- performed application orchestration;
- mixed output responsibilities with resolution behavior.

That inconsistency motivated this RFC.

---

# Architecture Assessment

## Existing Presentation Components

The FamilyOS presentation layer contains the following primary components:

- `interfaces.cli.app`;
- CLI command modules;
- `CommandContext`;
- `BaseCommand`;
- `Output`;
- `ErrorHandler`;
- Typer command groups and command wrappers.

These components provide the interface boundary between users and application
capabilities.

## Application Composition

Application dependencies are composed by:

```text
ApplicationFactory
        |
        v
ApplicationContainer
        |
        v
Application services and use cases
```

The composition root may depend on concrete infrastructure, domain, runtime,
and plugin implementations.

Presentation code should consume the resulting application capabilities rather
than reproduce composition logic.

## Original Responsibility Distribution

The original CLI contained multiple command styles.

Some commands used:

```text
Command
    |
    v
BaseCommand
    |
    v
CommandContext
    |
    v
Application Use Case
```

Other commands instantiated or manipulated lower-level application and domain
components directly.

This produced inconsistent dependency directions.

---

# Problem Statement

The problem addressed by RFC-0001 is not the absence of a presentation layer.

The problem is the absence of a consistent architectural contract defining:

- what presentation components may do;
- where application orchestration belongs;
- how commands access application capabilities;
- where input normalization occurs;
- where output formatting occurs;
- how interface-specific behavior remains isolated;
- how future interfaces can reuse the same application capabilities.

Without these boundaries, presentation code can gradually absorb domain and
application responsibilities.

---

# Decision Drivers

The primary decision drivers are:

- consistency;
- maintainability;
- architectural clarity;
- testability;
- separation of responsibilities;
- incremental migration;
- preservation of existing CLI behavior.

Performance is not a primary driver.

Security behavior is not redefined by this RFC.

Backward compatibility should be preserved wherever practical.

---

# Goals

RFC-0001 establishes the following goals:

- define a unified presentation architecture;
- consolidate existing presentation responsibilities;
- minimize application orchestration inside presentation components;
- prevent presentation components from constructing domain behavior directly;
- standardize access to application capabilities;
- centralize user-facing output behavior;
- preserve thin command wrappers;
- maintain deterministic and testable presentation behavior;
- prepare FamilyOS for additional presentation interfaces;
- preserve the existing CLI user experience.

---

# Non-Goals

RFC-0001 does not:

- redesign the domain layer;
- redesign the plugin runtime;
- redesign the generation engine;
- introduce REST or web interfaces;
- replace Typer;
- redefine dependency injection;
- redefine plugin resolution semantics;
- redefine plugin diagnostic semantics;
- introduce a new presentation framework.

Those concerns remain governed by their respective architecture documents,
RFCs, ADRs, and implementation layers.

---

# Architectural Decision

FamilyOS shall maintain an explicit presentation layer responsible for
interface concerns only.

Presentation components are responsible for:

- receiving external requests;
- validating interface-level syntax where appropriate;
- translating primitive external input into application requests;
- invoking application use cases and application services;
- presenting application results;
- translating expected application failures into interface behavior;
- choosing interface-specific output and exit policies.

Presentation components shall not own:

- domain business rules;
- application orchestration;
- dependency resolution algorithms;
- domain object lifecycle;
- generation planning;
- plugin repository construction when part of an application operation;
- dependency graph construction;
- infrastructure composition.

---

# Proposed and Accepted Design

The accepted presentation flow is:

```text
External Interface
        |
        v
Command / Controller
        |
        v
Presentation Context
        |
        v
Application Use Case / Service
        |
        v
Application Result
        |
        v
Presenter / Output Boundary
        |
        v
External User
```

For FamilyOS CLI:

```text
Typer
        |
        v
CLI Command
        |
        v
CommandContext
        |
        v
ApplicationContainer
        |
        v
Application Use Case / Service
```

The composition root remains outside the presentation responsibility:

```text
Bootstrap
   |
   +--> Application
   +--> Domain
   +--> Infrastructure
   +--> Plugin implementations
   |
   v
ApplicationContainer
```

This dependency is allowed because bootstrap is the composition root.

---

# Presentation Context

`CommandContext` is the shared access point between CLI commands and
application capabilities.

Its responsibilities are limited to:

- obtaining application services and use cases from the application container;
- exposing those capabilities through stable presentation-facing properties;
- caching command-scoped access where appropriate.

`CommandContext` does not implement business logic.

It does not construct domain models for command-specific operations.

It does not replace the application container.

Example dependency direction:

```text
CLI Command
    |
    v
CommandContext
    |
    v
ApplicationContainer
    |
    v
ResolvePluginsUseCase
```

---

# Command Model

Commands should remain thin.

A command may:

1. receive CLI arguments and options;
2. resolve an application capability through `CommandContext`;
3. invoke that capability;
4. translate the result into CLI output;
5. apply CLI-specific exit behavior.

Commands should not replicate application orchestration.

Two implementation styles are acceptable where appropriate:

```text
Typer wrapper
    |
    v
Command class
    |
    v
BaseCommand
```

and:

```text
Typer wrapper / thin command function
    |
    v
CommandContext
```

`BaseCommand` is a convenience abstraction, not a mandatory superclass for
every command.

Architectural consistency is defined by responsibility boundaries, not by
inheritance.

---

# Application Boundary

The application layer owns orchestration.

Presentation input may arrive as primitives such as:

- strings;
- paths;
- flags;
- option values;
- lists of dependency expressions.

The application layer may normalize those values into domain or ecosystem
models when that normalization is part of the application operation.

For example:

```text
CLI
preset: str | None
        |
        v
CreateDomainUseCase
        |
        v
GenerationPresetId
        |
        v
GenerationRequestFactory
```

The CLI therefore does not need to construct `GenerationPresetId`.

---

# Plugin Resolution Boundary

Plugin resolution originally required the CLI to know:

- `PluginRepository`;
- `PluginDependency`;
- `ConstraintSet`;
- `PluginId`;
- `PluginResolutionPipeline`.

That orchestration has been moved behind:

```text
ResolvePluginsUseCase
```

The accepted flow is:

```text
CLI primitive input
        |
        v
ResolvePluginsUseCase
        |
        +--> validate canonical Plugin IDs
        +--> parse version constraints
        +--> construct repository
        +--> construct dependencies
        +--> invoke PluginResolutionPipeline
        |
        v
ResolutionPlan
```

The CLI no longer owns plugin resolution construction.

---

# Diagnostic Presentation Boundary

RFC-0007 defines the plugin resolution diagnostic presentation architecture.

RFC-0001 does not override that decision.

The accepted diagnostic presentation flow remains:

```text
ResolutionPlan
        |
        v
DiagnosticPipeline
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
Output
```

These components are used from the CLI because they form the accepted
presentation path for plugin resolution diagnostics.

Their presence does not mean that plugin resolution orchestration belongs to
the presentation layer.

The distinction is:

```text
Resolution orchestration
    -> application responsibility

Diagnostic presentation
    -> presentation responsibility
```

---

# Output Boundary

`Output` provides consistent user-facing CLI output.

Supported output responsibilities include:

- success messages;
- error messages;
- warnings;
- informational messages;
- rendered multiline diagnostics;
- optional terminal styling.

The output boundary owns Typer-specific rendering behavior.

Domain and application code do not depend on `Output`.

---

# Error Handling

`ErrorHandler` provides centralized translation of expected FamilyOS errors
into CLI behavior.

Typical flow:

```text
Application
    |
    v
FamilyOSError
    |
    v
ErrorHandler
    |
    +--> Output.error(...)
    |
    v
Typer exit policy
```

Not every expected failure must use `FamilyOSError`.

Some application capabilities may expose explicit result or status semantics.

CLI exit behavior remains an interface responsibility.

---

# Dependency Rules

The following dependency direction is accepted:

```text
interfaces
    |
    v
application
    |
    v
domain / application ports
```

Bootstrap may depend on all concrete layers required for composition.

The following direction is prohibited for normal application behavior:

```text
domain
    |
    X
    v
interfaces
```

and:

```text
application
    |
    X
    v
interfaces
```

Typer remains confined to the CLI interface layer.

---

# Implementation Consolidation

RFC-0001 consolidation included the following corrections.

## Legacy Package-Level Command Removal

A legacy `init()` implementation remained in:

```text
interfaces/cli/commands/__init__.py
```

It directly constructed `CreateProjectUseCase`.

The duplicate implementation was removed.

The canonical command path is:

```text
app.py
    |
    v
commands/init.py
    |
    v
InitCommand
    |
    v
CommandContext
```

## Domain Preset Normalization

`create_domain.py` previously constructed `GenerationPresetId` directly.

Normalization was moved behind the application boundary.

The CLI now passes primitive preset input to `CreateDomainUseCase`.

## Plugin Resolution Orchestration

`plugin_resolve.py` previously:

- parsed dependency expressions;
- validated canonical plugin identifiers;
- created `PluginRepository`;
- created `PluginDependency`;
- parsed `ConstraintSet`;
- invoked `PluginResolutionPipeline`.

Those responsibilities were moved into `ResolvePluginsUseCase`.

The CLI now delegates the application operation and retains only presentation
responsibilities.

---

# Testing Strategy

Presentation consolidation is validated through:

- unit tests for CLI commands;
- unit tests for `CommandContext`;
- application use-case tests;
- output tests;
- error-handler tests;
- integration tests;
- end-to-end CLI tests;
- static architecture audits;
- Ruff;
- MyPy;
- repository-wide Pytest.

Specific regression coverage exists for:

- project initialization;
- artifact creation;
- domain creation;
- preset normalization;
- generation catalog commands;
- plugin resolution;
- plugin resolution failures;
- plugin diagnostics;
- CLI exit codes.

---

# Validation

The RFC-0001 consolidation work confirmed:

```text
CLI direct domain imports
PASS: none

Direct use-case construction in CLI
PASS: none

CLI plugin resolution construction
PASS: removed

CLI tests
34 passed

CLI Ruff
All checks passed

Working tree after implementation commits
clean
```

The plugin diagnostic presentation import remains intentionally present in
`plugin_resolve.py` because it implements the presentation architecture
accepted by RFC-0007.

Repository-wide quality gates had also previously validated the current
baseline with:

```text
Ruff
All checks passed

MyPy
Success: no issues found in 527 source files

Pytest
1253 passed
```

---

# Consequences

## Positive Consequences

The accepted architecture provides:

- thinner CLI commands;
- clearer application boundaries;
- less domain knowledge in presentation components;
- centralized application access through `CommandContext`;
- easier command testing;
- easier introduction of future interfaces;
- reduced duplication;
- explicit separation between orchestration and presentation;
- preserved RFC-0007 diagnostic architecture.

## Trade-Offs

Some presentation commands still interact with application-facing result
models.

This is acceptable where those models represent the result of the application
operation and do not cause the CLI to reproduce domain behavior.

`BaseCommand` is not required everywhere.

A forced migration of every command to inheritance would increase complexity
without improving architectural boundaries.

---

# Alternatives Considered

## Mandatory BaseCommand Inheritance

Rejected.

Architectural consistency should be based on responsibility boundaries rather
than requiring every command to inherit from a common base class.

## Presentation Service Layer

Rejected as a universal requirement.

Additional presentation services should only be introduced when they own a
distinct responsibility.

RFC-0007 specifically rejected a redundant
`DiagnosticPresentationService`.

## Direct Construction in Commands

Rejected.

Commands should not directly construct application use cases or reproduce
application composition.

## Move Diagnostic Rendering into Application

Rejected.

Terminal diagnostic rendering is a presentation responsibility and remains in
the CLI-facing architecture defined by RFC-0007.

---

# Future Evolution

Future interfaces may include:

- REST APIs;
- web applications;
- desktop clients;
- automation adapters.

Those interfaces should reuse application capabilities while implementing
their own presentation concerns.

For example:

```text
REST Controller
      |
      v
Application Use Case
      |
      v
REST Presenter
```

The addition of new interfaces must not require moving business rules into
presentation code.

---

# Acceptance Criteria

RFC-0001 is accepted because:

- a unified presentation responsibility model is defined;
- application composition is centralized;
- commands no longer instantiate application use cases directly;
- direct CLI-to-domain dependency identified during the audit was removed;
- plugin resolution orchestration was moved behind an application use case;
- CLI-specific diagnostic presentation remains isolated from application
  orchestration;
- `CommandContext` exposes application capabilities;
- output behavior is centralized;
- expected error behavior has a shared boundary;
- targeted CLI and application tests pass;
- Ruff validation passes;
- MyPy validation passes for the modified application boundary;
- the working tree is clean after implementation commits.

---

# Final Decision

FamilyOS adopts the presentation architecture defined by RFC-0001.

The presentation layer is an explicit architectural boundary.

Commands and controllers translate external requests, invoke application
capabilities, and present results.

Application orchestration remains outside presentation components.

Domain and infrastructure behavior remain outside the presentation layer.

Bootstrap remains responsible for concrete application composition.

RFC-0007 remains authoritative for plugin resolution diagnostic presentation.

---

# Final State

RFC-0001 — Presentation Layer Consolidation is complete.

**Status: Accepted**