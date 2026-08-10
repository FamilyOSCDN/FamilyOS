# Build Framework

# 19 References

## Overview

EPIC-BLD-001 — Build Framework depends on a set of FamilyOS foundations, engineering frameworks, architectural decisions, implementation conventions, and external standards.

This document identifies the principal references that define the context in which the Build Framework operates.

The purpose of these references is to preserve consistency across FamilyOS engineering.

The Build Framework does not operate independently.

It inherits constraints from upstream foundations and provides outputs to downstream frameworks.

The central principle is:

> Build engineering must remain aligned with the broader FamilyOS architecture, governance model, and engineering standards.

---

# Purpose

The References document provides a structured index of materials relevant to EPIC-BLD-001.

It identifies references related to:

* engineering foundations;
* testing;
* quality;
* documentation;
* plugins;
* security;
* release;
* specifications;
* architecture decisions;
* requests for comments;
* repository configuration;
* toolchain standards;
* packaging standards;
* software supply-chain concepts.

The reference set supports:

* traceability;
* architectural consistency;
* implementation guidance;
* validation;
* governance;
* future framework evolution.

---

# Reference Classification

References are grouped into the following categories:

```text id="9aa3ha"
References
│
├── FamilyOS Foundations
├── FamilyOS Engineering Frameworks
├── FamilyOS Architectural Documents
├── FamilyOS Plugin Documents
├── FamilyOS Governance Records
├── Repository References
├── Python Packaging Standards
├── Toolchain References
├── CI and Automation References
├── Supply Chain References
└── Future References
```

---

# Internal FamilyOS References

Internal references define the normative and architectural environment of the Build Framework.

These references take precedence over external guidance where FamilyOS establishes explicit platform rules.

---

# Engineering Foundation

## EPIC-ENG-001 — Engineering Foundation

EPIC-ENG-001 provides the primary engineering foundation upon which the Build Framework is built.

Relevant areas include:

* engineering principles;
* repository architecture;
* development workflow;
* coding standards;
* project structure;
* toolchain;
* environment management;
* dependency management;
* configuration management;
* build philosophy;
* testing philosophy;
* documentation philosophy;
* quality philosophy;
* technical governance;
* engineering lifecycle.

The Build Framework specializes these general concepts for artifact production.

---

# Engineering Constitution

The FamilyOS Engineering Constitution defines foundational engineering constraints and principles that apply across the platform.

The Build Framework must remain compatible with its requirements.

Relevant concerns may include:

* architectural discipline;
* explicit engineering decisions;
* maintainability;
* quality;
* security;
* governance.

---

# Architecture Vision

The FamilyOS Architecture Vision defines the broader platform direction.

Build architecture must support that vision rather than introduce isolated infrastructure assumptions.

---

# Architecture Map

The Architecture Map provides context for how build engineering interacts with other FamilyOS capabilities.

The Build Framework should remain consistent with established platform boundaries.

---

# Application Architecture

Application Architecture defines the structural organization of FamilyOS application components.

Build packaging must preserve and respect those boundaries.

---

# Domain Architecture

Domain Architecture defines domain separation and ownership.

Build processes should not introduce packaging behavior that violates domain boundaries.

---

# Runtime Architecture

Runtime Architecture defines the environment in which FamilyOS software executes.

Build artifacts must remain compatible with runtime expectations.

---

# CLI Architecture

The FamilyOS CLI Architecture is relevant to:

* package construction;
* command entry points;
* executable artifact validation;
* CLI smoke testing.

---

# Configuration Architecture

Configuration Architecture defines broader configuration principles.

The Build Framework specializes them for build-time configuration.

---

# Data Architecture

Data Architecture may influence generated schemas, metadata artifacts, or data-related build outputs.

---

# API Architecture

API Architecture may influence generated API specifications or documentation artifacts.

---

# Infrastructure Architecture

Infrastructure Architecture provides context for future CI, build-worker, artifact-storage, or execution infrastructure.

The Build Framework should not prematurely assume specific infrastructure.

---

# Deployment Architecture

Deployment Architecture begins downstream from release artifacts.

The Build Framework must preserve the separation between build, release, and deployment.

---

# Security Architecture

Security Architecture is a critical reference for:

* dependency trust;
* toolchain security;
* secret handling;
* build permissions;
* artifact integrity;
* software supply-chain controls.

