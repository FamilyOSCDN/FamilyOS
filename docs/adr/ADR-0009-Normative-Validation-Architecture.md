# ADR-0009 — Normative Validation Architecture

**Identifier:** ADR-0009  
**Title:** Normative Validation Architecture  
**Status:** Accepted  
**Date:** 2026-08-03  
**Owner:** FamilyOS Project  
**Layer:** Architecture Decision Records  

---

# Status

Accepted

---

# Date

2026-08-03

---

# Context

FamilyOS adopts a Specification-Driven Platform approach where technical contracts are defined before implementation.

Specifications define:

- structural requirements;
- behavioral expectations;
- compatibility rules;
- platform constraints.

As the platform grows, manually verifying compliance with specifications becomes insufficient.

FamilyOS requires a validation architecture capable of determining whether implementations, documentation, plugins, and generated artifacts comply with approved specifications.

Previous architectural decisions established:

- ADR-0007 — Official Plugin Architecture;
- ADR-0008 — Specification-Driven Platform.

These decisions require a complementary validation model.

---

# Problem Statement

A platform governed by specifications requires a reliable mechanism to verify conformance.

Traditional validation approaches based only on tests create several limitations:

- tests may validate implementation details without validating contracts;
- documentation rules may remain unchecked;
- structural violations may be discovered late;
- compliance cannot be measured consistently.

FamilyOS requires a validation architecture where specifications can be transformed into objective verification rules.

---

# Decision

FamilyOS adopts a Normative Validation Architecture.

Validation SHALL be based on approved specifications and their normative requirements.

The validation system SHALL verify compliance between:

```text
Specifications

↓

Validation Rules

↓

Implementation Artifacts

↓

Compliance Results
```

Validation SHALL produce deterministic results.

---

# Architectural Principles

The Normative Validation Architecture follows these principles.

---

## Specification-First Validation

Specifications SHALL define the authoritative source for validation rules.

---

## Objective Verification

Validation rules SHALL produce measurable results.

A validation result SHALL be:

- PASS;
- FAIL;
- NOT APPLICABLE.

---

## Deterministic Results

The same input and the same validation rules SHALL produce the same result.

---

## Traceability

Every validation result SHOULD reference the specification requirement that produced it.

---

## Separation of Validation and Correction

Validation SHALL identify non-conformity.

Validation SHALL NOT automatically modify resources unless explicitly defined by another approved mechanism.

---
# Architecture Overview

The Normative Validation Architecture is organized into multiple layers.

The validation flow is defined as:

```text
                 Specifications

                       │

                       ▼

              Validation Rules

                       │

                       ▼

              Validation Engine

                       │

        ┌──────────────┼──────────────┐

        ▼              ▼              ▼

 Documentation    Structure      Runtime

 Validation       Validation    Validation

        │              │              │

        └──────────────┼──────────────┘

                       ▼

             Compliance Report
```

---

# Validation Rule Model

Validation rules represent executable interpretations of normative requirements.

A validation rule SHALL contain:

- specification identifier;
- requirement identifier;
- validation logic;
- validation scope;
- validation result.

Example:

```text
Specification:

SPEC-0005-R3

Requirement:

Every document SHALL contain exactly one level-1 heading.

Validation Rule:

Count level-1 headings.

Expected result:

Exactly one.
```

---

# Validation Engine

The Validation Engine is responsible for executing validation rules against FamilyOS resources.

The Validation Engine SHALL:

- load applicable validation rules;
- execute validation checks;
- collect results;
- generate compliance information.

The Validation Engine SHALL NOT modify validated resources.

---

# Validation Layers

FamilyOS validation SHALL support multiple validation layers.

---

## Structural Validation

Structural validation verifies:

- directories;
- files;
- naming rules;
- document organization.

Examples:

- SPEC-0006 compliance;
- SPEC-0007 compliance;
- SPEC-0008 compliance.

---

## Metadata Validation

Metadata validation verifies:

- identifiers;
- versions;
- statuses;
- required metadata fields.

Examples:

