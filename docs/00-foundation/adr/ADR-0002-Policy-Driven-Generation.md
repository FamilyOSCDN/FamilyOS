---
id: ADR-0002
title: Policy-Driven Generation Architecture
status: Accepted
date: 2026-07-28
deciders:
  - FamilyOS Team
consulted: []
informed: []
related:
    - Generation-Architecture
---

# Context

FamilyOS is designed around a generation engine that transforms business
specifications into complete software architectures.

As the project grows, generation decisions such as naming conventions,
artifact locations, template selection, rendering context and execution
strategies will become increasingly numerous.

Keeping these decisions embedded inside large services would gradually
increase coupling, reduce testability and make extensions through plugins
more difficult.

A more explicit architectural model is required.

---

# Decision

FamilyOS adopts a **Policy-Driven Generation Architecture**.

Business decisions are encapsulated into dedicated **Policies**.

Each Policy is responsible for answering one and only one business question.

Examples include:

- ArtifactPathPolicy
- ArtifactTemplatePolicy
- ArtifactNamingPolicy
- ArtifactContextPolicy

Policies are deterministic, stateless, injectable and independently testable.

Higher-level components consume these policies without owning the business
rules themselves.

---

# Responsibilities

The generation engine is composed of four categories of components.

## Policies

Policies encapsulate business decisions.

They answer questions such as:

- Where should an artifact be generated?
- Which template should be used?
- How should an artifact be named?
- Which rendering context should be provided?

---

## Planners

Planners organize business decisions into executable generation plans.

They determine:

- which artifacts exist;
- their relationships;
- their ordering.

---

## Adapters

Adapters transform one model into another.

They never introduce business rules.

Their responsibility is limited to converting representations.

---

## Strategies

Strategies execute technical algorithms.

Examples include:

- template rendering;
- filesystem generation;
- execution pipelines.

Strategies perform work but do not decide business rules.

---

# Consequences

## Positive

- Business decisions become explicit.
- Components become easier to understand.
- Policies are independently testable.
- Plugin extensions become significantly simpler.
- The generation engine remains technology independent.
- Future evolution is localized around well-defined extension points.

## Negative

- The number of small classes increases.
- Additional abstractions require discipline.
- Developers must understand the distinction between Policies,
  Planners, Adapters and Strategies.

These trade-offs are considered acceptable in exchange for long-term
maintainability.

---

# Alternatives Considered

## Monolithic Generation Service

Rejected.

Embedding all generation decisions inside one or several large services
would create unnecessary coupling and make future extensions difficult.

## Factory-Based Generation

Rejected.

Factories are useful when object construction is complex.

However, they are not appropriate for encapsulating business decisions such
as naming, paths or template selection.

These concerns are better represented as independent Policies.

---

# Status

Accepted.

This ADR defines the architectural direction for all future evolution of
the FamilyOS Generation Engine.

Future generation capabilities should follow the principles defined by this
decision unless a new ADR explicitly supersedes it.