The Build Framework must not define security controls in conflict with the Security Architecture.

---

# Observability Architecture

Observability Architecture provides broader guidance relevant to:

* build logs;
* build metrics;
* stage visibility;
* failure diagnostics;
* structured evidence.

Build observability should align with platform observability principles.

---

# Documentation Architecture

Documentation Architecture governs how Build Framework documentation is structured and maintained.

It also influences generated documentation artifacts.

---

# Governance Architecture

Governance Architecture defines broader decision authority and review structures.

Build Governance operates within this model.

---

# Testing Framework

## EPIC-TST-001 — Testing Framework

EPIC-TST-001 defines the official FamilyOS testing model.

Relevant areas include:

* testing principles;
* testing architecture;
* test levels;
* unit testing;
* integration testing;
* functional testing;
* system testing;
* regression testing;
* fixtures;
* test data;
* mocks;
* test execution;
* performance;
* reporting.

The Build Framework consumes testing evidence.

It does not redefine test semantics.

---

# Testing Relationship

The relationship is:

```text id="5g21w7"
Build Validation
      ↓
Applicable Testing
      ↓
Testing Framework
      ↓
Test Evidence
      ↓
Build Trust
```

---

# Quality Framework

## EPIC-QLT-001 — Quality Framework

EPIC-QLT-001 defines FamilyOS quality governance.

Relevant areas include:

* quality principles;
* quality architecture;
* quality metrics;
* quality evidence;
* quality risk;
* quality debt;
* reviews;
* automation;
* observability;
* quality gates;
* compliance;
* continuous improvement;
* governance.

The Build Framework produces evidence that may participate in quality evaluation.

---

# Quality Relationship

The relationship is:

```text id="7lplwi"
Build Evidence
      ↓
Quality Assessment
      ↓
Quality Gate
```

The Quality Framework owns the gate semantics.

---

# Documentation Framework

## EPIC-DOC-001 — Documentation Framework

EPIC-DOC-001 governs the documentation lifecycle and standards used by the Build Framework.

Relevant areas include:

* documentation vision;
* documentation architecture;
* documentation standards;
* documentation lifecycle;
* templates;
* metadata;
* versioning;
* validation;
* automation;
* generation;
* publishing;
* traceability;
* quality;
* governance;
* toolchain.

---

# Documentation Relationship

The Build Framework interacts with documentation in two ways:

```text id="61lyl5"
Documentation Framework
       ↓
Build Documentation Standards
```

and:

```text id="m7j4g5"
Documentation Sources
       ↓
Build
       ↓
Documentation Artifacts
```

---

# Plugin Architecture

FamilyOS plugin architecture defines how official plugins are structured and integrated.

Relevant build concerns include:

* plugin package structure;
* plugin metadata;
* capability definitions;
* plugin resources;
* plugin discovery;
* plugin packaging.

---

# ADR-0007 — Official Plugins Architecture

ADR-0007 defines the official plugin architecture.

The Build Framework must preserve plugin structural contracts when producing plugin artifacts.

---

# Official Plugin Implementation

## EPIC-PLUGIN-001 — Official Plugin Implementation

This EPIC provides implementation context for official FamilyOS plugins.

The Build Framework should support consistent build and validation behavior across official plugin implementations.

---

# Plugin Compliance Framework

## EPIC-PLUGIN-002 — Plugin Compliance Framework

EPIC-PLUGIN-002 defines how plugin compliance is evaluated.

Relevant build integration includes:

* compliance validation;
* evidence;
* findings;
* compliance gates;
* plugin artifact readiness.

---

# Plugin Compliance Relationship

A conceptual relationship is:

```text id="02yp1e"
Plugin Source
      ↓
Compliance Validation
      ↓
Plugin Build
      ↓
Artifact Validation
```

The Build Framework consumes compliance results without redefining compliance policy.

---

# Official Plugin RFCs

The following RFCs define plugin-domain architecture relevant to component build behavior:

```text id="xq9w73"
RFC-0010 — Security Plugin
RFC-0011 — Health Plugin
RFC-0012 — Finance Plugin
RFC-0013 — Education Plugin
RFC-0014 — Documents Plugin
RFC-0015 — Communication Plugin
```

Build-specific handling must remain compatible with these plugin definitions.

---

# Release Framework

## EPIC-REL-001 — Release Framework

