# Domain Generation Pipeline

## Status

Draft

---

# Purpose

The Domain Generation Pipeline is the core engine of FamilyOS.

Its responsibility is to transform a domain specification into a fully generated domain while keeping every processing step independent, testable and extensible.

The pipeline follows the principles of:

- Domain Driven Design
- Clean Architecture
- Single Responsibility Principle
- Open/Closed Principle
- Dependency Inversion Principle

---

# High-Level Architecture

```text
Specification (.yaml)
        │
        ▼
YamlDomainSpecificationLoader
        │
        ▼
DomainSpecification
        │
        ▼
DomainSpecificationValidator
        │
        ▼
GenerateDomainFromSpecificationUseCase
        │
        ▼
DomainGenerationPlanner
        │
        ▼
DomainGenerationPlan
        │
        ▼
ArtifactGenerationMapper
        │
        ▼
GenerationEngine
        │
        ▼
Generated Project
```

---

# Responsibilities

## YamlDomainSpecificationLoader

Responsible for reading YAML specifications and creating a DomainSpecification object.

It performs no validation.

---

## DomainSpecificationValidator

Ensures the specification is valid.

Typical checks include:

- duplicate names
- missing entities
- missing aggregates
- invalid references
- business rules consistency

---

## GenerateDomainFromSpecificationUseCase

Application orchestrator.

Responsible for:

1. Loading
2. Validation
3. Plugin preprocessing
4. Planning
5. Mapping
6. Generation
7. Plugin postprocessing

No business logic should exist outside this orchestration.

---

## DomainGenerationPlanner

Transforms a validated specification into a generation plan.

The planner decides:

- what must be generated
- generation order
- dependencies

---

## DomainGenerationPlan

Immutable description of the generation process.

Contains GenerationUnits.

---

## GenerationUnit

Represents one unit of generation.

Examples:

- Domain
- Aggregate
- Entity
- Repository
- Service
- Value Object
- Event
- Command
- Query

---

## ArtifactGenerationMapper

Transforms GenerationUnits into concrete generation artifacts.

---

## GenerationEngine

Executes the generation.

The engine never makes business decisions.

It only executes the plan.

---

# Plugin Extension Points

Plugins may contribute during the following stages.

```text
Specification Loaded
        │
        ▼
Pre Validation Hooks
        │
        ▼
Validation
        │
        ▼
Post Validation Hooks
        │
        ▼
Planning
        │
        ▼
Post Planning Hooks
        │
        ▼
Generation
        │
        ▼
Post Generation Hooks
```

Plugins must never modify the engine itself.

They extend the pipeline through hooks.

---

# Design Rules

Every component must have one responsibility.

Dependencies always point inward.

Business rules remain inside the Domain layer.

Application orchestrates.

Infrastructure implements.

Interfaces expose.

---

# Future Evolution

The pipeline must support future generators including:

- Documentation
- Python
- Java
- Rust
- Go
- TypeScript
- OpenAPI
- GraphQL
- Database Schemas
- Microservices
- AI-assisted generators

without changing the Domain layer.

---

# Vision

FamilyOS is not a documentation generator.

It is a domain generation platform.

Every generated artifact originates from a single domain specification.

The specification is the single source of truth.