- SPEC-0002 compliance;
- SPEC-0003 compliance;
- SPEC-0004 compliance.

---

## Documentation Validation

Documentation validation verifies:

- document structure;
- required sections;
- formatting rules.

Example:

- SPEC-0005 compliance.

---

## Platform Validation

Platform validation verifies implementation contracts.

Examples:

- plugin lifecycle compliance;
- capability contracts;
- contribution contracts.

---

# Compliance Reporting

Validation results SHALL be presented through compliance reports.

A compliance report SHALL include:

- validation scope;
- executed rules;
- results;
- failures;
- references to violated requirements.

Example:

```text
FamilyOS Compliance Report

SPEC-0005-R3  PASS
SPEC-0006-R2  PASS
SPEC-0008-R5  FAIL

Result:

NON-COMPLIANT
```

---

# CLI Integration

The FamilyOS CLI SHOULD provide validation commands.

Example:

```bash
familyos validate
```

The command MAY support:

```bash
familyos validate documentation

familyos validate plugins

familyos validate project
```

---

# Validation Lifecycle

Validation rules SHALL evolve with specifications.

When a specification changes:

- related validation rules SHOULD be reviewed;
- obsolete rules SHOULD be deprecated;
- new rules SHOULD be introduced when required.

---

# Validation Scope

Validation MAY apply to:

- documentation;
- source code;
- plugins;
- generated artifacts;
- project structures.

---
# Consequences

The adoption of a Normative Validation Architecture introduces the following consequences.

---

## Positive Consequences

### Increased Platform Reliability

FamilyOS can verify that implementations and resources conform to defined contracts.

---

### Automated Compliance

Specifications can progressively become executable validation sources.

---

### Reduced Specification Drift

Validation ensures that implementations remain aligned with approved contracts.

---

### Improved Transparency

Compliance reports provide explicit visibility into platform conformity.

---

### Foundation for Developer Tooling

The validation architecture enables future tooling such as:

- CLI validators;
- CI validation pipelines;
- conformance reports;
- automated documentation checks.

---

## Negative Consequences

### Additional Maintenance

Validation rules require continuous maintenance alongside specifications.

---

### Increased Initial Complexity

The platform requires additional validation infrastructure.

---

### Governance Requirement

Specification changes require corresponding validation review.

---

# Governance

The Normative Validation Architecture SHALL be governed through:

- Specifications;
- Architecture Decision Records;
- Validation Rule Reviews;
- Compliance Processes.

Changes to validation behavior SHALL preserve traceability to the originating specification requirement.

Validation rules SHALL NOT introduce requirements that are not defined by approved specifications.

---

# Implementation Status

The architecture defined by this ADR is progressively implemented through:

- FamilyOS CLI validation capabilities;
- specification validation tooling;
- automated test suites;
- plugin validation mechanisms;
- generation framework validation.

Existing validation practices already follow this model through:

- mypy validation;
- ruff validation;
- pytest validation;
- plugin contract validation;
- architecture conformance checks.

---

# Related Specifications

This ADR depends on:

- SPEC-0001 — Documentation Structure
- SPEC-0002 — Identifier
- SPEC-0003 — Metadata
- SPEC-0004 — Versioning
- SPEC-0005 — Document Format
- SPEC-0006 — Directory Layout
- SPEC-0007 — File Format
- SPEC-0008 — Naming Conventions

---

# Related RFCs

This ADR is related to:

- RFC-000Y — Plugin SDK v2
- RFC-000Z — Plugin Discovery & Distribution
- RFC-000AA — Plugin Versioning & Compatibility
- RFC-000AB — Plugin Dependency Graph
- RFC-000AC — Plugin Resolution Diagnostics
- RFC-000AD — Plugin Resolution User Experience
- RFC-000AG — Plugin Generated Artifacts

---

# Related ADRs

Related architectural decisions:

- ADR-0007 — Official Plugin Architecture
- ADR-0008 — Specification-Driven Platform

---

# Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0.0 | Accepted | Initial publication of the Normative Validation Architecture decision. |

