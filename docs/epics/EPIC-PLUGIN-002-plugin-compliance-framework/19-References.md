# Plugin Compliance Framework

# 19 References

## Introduction

The Plugin Compliance Framework depends on a broad set of FamilyOS architectural, engineering, governance, and plugin ecosystem foundations.

This document identifies the principal normative and contextual references that influence EPIC-PLUGIN-002.

These references define requirements that the compliance framework consumes, coordinates, or translates into plugin-specific compliance rules.

The compliance framework does not replace these sources of authority.

---

# Reference Principle

The governing reference principle is:

> Compliance rules should trace back to authoritative FamilyOS requirements whenever such requirements already exist.

EPIC-PLUGIN-002 coordinates enforcement.

It does not redefine foundational architecture, testing, quality, documentation, security, or plugin contracts without an explicit architectural decision.

---

# Engineering Foundation

## EPIC-ENG-001 — Engineering Foundation

The Engineering Foundation defines the general engineering model within which the Plugin Compliance Framework operates.

Relevant concerns include:

* engineering principles;
* development workflows;
* coding standards;
* project structure;
* toolchain;
* configuration;
* governance;
* lifecycle;
* release practices.

Plugin compliance should align with these platform-wide engineering expectations.

---

# Documentation Framework

## EPIC-DOC-001 — Documentation Framework

The Documentation Framework defines FamilyOS documentation architecture and standards.

Plugin compliance may consume documentation requirements covering:

* required plugin documentation;
* structure;
* naming;
* references;
* formatting;
* completeness;
* lifecycle documentation.

Documentation-specific standards remain authoritative within EPIC-DOC-001.

---

# Testing Framework

## EPIC-TST-001 — Testing Framework

The Testing Framework defines how FamilyOS testing is structured, governed, executed, and integrated into engineering workflows.

Plugin compliance consumes testing evidence rather than redefining the testing strategy.

Relevant concerns include:

* unit tests;
* contract tests;
* integration tests;
* regression tests;
* lifecycle tests;
* test execution evidence;
* testing gates.

---

# Quality Framework

## EPIC-QLT-001 — Quality Framework

The Quality Framework defines platform-wide quality expectations.

Plugin compliance may consume quality evidence related to:

* static analysis;
* type checking;
* test results;
* maintainability;
* quality gates;
* engineering quality standards.

Quality semantics remain owned by EPIC-QLT-001.

---

# Plugin Architecture

## FamilyOS Plugin Architecture

The Plugin Architecture is one of the primary normative sources for EPIC-PLUGIN-002.

It defines:

* plugin integration boundaries;
* plugin lifecycle;
* plugin structure;
* supported extension mechanisms;
* capabilities;
* contributions;
* plugin metadata;
* runtime interaction;
* dependency expectations.

The Compliance Framework verifies conformance to these contracts.

---

# Official Plugins Architecture

## ADR-0007 — Official Plugins Architecture

ADR-0007 defines the architecture and governance principles for official FamilyOS plugins.

EPIC-PLUGIN-002 builds on these principles by introducing systematic and automatable conformance validation.

Relevant areas include:

* official plugin structure;
* architectural boundaries;
* plugin responsibilities;
* platform integration;
* first-party governance.

---

# Plugin Implementation Strategy

## ADR-0013 — Official Plugin Implementation Strategy

Where applicable, this architectural decision provides implementation constraints and patterns for official plugins.

Compliance rules may reference requirements established by this strategy when those requirements are intended to be enforceable platform contracts.

---

# Specification-Driven Architecture

## ADR-0008 — Specification-Driven Platform

The specification-driven platform approach influences how compliance requirements should be represented.

Relevant principles include:

* explicit contracts;
* machine-readable specifications;
* deterministic validation;
* generated or derived tooling;
* separation between specification and implementation.

The Compliance-as-Code direction of EPIC-PLUGIN-002 aligns strongly with this model.

---

# Normative Validation Architecture

## ADR-0009 — Normative Validation Architecture

The Normative Validation Architecture provides important context for the distinction between:

* normative requirements;
* validation mechanisms;
* validation results;
* enforcement.

