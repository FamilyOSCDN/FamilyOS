# ADR-0011 — Official Plugin Certification Process

## Status

Accepted

## Date

2026-08-04

---

# Context

FamilyOS Phase 2 introduces an official plugin ecosystem.

The platform now supports multiple official domain plugins:

- RFC-0010 — Security Plugin
- RFC-0011 — Health Plugin
- RFC-0012 — Finance Plugin

These plugins demonstrate that FamilyOS can support independent domain development while maintaining a stable architectural contract.

As the ecosystem grows, FamilyOS requires a formal certification process to ensure that official plugins maintain:

- architectural consistency
- SDK compatibility
- runtime stability
- security principles
- testing quality
- long-term maintainability

This ADR defines the requirements and lifecycle required for a plugin to become an official FamilyOS plugin.

---

# Decision

A plugin must complete a structured certification process before becoming an official FamilyOS plugin.

The lifecycle is:

```text
Plugin Development

        ↓

Plugin Candidate

        ↓

Certification Review

        ↓

Official FamilyOS Plugin
```

Only certified plugins may be included in:

- FamilyOS official plugin registry
- default platform distribution
- official documentation
- supported domain ecosystem


---

# Plugin Maturity Levels

FamilyOS defines three maturity levels for plugin lifecycle management.

---

# Level 1 — Experimental Plugin

An experimental plugin is under active development.

Requirements:

- valid plugin structure
- plugin metadata
- basic implementation
- local tests

Experimental plugins:

- are not part of the official ecosystem
- may change architecture freely
- are not guaranteed SDK compatibility

---

# Level 2 — Plugin Candidate

A candidate plugin has reached architectural completeness but has not completed official certification.

Requirements:

- implements the Plugin SDK contract
- integrates with PluginRuntime
- exposes capabilities
- provides contributions
- includes domain validation
- includes automated tests

A candidate plugin must pass:

- mypy
- ruff
- pytest

without errors.

---


---

# Level 3 — Official FamilyOS Plugin

An official FamilyOS plugin has successfully completed the certification process.

An official plugin is considered:

- architecturally stable
- SDK compatible
- runtime validated
- production ready
- supported by the FamilyOS ecosystem

Official plugins become part of:

- the official plugin registry
- supported FamilyOS distributions
- official documentation

---

# Certification Requirements

An official plugin must satisfy all certification requirements.

The certification review validates:

- architecture compliance
- plugin contract compliance
- runtime integration
- capability stability
- contribution correctness
- validation quality
- testing coverage
- documentation completeness

---


---

# Architecture Requirements

The plugin must provide the official plugin foundation:

```text
plugins/builtin/<domain>/

├── plugin.yaml
├── plugin.py
├── capabilities/
├── validation/
├── recipes/
└── templates/
```
Domain-specific modules MAY be added according to domain requirements:

models/

profiles/

records/

metrics/

policies/

rules/

registries/

The plugin architecture must follow:

ADR-0007 — Official Plugins Architecture
ADR-0010 — Official Plugin Domain Maturity Review
Plugin Contract Requirements

The plugin must implement the FamilyOS Plugin SDK contract.

Required elements:

```text
Plugin

├── metadata
├── capabilities()
├── contributions()
└── runtime integration
```
Plugin metadata must provide:

name
version
author
description

Plugin manifest must provide:

identifier
module path
class name
enabled state


---

# Runtime Certification

The plugin must successfully pass runtime validation.

The required lifecycle is:

```text
Plugin

    ↓

Discovery

    ↓

Loading

    ↓

Initialization

    ↓

Activation

    ↓

ACTIVE state
```

The runtime must correctly register:

- plugin instance
- capabilities
- contributions

---

# Capability Certification

Official plugins must expose stable domain capabilities.

Requirements:

- capability identifiers must be unique
- capability identifiers must be immutable
- capabilities must expose metadata
- capabilities must be registered by PluginRuntime

Examples:

- familyos.finance.account
- familyos.health.record
- familyos.security.policy

---

# Contribution Certification

Official plugins may contribute functionality through the FamilyOS contribution system.

Supported contribution types:

- GenerationContribution
- GenerationRecipeContribution
- TemplateContribution

Each contribution must respect the Plugin SDK contract.


---

# Validation Certification

Official plugins must protect domain consistency.

Validation follows two levels:

## Entity Validation

Domain entities must reject invalid states.

Example:

- Invalid Account
- Validation Error

---

## Domain Validation

Business rules must be implemented through domain validators.

Example:

- FinanceValidator
- HealthValidator
- SecurityValidator

---

# Testing Requirements

Every official plugin must provide automated tests.

Required test areas:

- domain models
- registries
- validation
- plugin contract
- runtime loading
- runtime activation
- capabilities
- contributions

The complete test suite must pass:

- mypy
- ruff
- pytest

without errors.

---

# Security Requirements

Official plugins must respect FamilyOS security principles.

Plugins must:

- protect sensitive domain data
- avoid exposing secrets
- validate external inputs
- respect capability boundaries
- avoid unauthorized runtime access

Protected domains include:

- Health information
- Financial information
- Identity information
- Family records

---

# Certification Approval Process

The certification process requires:

Plugin Candidate

↓

Architecture Review

↓

Technical Validation

↓

Security Review

↓

Official Approval

↓

Official FamilyOS Plugin

The approval decision must confirm:

- architecture compliance
- runtime compatibility
- test quality
- documentation completeness
- long-term maintainability

---

# Maintenance and Versioning

Official plugins must maintain compatibility with the FamilyOS Plugin SDK.

Changes affecting:

- capabilities
- contributions
- domain models
- generated artifacts

must follow versioning rules.

Breaking changes require:

- compatibility review
- migration strategy
- documentation update

---

# Consequences

## Positive Consequences

The certification process provides:

- predictable plugin quality
- stable ecosystem growth
- reduced architectural drift
- safer domain expansion
- easier maintenance

---

## Negative Consequences

The certification process introduces:

- additional development effort
- documentation requirements
- architectural review overhead

These constraints are intentional to preserve long-term FamilyOS stability.

---

# Related Documents

- ADR-0007 — Official Plugins Architecture
- ADR-0010 — Official Plugin Domain Maturity Review
- RFC-000Y — Plugin SDK v2
- RFC-0010 — Official Security Plugin
- RFC-0011 — Official Health Plugin
- RFC-0012 — Official Finance Plugin