EPIC-REL-001 is the principal downstream framework for Build outputs.

Relevant concerns include:

* versioning;
* release candidates;
* release approval;
* artifact promotion;
* publication;
* distribution;
* release notes;
* release lifecycle;
* rollback strategy.

---

# Build And Release Relationship

The boundary is:

```text id="0u3ik7"
Build Framework
      ↓
Trusted Artifact
      +
Evidence
      ↓
Release Framework
      ↓
Promotion / Publication
```

Build completion must not automatically imply release approval.

---

# Build Framework Control Documents

EPIC-BLD-001 includes the following control documents:

```text id="d9u83h"
EPIC-BLD-001.md
EPIC.yaml
README.md
MANIFEST.md
CHANGELOG.md
VALIDATION.md
Revision-History.md
```

These documents support framework governance, status tracking, validation, and release readiness.

---

# Build Framework Normative Documents

The normative Build Framework document set includes:

```text id="hv85ht"
00-EPIC.md
01-Context.md
02-Vision.md
03-Build-Principles.md
04-Build-Architecture.md
05-Build-Lifecycle.md
06-Build-Input-Requirements.md
07-Build-Inputs-and-Project-Structure.md
08-Build-Toolchain.md
09-Build-Environment-Management.md
10-Dependency-Management.md
11-Build-Configuration.md
12-Build-Philosophy.md
13-Build-Execution.md
14-Artifact-Management.md
15-Build-Validation.md
16-Build-Governance.md
17-Build-Automation-and-CI.md
18-Roadmap.md
19-References.md
20-Validation.md
21-Summary.md
22-Release.md
23-Implementation-Checklist.md
```

---

# FamilyOS Specifications

FamilyOS specifications may define artifact-relevant contracts.

Examples include specifications covering:

* document structure;
* identifiers;
* metadata;
* versioning;
* document formats.

Build tooling that produces specification-governed outputs must preserve those contracts.

---

# SPEC-0001 — Structure

Structure specifications may influence packaging or generated artifacts.

---

# SPEC-0002 — Identifier

Identifier specifications may influence:

* artifact metadata;
* manifests;
* generated resources.

---

# SPEC-0003 — Metadata

Metadata specifications are relevant where build artifacts carry structured FamilyOS metadata.

---

# SPEC-0004 — Versioning

Versioning specifications may interact with artifact identity and Release Framework behavior.

---

# SPEC-0005 — Document Format

Document format requirements may affect generated documentation or document artifacts.

---

# Architecture Decision Records

Build architecture decisions should reference relevant ADRs.

Known FamilyOS architectural decisions may include:

```text id="64qs0u"
ADR-0007
ADR-0008
ADR-0009
ADR-0010
ADR-0011
ADR-0013
```

The exact applicability of each ADR should be evaluated before adding a normative dependency.

---

# ADR Governance Rule

The Build Framework should reference an ADR only where that ADR materially constrains build behavior.

References should not be added solely for completeness.

---

# Request For Comments

RFCs define approved or proposed architectural capabilities.

Build implementation must remain compatible with RFCs affecting:

* packaging;
* plugins;
* metadata;
* generation;
* integration;
* distribution.

---

# Repository References

The FamilyOS repository itself is an important implementation reference.

Relevant areas include:

```text id="htq1ue"
src/
tests/
docs/
pyproject.toml
CI configuration
Git configuration
```

These represent current implementation state rather than Build Framework architecture by themselves.

---

# Source Repository

The canonical repository is the authoritative source for FamilyOS engineering state.

The Build Framework assumes a Git-based repository model unless governance changes this assumption.

---

# `pyproject.toml`

For the Python-based FamilyOS implementation, `pyproject.toml` is an important project-level reference.

It may define:

* project metadata;
* dependencies;
* build backend;
* tool configuration;
* packaging behavior.

The exact content is implementation-specific.

---

# Git

Git is currently the primary version-control mechanism relevant to:

* source revision;
* working tree state;
* tags;
* release history;
* build traceability.

---

# Git Tags

Git tags may participate in release or version context.

Tag semantics belong primarily to Release Framework governance.

---

# Python Runtime

Python is currently a core FamilyOS implementation runtime.

Relevant build concerns include:

* runtime compatibility;
* packaging;
* dependency resolution;
* wheel generation;
* source distributions.

---

# Python Packaging Standards