EPIC-PLUGIN-002 extends these concepts specifically into plugin compliance.

---

# Plugin Domain Maturity

## ADR-0010 — Official-Plugin Domain Maturity Review

Domain maturity review contributes to understanding the level of engineering assurance expected from official plugins.

Compliance may consume maturity-related requirements where they become explicit and mechanically enforceable.

Maturity assessment itself should remain distinct from ordinary rule evaluation where human judgment is required.

---

# Plugin Certification

## ADR-0011 — Official-Plugin Certification Process

The Official-Plugin Certification Process defines the broader certification context into which EPIC-PLUGIN-002 integrates.

The primary relationship is:

```text
Compliance
    │
    ▼
Certification Eligibility
    │
    ▼
Certification Process
```

Compliance produces technical conformance evidence.

Certification provides a broader governed trust decision.

---

# Official Plugin RFCs

The official plugin RFCs define domain-specific plugin behavior and contracts.

Current relevant RFCs include:

```text
RFC-0010 — Security Plugin
RFC-0011 — Health Plugin
RFC-0012 — Finance Plugin
RFC-0013 — Education Plugin
RFC-0014 — Documents Plugin
RFC-0015 — Communication Plugin
```

Compliance may verify generic plugin requirements derived from these RFCs where those requirements represent reusable platform contracts.

Domain-specific business correctness remains owned by the corresponding domain specifications.

---

# Security Architecture

## FamilyOS Security Architecture

The Security Architecture defines security principles and boundaries relevant to plugin compliance.

Compliance may consume requirements concerning:

* trust boundaries;
* permissions;
* authorization;
* secret handling;
* sensitive data access;
* external communication;
* runtime isolation;
* privileged operations.

Security architecture remains the authoritative source for security meaning.

---

# Configuration Architecture

## FamilyOS Configuration Architecture

The Configuration Architecture defines how configuration should be represented and consumed across FamilyOS.

Plugin compliance may validate:

* declared configuration;
* configuration schemas;
* required values;
* secret declarations;
* prohibited environment assumptions;
* supported configuration interfaces.

---

# Runtime Architecture

## FamilyOS Runtime Architecture

The Runtime Architecture defines plugin execution boundaries and supported runtime contracts.

Relevant compliance areas include:

* registration;
* activation;
* execution;
* runtime dependencies;
* lifecycle behavior;
* internal API restrictions.

---

# Capability Architecture

The FamilyOS capability model defines explicit interfaces through which plugins expose supported behavior.

Compliance rules may validate:

* capability declarations;
* capability identifiers;
* contract implementation;
* registration;
* compatibility.

Capability contracts remain authoritative.

---

# Contribution Architecture

The contribution system defines the mechanisms through which plugins register platform extensions.

Relevant contribution types may include:

* policies;
* rules;
* recipes;
* workflows;
* commands;
* services;
* integrations;
* templates.

The Compliance Framework verifies that plugin contributions follow supported contribution contracts.

---

# Dependency Architecture

FamilyOS architecture establishes allowed dependency relationships.

Plugin compliance may validate:

* plugin dependencies;
* platform dependencies;
* prohibited internal dependencies;
* dependency direction;
* circular dependencies;
* compatibility constraints.

---

# Release Strategy

## FamilyOS Release Strategy

Release strategy influences compliance gates and release-grade evidence requirements.

Relevant areas include:

* versioning;
* release candidates;
* tags;
* artifacts;
* release eligibility;
* compatibility;
* changelogs.

The Release Framework remains responsible for release mechanics.

Compliance provides release eligibility evidence.

---

# Build Framework

## EPIC-BLD-001 — Build Framework

The Build Framework is expected to define how FamilyOS creates reproducible artifacts.

Plugin compliance integrates with build workflows through:

* build eligibility;
* artifact validation;
* package metadata;
* artifact identity;
* artifact digest;
* source-to-artifact traceability.

---

# Release Framework

## EPIC-REL-001 — Release Framework

The Release Framework is expected to define:

* release workflow;
* release gates;
* release candidates;
* versioning;
* artifact publication;
* distribution.

