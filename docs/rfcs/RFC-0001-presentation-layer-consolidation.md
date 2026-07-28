# RFC-0001: Presentation Layer Consolidation

| Field | Value |
|------|------|
| RFC | RFC-0001 |
| Title | Presentation Layer Consolidation |
| Status | Draft |
| Authors | FamilyOS Architecture Team |
| Created | 2026-07-28 |
| Updated | 2026-07-28 |
| Target Release | TBD |
| Supersedes | None |
| Superseded By | None |

---

# Executive Summary

This RFC proposes the consolidation of the FamilyOS Presentation Layer.

The architectural review identified that a presentation layer already exists
through the combination of CLI commands, command context, output helpers and
error handling. However, presentation responsibilities are currently
distributed across multiple components and command implementations are not
fully consistent.

The objective of this RFC is not to introduce a new presentation layer.

Instead, it defines a common architectural direction that consolidates the
existing presentation components into a coherent and maintainable model.

The proposed architecture separates presentation from application
orchestration while preserving the existing user experience and allowing an
incremental migration.

---

# Context

FamilyOS has progressively evolved from a command-line application into a
specification-driven generation framework.

During the Architecture Assessment, the following observations were made.

The current CLI already provides:

- a centralized command entry point;
- shared command context;
- common output helpers;
- centralized error handling.

These components collectively form a presentation layer.

At the same time, the review highlighted that presentation responsibilities
are not applied consistently across all commands.

Some commands simply delegate to application use cases, while others perform
additional orchestration before invoking the application layer.

This inconsistency makes the presentation layer harder to evolve and more
difficult to reason about.

The objective of this RFC is to establish a unified architectural direction
before additional commands and interfaces are introduced.

---

# Architecture Assessment

The architectural review produced several findings relevant to this RFC.

## Existing Presentation Components

The current presentation layer already includes:

- CLI application;
- command implementations;
- command context;
- output abstraction;
- error handler.

These components provide a solid foundation and should be preserved.

## Responsibility Distribution

Presentation responsibilities are currently distributed across multiple
locations.

Some commands:

- translate CLI arguments;
- coordinate application services;
- validate intermediate results;
- present output.

Other commands simply delegate to a use case.

This creates multiple command styles inside the same interface layer.

## Application Interaction

Application use cases expose different kinds of outcomes.

Some return structured models.

Others rely on exceptions.

Others perform work without returning presentation-oriented information.

This inconsistency forces presentation logic to compensate for differences
between use cases.

## Future Evolution

Future interfaces may include:

- REST APIs;
- Web interfaces;
- Desktop applications;
- Automation services.

The current presentation model should therefore evolve toward reusable
presentation principles rather than CLI-specific implementations.

---

# Problem Statement

The current architecture already contains the essential building blocks of a
presentation layer.

The problem is not the absence of presentation abstractions.

The problem is the lack of a unified architectural model describing how those
components should collaborate.

Without such guidance, future commands and interfaces risk introducing
additional orchestration, duplicated presentation logic and inconsistent user
experience.

As FamilyOS continues to grow, maintaining consistency across multiple entry
points becomes increasingly difficult without an explicit architectural
decision.

---

# Decision Drivers

This RFC is primarily motivated by the following architectural drivers.

- Consistency
- Maintainability
- Simplicity
- Testability
- Separation of Responsibilities

Performance is not a primary driver for this decision.

Security is not directly affected by this RFC.

Backward compatibility should be preserved throughout the migration.

---

# Goals

This RFC intends to achieve the following objectives.

- Define a unified presentation architecture.
- Consolidate existing presentation responsibilities.
- Minimize orchestration inside presentation components.
- Promote consistent command implementations.
- Improve long-term maintainability.
- Prepare the architecture for additional presentation interfaces.
- Preserve the existing user experience.

---

# Non Goals

This RFC does not attempt to redesign the application layer.

This RFC does not introduce new user interfaces.

This RFC does not modify the generation engine.

This RFC does not redefine dependency injection.

This RFC does not redesign the plugin runtime.

These topics are expected to be addressed by future RFCs.


---

# Architectural Decision

FamilyOS shall consolidate its existing presentation layer into a unified
architectural model.

This RFC does not introduce a new presentation framework.

Instead, it formalizes how existing presentation components collaborate and
defines clear responsibility boundaries between the presentation layer and the
application layer.

Presentation components shall be responsible only for:

- receiving external requests;
- translating input into application requests;
- invoking application use cases;
- presenting application results;
- translating application errors into user-facing responses.

Business rules, orchestration and generation decisions shall remain outside of
the presentation layer.

This decision establishes presentation as an architectural responsibility
rather than a collection of CLI utilities.

---

# Proposed Design

The Presentation Layer is composed of five conceptual responsibilities.

```text
External Interface
        │
        ▼
Command / Controller
        │
        ▼
Presentation Context
        │
        ▼
Application Use Case
        │
        ▼
Presentation Result
        │
        ▼
Output / Presenter