FamilyOS should use established Python packaging standards where appropriate rather than invent custom packaging behavior.

Relevant standards include the Python Packaging Authority ecosystem and Python Enhancement Proposals governing packaging.

---

# `pyproject.toml` Standard

`pyproject.toml` provides a standardized project configuration and build-system interface.

Relevant concepts include:

* build-system requirements;
* build backend declaration;
* project metadata.

---

# PEP 517

PEP 517 defines a standard interface between build frontends and build backends.

This is relevant to the Build Architecture separation between:

```text id="pg28os"
Build Frontend
      ↓
Build Backend
```

---

# PEP 518

PEP 518 defines build-system requirements in `pyproject.toml`.

This supports explicit build dependency declaration.

---

# PEP 621

PEP 621 standardizes project metadata representation in `pyproject.toml`.

It is relevant to artifact metadata consistency.

---

# Wheel Specification

The Python wheel format defines binary package artifact conventions.

Wheel validation should follow ecosystem standards.

---

# Source Distribution Standards

Python source distributions provide source-based package artifacts.

FamilyOS build validation should preserve standard packaging semantics.

---

# Python Packaging User Guide

The Python Packaging User Guide provides practical ecosystem guidance relevant to:

* building packages;
* project metadata;
* wheel and source distribution generation;
* installation;
* publishing boundaries.

FamilyOS architecture remains authoritative over project-specific behavior.

---

# Toolchain References

Current FamilyOS build and validation tooling may include:

* Python;
* Ruff;
* MyPy;
* Pytest;
* package builders;
* Git.

These tools implement framework capabilities.

They do not define the framework architecture.

---

# Ruff

Ruff is relevant to static source validation.

Build automation may invoke Ruff using canonical repository configuration.

---

# MyPy

MyPy is relevant to static type validation.

Its role in build readiness should remain aligned with FamilyOS engineering standards.

---

# Pytest

Pytest is relevant to test execution.

Test semantics remain governed by EPIC-TST-001.

---

# Python Build Frontend

A standards-compatible Python build frontend may be used to generate package artifacts.

The specific frontend should remain replaceable without changing Build Framework architecture.

---

# CI References

CI systems implement Build Automation.

Provider-specific documentation may be consulted during implementation.

However, CI-provider behavior must remain subordinate to:

```text id="65c0d8"
Canonical Build Semantics
```

---

# CI Provider Independence

FamilyOS should avoid treating one CI provider's syntax as the Build Framework itself.

Provider-specific configuration is an adapter.

---

# Continuous Integration Principles

Relevant general CI concepts include:

* clean checkout;
* repeatable environment setup;
* automated testing;
* build automation;
* artifact collection;
* failure visibility.

These concepts align with the Build Automation chapter.

---

# Reproducible Builds

The broader reproducible-builds ecosystem provides concepts relevant to future FamilyOS maturity.

Relevant concepts include:

* deterministic inputs;
* normalized timestamps;
* controlled environment;
* repeatable toolchain;
* artifact comparison.

FamilyOS may adopt these techniques progressively.

---

# Software Supply Chain References

Future Build Framework maturity may benefit from established supply-chain standards.

These references are informative until FamilyOS explicitly adopts them.

---

# SLSA

Supply-chain Levels for Software Artifacts provides a framework for software supply-chain assurance.

Relevant concepts include:

* build provenance;
* controlled builders;
* source integrity;
* artifact integrity.

FamilyOS may adopt appropriate concepts in future maturity phases.

---

# Provenance

Build provenance describes how artifacts were produced.

The Build Framework's Evidence model provides a foundation for future formal provenance.

---

# SBOM

A Software Bill of Materials may describe software dependency composition.

Potential future use cases include:

* vulnerability analysis;
* dependency transparency;
* release evidence.

No universal FamilyOS SBOM requirement is established by EPIC-BLD-001 at current maturity.

---

# SPDX

SPDX is an industry standard that may become relevant to future SBOM or licensing metadata.

It is currently an informative future reference unless explicitly adopted.

---

# CycloneDX

CycloneDX may also become relevant to future SBOM capabilities.

It is not currently a mandatory FamilyOS build format.

---

# Artifact Signing References

Future release architecture may use artifact signing.

Possible technologies or standards should be evaluated through a separate architectural decision before adoption.

Build Framework references signing conceptually but does not mandate a particular implementation.

---