EPIC-PLUGIN-002 provides plugin-specific compliance evidence that the Release Framework can consume.

---

# Governance Architecture

## FamilyOS Governance Architecture

Governance architecture influences:

* ownership;
* policy evolution;
* approval authority;
* exceptions;
* suppressions;
* lifecycle;
* traceability.

Compliance governance must integrate with the broader FamilyOS governance model.

---

# Documentation Architecture

## FamilyOS Documentation Architecture

The Documentation Architecture defines how FamilyOS documentation is organized and governed.

Compliance documentation requirements should align with this architecture rather than create independent documentation conventions.

---

# Repository Architecture

Repository structure and conventions may influence:

* plugin discovery;
* structural rules;
* documentation locations;
* test locations;
* compliance policy artifacts.

Repository-level rules should remain aligned with the authoritative engineering and project structure documentation.

---

# Engineering Constitution

## FamilyOS Engineering Constitution

The Engineering Constitution represents a high-level normative source for platform engineering behavior.

Compliance rules should remain consistent with its principles.

Where a compliance rule derives directly from constitutional engineering requirements, the relationship should be traceable.

---

# Naming Conventions

## docs/04-reference/Naming-Conventions.md

Naming conventions may influence compliance requirements concerning:

* plugin IDs;
* namespaces;
* files;
* directories;
* capabilities;
* contributions;
* rule identifiers.

Where naming conventions are normative, compliance can automate their validation.

---

# Reserved Words

## docs/04-reference/Reserved-Words.md

Reserved names may participate in structural or identity compliance validation.

The compliance system should consume the authoritative reserved-word definitions rather than maintain an independent duplicate list.

---

# Glossary

## docs/04-reference/Glossary.md

The FamilyOS glossary provides authoritative terminology used across EPIC-PLUGIN-002.

Compliance documentation and tooling should use established platform language consistently.

---

# Acronyms

## docs/04-reference/Acronyms.md

Framework documentation should follow the official acronym definitions where applicable.

---

# Language Reference

## docs/04-reference/Language.md

The Language reference influences normative documentation language and terminology.

Compliance rules should use consistent terms such as:

```text
MUST
MUST NOT
SHOULD
SHOULD NOT
MAY
```

when normative semantics are intended.

---

# Specification Registry

## docs/06-specifications/

Formal specifications may define machine-readable or normative contracts consumed by the compliance framework.

As the framework matures, detailed compliance schemas may themselves become FamilyOS specifications.

Potential future specifications may include:

```text
Plugin Compliance Rule Schema
Compliance Profile Schema
Compliance Evidence Schema
Compliance Result Schema
Compliance Report Schema
```

---

# Plugin Metadata Schema

The official plugin metadata schema is a critical compliance dependency.

Metadata rules should validate against the authoritative schema rather than reimplement field semantics independently.

---

# Plugin Manifest

The plugin manifest provides primary evidence for:

* plugin identity;
* version;
* capabilities;
* contributions;
* dependencies;
* compatibility;
* classification.

Manifest compliance is therefore foundational to many rule domains.

---

# Plugin SDK

The FamilyOS Plugin SDK defines supported extension interfaces available to plugin authors.

Compliance may verify that plugins use these supported interfaces rather than internal platform implementation details.

The SDK remains authoritative for its public API contracts.

---

# FamilyOS CLI Architecture

The CLI Architecture defines how compliance commands should integrate into the standard FamilyOS command surface.

EPIC-PLUGIN-002 may introduce compliance capabilities, but command implementation must follow CLI architecture principles.

---

# CI and Engineering Toolchain

The existing engineering toolchain provides important compliance evidence sources.

Current relevant tools include:

```text
Pytest
Ruff
MyPy
```

These tools remain responsible for their own analysis semantics.

The Compliance Framework consumes and interprets their results according to plugin compliance policy.

---

# Pytest

Pytest provides testing evidence.

Compliance may consume:

* execution status;
* passed tests;
* failed tests;
* skipped tests;
* test selection;
* execution metadata.

Compliance does not redefine what a Pytest failure means.

---

# Ruff

