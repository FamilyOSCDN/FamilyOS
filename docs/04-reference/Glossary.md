# FamilyOS Glossary

**Version:** 1.0
**Status:** Stable
**Last Updated:** August 2026

---

# Purpose

This document defines the official terminology used throughout the FamilyOS platform.

Each concept is defined exactly once and serves as the authoritative reference for all documentation.

This document is normative.

---

# Scope

The glossary applies to:

- Foundation
- Product
- Architecture
- Engineering
- Reference
- Specifications
- ADRs
- RFCs
- Plugin documentation
- Generated documentation

---

# Glossary

## Aggregate

A consistency boundary that groups related entities and value objects into a single transactional unit.

---

## Aggregate Root

The primary entity through which an aggregate is accessed and modified.

---

## Application Layer

The layer responsible for orchestrating use cases without containing business rules.

---

## Architecture

The fundamental organization of the FamilyOS platform, including its components, relationships, and governing principles.

---

## Artifact

A generated or manually maintained deliverable produced by the platform, such as source code, documentation, or configuration files.

---

## Bounded Context

A well-defined boundary within which a domain model has a single, consistent meaning.

---

## Capability

A feature or service exposed by a plugin through the Plugin SDK.

---

## Clean Architecture

The architectural style adopted by FamilyOS that separates concerns into independent layers with inward-facing dependencies.

---

## Command

A request to perform a state-changing operation.

---

## Contribution

A plugin-provided extension that integrates with the platform through officially supported extension points.

---

## Domain

A functional area representing a coherent set of business responsibilities.

---

## Domain Model

The representation of business concepts, relationships, rules, and behaviors within a domain.

---

## Entity

An object identified by a stable identity whose lifecycle extends beyond changes to its attributes.

---

## Event

A record describing something that has occurred within the system.

---

## Generation Framework

The subsystem responsible for generating platform artifacts from specifications and templates.

---

## Plugin

An independently deployable software component that extends FamilyOS without modifying the platform core.

---

## Plugin Runtime

The runtime environment responsible for discovering, loading, validating, activating, and managing plugins.

---

## Preset

A predefined generation configuration that combines one or more generation strategies.

---

## Repository

An abstraction that provides access to domain objects while hiding persistence details.

---

## Specification

A structured description defining the expected behavior, structure, or configuration of a platform component.

---

## Strategy

An interchangeable algorithm or implementation selected according to a specific context.

---

## Template

A reusable document or source file used by the Generation Framework to produce artifacts.

---

## Use Case

An application service that coordinates domain operations to fulfill a business objective.

---

## Value Object

An immutable object identified solely by its attributes rather than by identity.

---

# Maintenance

New concepts shall be added only when they are platform-wide concepts.

Project-specific terminology belongs to the appropriate domain documentation.

Definitions should remain concise, implementation-independent, and stable across platform releases.

---

# Summary

The FamilyOS Glossary establishes a common vocabulary shared by the entire platform. It ensures that every architectural, technical, and functional concept has a single authoritative definition, promoting consistency, clarity, and long-term maintainability.
