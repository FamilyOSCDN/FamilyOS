---
id: ARC-002
title: Generation Architecture
status: Stable
owner: FamilyOS Team
created: 2026-07-28
updated: 2026-07-28
version: 1.0.0
tags:
  - architecture
  - generation
  - engine
  - ddd
related:
  - Architecture-Principles
  - Domain-Driven-Design
  - Engineering-Principles
---

# Generation Architecture

## Purpose

The FamilyOS Generation Engine transforms domain specifications into executable software artifacts.

Its objective is **not** simply to generate files.

Its responsibility is to transform business knowledge into a complete, maintainable and extensible software architecture while remaining independent of any generation technology.

The generation engine is therefore considered a core business capability of FamilyOS.

---

# Vision

FamilyOS is a **policy-driven generation engine**.

The domain defines **what** must be generated.

Policies define **how decisions are made**.

Planners organize those decisions into executable plans.

Adapters transform plans into execution models.

Strategies execute generation independently of the underlying technologies.

---

# Architectural Principles

The generation engine follows four fundamental principles.

## 1. The Domain Decides

Business decisions always belong to the domain.

Examples:

- which artifacts exist;
- how artifacts are named;
- where artifacts belong;
- which template should be used.

The domain never knows:

- Jinja
- YAML parsing
- File systems
- CLI frameworks
- External services

---

## 2. The Application Orchestrates

The application coordinates the generation workflow.

Typical workflow:

Specification
→ Validation
→ Planning
→ Mapping
→ Generation

The application contains orchestration logic but no business rules.

---

## 3. Infrastructure Executes

Infrastructure performs technical work.

Examples:

- loading specifications;
- rendering templates;
- writing files;
- loading plugins;
- accessing external resources.

Infrastructure never decides business rules.

---

## 4. Interfaces Trigger Use Cases

Interfaces expose FamilyOS capabilities.

Examples:

- CLI
- REST API
- Desktop UI
- IDE plugins

Interfaces never implement business logic.

---

# Layer Responsibilities

cat > docs/00-foundation/Generation-Architecture.md <<'EOF'
---
id: ARC-002
title: Generation Architecture
status: Stable
owner: FamilyOS Team
created: 2026-07-28
updated: 2026-07-28
version: 1.0.0
tags:
  - architecture
  - generation
  - engine
  - ddd
related:
  - Architecture-Principles
  - Domain-Driven-Design
  - Engineering-Principles
---

# Generation Architecture

## Purpose

The FamilyOS Generation Engine transforms domain specifications into executable software artifacts.

Its objective is **not** simply to generate files.

Its responsibility is to transform business knowledge into a complete, maintainable and extensible software architecture while remaining independent of any generation technology.

The generation engine is therefore considered a core business capability of FamilyOS.

---

# Vision

FamilyOS is a **policy-driven generation engine**.

The domain defines **what** must be generated.

Policies define **how decisions are made**.

Planners organize those decisions into executable plans.

Adapters transform plans into execution models.

Strategies execute generation independently of the underlying technologies.

---

# Architectural Principles

The generation engine follows four fundamental principles.

## 1. The Domain Decides

Business decisions always belong to the domain.

Examples:

- which artifacts exist;
- how artifacts are named;
- where artifacts belong;
- which template should be used.

The domain never knows:

- Jinja
- YAML parsing
- File systems
- CLI frameworks
- External services

---

## 2. The Application Orchestrates

The application coordinates the generation workflow.

Typical workflow:

Specification
→ Validation
→ Planning
→ Mapping
→ Generation

The application contains orchestration logic but no business rules.

---

## 3. Infrastructure Executes

Infrastructure performs technical work.

Examples:

- loading specifications;
- rendering templates;
- writing files;
- loading plugins;
- accessing external resources.

Infrastructure never decides business rules.

---

## 4. Interfaces Trigger Use Cases

Interfaces expose FamilyOS capabilities.

Examples:

- CLI
- REST API
- Desktop UI
- IDE plugins

Interfaces never implement business logic.

---

# Layer Responsibilities


A policy must never answer multiple unrelated questions.

---

# Dependency Rules

The generation engine follows strict dependency rules.

Allowed:

Planner
→
Policy

Mapper
→
Policy

Application
→
Domain

Infrastructure
→
Domain Contracts

Forbidden:

Domain
→
Infrastructure

Domain
→
CLI

Policy
→
File System

Policy
→
Template Engine

---

# Plugin Model

Plugins extend the generation engine through domain contracts.

Plugins should replace or contribute:

- policies;
- planners;
- adapters;
- strategies.

The core generation engine should not require modification when adding new capabilities.

---

# Design Rules

Every new component should satisfy the following principles.

A class should have a single responsibility.

A policy should answer one business question.

A planner should organize decisions.

An adapter should transform models.

A strategy should execute work.

Business decisions belong to the domain.

Technical execution belongs to infrastructure.

---

# Long-Term Objective

The long-term objective of the generation engine is to transform a domain specification into a complete software architecture while remaining:

- deterministic;
- testable;
- extensible;
- technology independent;
- plugin driven.

The generation engine should remain understandable even as FamilyOS grows to hundreds of modules and thousands of generated artifacts.