Ruff provides static-analysis and formatting-related evidence according to FamilyOS engineering configuration.

Compliance may require successful Ruff validation for specific plugin profiles.

---

# MyPy

MyPy provides type-checking evidence.

Compliance may require MyPy success according to FamilyOS quality and plugin profile policy.

---

# External Standards

EPIC-PLUGIN-002 may eventually integrate with external standards for areas such as:

* software supply chain provenance;
* attestations;
* vulnerability reporting;
* machine-readable findings;
* software bills of materials.

Potential examples may include standards such as:

```text
SARIF
SBOM formats
Software provenance attestations
```

Any external standard adoption should be governed explicitly before becoming normative.

---

# SARIF

SARIF may become useful as a reporting projection for compliance findings.

If supported, SARIF should remain a representation format.

It must not replace the canonical FamilyOS Compliance Result model.

---

# SBOM Integration

A future Software Bill of Materials integration may provide evidence for:

* dependencies;
* artifact contents;
* supply chain provenance;
* vulnerability analysis.

SBOM semantics should remain owned by the relevant supply-chain architecture or standard.

---

# Attestation Standards

Future attestation standards may strengthen:

* evidence integrity;
* producer identity;
* artifact binding;
* trusted build provenance.

These should extend the Evidence Model without changing the principle that evidence must remain traceable to compliance rules.

---

# Reference Hierarchy

Where multiple references apply, compliance rules should respect the FamilyOS normative hierarchy.

Conceptually:

```text
Engineering Constitution
        │
        ▼
Architecture Decisions
        │
        ▼
RFCs and Specifications
        │
        ▼
Framework Standards
        │
        ▼
Compliance Rules
        │
        ▼
Validator Implementations
```

Implementation behavior must not override higher-level policy.

---

# Conflict Resolution

If two authoritative references appear to conflict, the compliance framework must not invent its own interpretation silently.

The conflict should be resolved through the appropriate:

* ADR;
* RFC;
* specification;
* governance decision.

Only then should the corresponding compliance rule be activated or changed.

---

# Reference Traceability

Every active compliance rule should eventually be able to identify its authoritative references.

Conceptually:

```text
Rule
├── Source Architecture
├── ADR
├── RFC
├── Specification
└── Framework Requirement
```

This relationship improves transparency and auditability.

---

# Reference Stability

References may evolve.

Compliance rules must therefore distinguish between:

* stable normative references;
* versioned specifications;
* historical references;
* deprecated references.

A rule must not silently change meaning because a referenced document was rewritten without compliance governance.

---

# Future Reference Documents

EPIC-PLUGIN-002 is expected to produce or depend on future detailed implementation specifications.

Potential future documents include:

```text
Plugin Compliance Specification
Compliance Rule Schema
Compliance Profile Specification
Validation Engine Specification
Evidence Schema
Finding Schema
Compliance Report Schema
Compliance CLI Specification
Certification Handoff Specification
```

These documents should refine this EPIC without contradicting its foundational architecture.

---

# Reference Governance

References used by active rules should be governed.

When an authoritative reference is deprecated or replaced, affected compliance rules should be reviewed.

Possible outcomes include:

* no rule change;
* documentation update;
* rule deprecation;
* new Rule ID;
* profile migration.

---

# References Summary

The Plugin Compliance Framework sits at the intersection of multiple FamilyOS engineering foundations.

Its principal dependency model is:

```text
Engineering Foundation
        │
        ├── Documentation Framework
        ├── Testing Framework
        ├── Quality Framework
        ├── Security Architecture
        ├── Runtime Architecture
        ├── Configuration Architecture
        ├── Governance Architecture
        │
        ▼
Plugin Architecture
        │
        ▼
Plugin Compliance Framework
        │
        ▼
Build / Release / Certification
```

The Compliance Framework translates these authoritative requirements into verifiable plugin conformance rules.

---

# Final Reference Principle

The governing principle of references within EPIC-PLUGIN-002 is:

> Compliance should enforce FamilyOS contracts, not invent parallel versions of them.

Every compliance requirement should therefore remain traceable to explicit platform architecture, policy, specification, or governance whenever an authoritative source exists.