# Cryptographic Hashing

Cryptographic hashes are relevant to artifact integrity.

The specific approved algorithm should be established through implementation or security governance.

---

# Checksums Versus Signatures

The distinction is:

```text id="7g0hou"
Checksum
   ↓
Content Integrity

Signature
   ↓
Integrity + Authorized Identity
```

This distinction should remain clear in future architecture.

---

# Container References

Containers may become useful for reproducible environments.

Potential references include standard container image and runtime concepts.

Containers are not mandatory Build Framework infrastructure.

---

# OCI

Open Container Initiative specifications may become relevant if FamilyOS adopts container-based build or distribution mechanisms.

They are not current mandatory build standards.

---

# Artifact Registry References

Future artifact storage may use package registries or artifact repositories.

Selection should follow Release Framework and Infrastructure Architecture needs.

The Build Framework does not mandate a dedicated artifact registry.

---

# Semantic Versioning

Versioning strategy belongs primarily to the Release Framework.

Semantic Versioning may be relevant if adopted by FamilyOS release governance.

Build artifacts should consume the canonical version context rather than create independent version semantics.

---

# Version Source Of Truth

The Build Framework should reference the canonical FamilyOS version source defined by Release governance.

Multiple independent version definitions should be avoided.

---

# Documentation Standards References

Build Framework documentation must comply with the Documentation Framework.

Relevant concerns include:

* Markdown standards;
* naming conventions;
* metadata;
* traceability;
* revision history;
* validation.

---

# Naming Conventions

FamilyOS reference documentation for naming conventions should govern:

* files;
* directories;
* identifiers;
* framework names;
* artifact-related labels.

---

# Language Reference

FamilyOS language standards should govern terminology used throughout Build Framework documentation.

---

# Glossary

The FamilyOS Glossary should be updated if Build Framework introduces terms requiring platform-wide definition.

Potential terms include:

* Build Context;
* Build ID;
* Candidate Artifact;
* Trusted Artifact;
* Artifact Set;
* Build Evidence.

---

# Acronyms

The Acronyms reference should include any Build Framework acronyms formally adopted.

---

# Future Reference Candidates

The following areas may become formal references later:

```text id="2poc8f"
Artifact Provenance Standards
Build Attestation Standards
SBOM Standards
Signing Infrastructure
Reproducible Build Standards
Artifact Registry Specifications
Remote Build Execution Standards
```

They should only become normative after explicit adoption.

---

# Reference Adoption Rule

External standards should become normative only through explicit engineering decision.

The preferred process is:

```text id="dbe4fu"
Identify Need
      ↓
Evaluate Standard
      ↓
Architecture Decision
      ↓
Adopt
      ↓
Document
```

The framework must not accidentally inherit external requirements.

---

# Normative Versus Informative References

References should be distinguished conceptually as:

```text id="nmp1rz"
Normative
    ↓
Defines Required FamilyOS Behavior

Informative
    ↓
Provides Guidance Or Future Context
```

FamilyOS internal framework documents are typically normative when they define applicable requirements.

External standards remain informative unless explicitly adopted.

---

# Reference Precedence

When references conflict, precedence should generally follow:

```text id="293hpr"
FamilyOS Engineering Constitution
        ↓
Approved Architecture Decisions
        ↓
Normative FamilyOS Frameworks
        ↓
Approved Specifications
        ↓
Implementation Configuration
        ↓
External Guidance
```

The exact conflict should be resolved through governance rather than blindly applying this hierarchy.

---

# Reference Traceability

Significant Build Framework requirements should be traceable to their originating reference where appropriate.

For example:

```text id="j2cf9w"
Testing Requirement
      ↓
EPIC-TST-001

Quality Gate
      ↓
EPIC-QLT-001

Plugin Compliance
      ↓
EPIC-PLUGIN-002

Release Promotion
      ↓
EPIC-REL-001
```

This avoids duplicated ownership.

---

# Reference Maintenance

References must be reviewed when:

* documents are renamed;
* frameworks are superseded;
* ADRs are replaced;
* external standards are formally adopted;
* tools change significantly.

Broken or obsolete references reduce framework reliability.

---

# Reference Governance

Adding a reference does not automatically make it normative.

Normative status must be explicit.

Similarly, removing a normative reference may require architecture review if it changes framework obligations.

---

# Reference Anti-Pattern — Citation Without Relevance

A framework should not reference documents merely to appear comprehensive.

Every normative reference should have a clear relationship to Build Framework responsibilities.

---

# Reference Anti-Pattern — External Standard As Hidden Requirement

External standards must not silently become mandatory through implementation convenience.

---

# Reference Anti-Pattern — Duplicated Rules

If another FamilyOS framework owns a rule, Build Framework documentation should reference that rule rather than create a conflicting duplicate.

---

# Reference Anti-Pattern — Tool Documentation As Architecture

Documentation for a particular tool may explain implementation.

It must not replace FamilyOS architecture documentation.

---

# Reference Review Checklist

The Build Framework reference set should periodically verify:

1. all internal framework references remain valid;
2. renamed documents are updated;
3. superseded ADRs are identified;
4. RFC relationships remain current;
5. release references remain aligned;
6. implementation references reflect actual tooling;
7. external references are correctly classified;
8. no external standard is treated as normative without adoption;
9. Build Framework terminology remains synchronized with FamilyOS reference documentation.

---

# Core Reference Set

The minimum strategic reference set for EPIC-BLD-001 is:

```text id="2km3gj"
EPIC-ENG-001 — Engineering Foundation
EPIC-TST-001 — Testing Framework
EPIC-QLT-001 — Quality Framework
EPIC-DOC-001 — Documentation Framework
EPIC-PLUGIN-001 — Official Plugin Implementation
EPIC-PLUGIN-002 — Plugin Compliance Framework
EPIC-REL-001 — Release Framework
ADR-0007 — Official Plugins Architecture
FamilyOS Engineering Constitution
FamilyOS Architecture Vision
FamilyOS Security Architecture
FamilyOS Governance Architecture
```

Additional references may be added as implementation matures.

---

# External Core Reference Set

Current implementation may benefit from the following external reference areas:

```text id="54v9hj"
Python Packaging Standards
PEP 517
PEP 518
PEP 621
Python Wheel Specification
Python Source Distribution Standards
Reproducible Build Concepts
Software Supply Chain Assurance Concepts
```

External references remain subordinate to explicit FamilyOS architecture.

---

# Reference Success Criteria

The Build Framework reference model is successful when FamilyOS can answer:

1. which upstream framework defines engineering foundations;
2. which framework owns testing rules;
3. which framework owns quality gates;
4. which framework owns documentation standards;
5. which framework owns plugin compliance;
6. which framework owns release decisions;
7. which ADRs materially constrain build architecture;
8. which repository files define current implementation state;
9. which external packaging standards apply;
10. which external standards are only informative;
11. how conflicting requirements are escalated;
12. how references remain current over time.

---

# Reference Invariants

The following invariants should remain true.

## Invariant 1

FamilyOS normative architecture takes precedence over implementation convenience.

## Invariant 2

External standards are not normative unless explicitly adopted.

## Invariant 3

Build Framework must not duplicate ownership already assigned to another framework.

## Invariant 4

Tool documentation must not substitute for Build Architecture.

## Invariant 5

Release behavior must remain governed by EPIC-REL-001.

## Invariant 6

Testing behavior must remain governed by EPIC-TST-001.

## Invariant 7

Quality governance must remain governed by EPIC-QLT-001.

## Invariant 8

Plugin compliance must remain governed by EPIC-PLUGIN-002.

## Invariant 9

References must remain traceable and reviewable.

## Invariant 10

Obsolete references must be removed or explicitly marked historical.

---

# Reference Model Summary

The FamilyOS Build Framework reference hierarchy can be summarized as:

```text id="7pwn1u"
FamilyOS Foundations
      ↓
FamilyOS Frameworks
      ↓
Architecture Decisions
      ↓
Specifications
      ↓
Repository Implementation
      ↓
External Standards And Guidance
```

This hierarchy keeps Build Framework behavior anchored in FamilyOS architecture while allowing use of established external engineering standards.

---

# Final Principle

The FamilyOS Build Framework reference model is founded on the following rule:

> FamilyOS should reuse established architectural authority and industry standards where appropriate, but every build requirement must remain traceable to an explicit and understood source.

References exist to strengthen consistency.

They must not create ambiguity about ownership.

The Build Framework therefore uses references to connect artifact production with the larger FamilyOS Engineering Platform while preserving clear boundaries between architecture, implementation, governance, and external guidance.
