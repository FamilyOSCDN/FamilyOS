# Build Framework

# 07 Build Inputs and Project Structure

## Overview

EPIC-BLD-001 — Build Framework defines how FamilyOS project structure supports reliable, reproducible, and maintainable build engineering.

Project structure is not merely an organizational concern.

Directory layout, file ownership, build configuration location, generated content placement, artifact destinations, and repository boundaries directly influence:

* build reproducibility;
* input discoverability;
* dependency resolution;
* automation;
* validation;
* developer experience;
* artifact management;
* governance.

The purpose of this document is to establish the structural expectations that allow FamilyOS build inputs and outputs to remain predictable, traceable, and easy to govern.

---

# Purpose

The Build Inputs and Project Structure model defines how build-relevant content should be organized across the FamilyOS repository.

It establishes expectations for:

* authoritative source locations;
* build configuration placement;
* dependency declarations;
* generated content;
* build tooling;
* temporary state;
* output directories;
* artifact locations;
* documentation inputs;
* plugin inputs;
* validation resources.

The central principle is:

> Build structure must make build behavior easier to understand, not harder to discover.

---

# Structural Objective

The FamilyOS project structure should allow an engineer to answer:

```text id="sy3mk4"
Where are the authoritative sources?

Where is build configuration defined?

Where are dependencies declared?

Where are generated inputs produced?

Where do temporary outputs go?

Where are final artifacts written?

Which files are part of the build contract?

Which files are implementation details?
```

The repository should make these boundaries visible.

---

# Canonical Structural Model

A conceptual FamilyOS build-oriented project structure is:

```text id="75anua"
Repository
│
├── Source
├── Tests
├── Documentation
├── Configuration
├── Build Tooling
├── Generated Inputs
├── Build Outputs
├── Validation Outputs
└── Release Inputs
```

The physical structure may evolve.

The conceptual responsibilities should remain distinct.

---

# Repository As Build Source Of Truth

The FamilyOS repository is the primary authoritative source for build-relevant engineering state.

Where practical, the repository should contain or reference:

* source;
* build configuration;
* dependency declarations;
* package metadata;
* tool configuration;
* schemas;
* templates;
* generators;
* validation definitions;
* CI configuration.

This supports the relationship:

```text id="nivgxo"
Repository State
      ↓
Resolved Build Context
```

---

# Structural Principle 1 — Authoritative Inputs Must Be Discoverable

Authoritative build inputs should exist in predictable locations.

Examples include:

* source under canonical source directories;
* dependencies in defined project configuration;
* build configuration in known configuration files;
* plugin metadata in defined plugin locations;
* documentation sources under documentation directories.

The build must not require engineers to search arbitrary filesystem locations.

---

# Structural Principle 2 — Source And Generated Content Must Be Distinguishable

Authoritative source and generated content must not be confused.

The preferred model is:

```text id="baui1n"
Authoritative Source
        ↓
Generator
        ↓
Generated Content
```

The repository structure should make this relationship clear.

Generated content must not silently replace authoritative source.

---

# Structural Principle 3 — Temporary State Must Be Isolated

Temporary build state should be structurally separated from source.

Examples include:

* cache directories;
* temporary working directories;
* intermediate package outputs;
* tool-generated scratch files.

The preferred model is:

```text id="yweos4"
Repository Source
       │
       └──── isolated from ──── Build Temporary State
```

Temporary state should be safely removable.

---

# Structural Principle 4 — Final Artifacts Must Have Predictable Destinations

Build artifacts should be written into known locations.

This improves:

* automation;
* CI artifact collection;
* cleanup;
* validation;
* release handoff.

Artifacts should not appear unpredictably throughout the repository.

---

# Structural Principle 5 — Build Configuration Must Be Centralized Where Practical

The project should avoid scattering equivalent build rules across multiple independent files.

The preferred pattern is:

```text id="eqg1p4"
Canonical Configuration
        ↓
Build Tools
```

rather than:

```text id="p9y19j"
Config A
Config B
CI Override
Shell Override
Local Notes
```

with conflicting semantics.

---

# Structural Principle 6 — Build Tooling Must Be Discoverable

Custom build scripts or generators must exist in defined locations.

Build tooling should not depend on:

* personal scripts;
* undocumented aliases;
* arbitrary external directories;
* untracked helper files.

If tooling is required by the canonical build, it must be discoverable through the project.

---

# Structural Principle 7 — Repository Layout Must Support Automation

CI systems should be able to locate canonical build inputs without machine-specific logic.

Automation should derive build behavior from repository structure and canonical configuration.

This enables:

```text id="pbbdh9"
Clone Repository
      ↓
Resolve Known Structure
      ↓
Execute Canonical Build
```

---

# Source Structure

FamilyOS source code should remain organized according to the architectural conventions defined by the Engineering Foundation.

For Python components, a typical structure may include:

```text id="1u8v5n"
src/
└── familyos_cli/
    ├── core/
    ├── plugins/
    ├── services/
    └── ...
```

The Build Framework does not redefine application architecture.

It defines how that structure participates in artifact production.

---

# Source Structure Requirements

Source directories should:

* contain authoritative implementation state;
* avoid build-generated noise;
* remain importable according to project packaging rules;
* remain compatible with static validation;
* avoid dependency on build output directories.

Build output must never become an implicit source dependency unless explicitly designed.

---

# Package Structure

Python package layout influences:

* package discovery;
* metadata generation;
* artifact construction;
* test installation;
* release packaging.

Package structure must therefore remain compatible with canonical packaging configuration.

---

# Package Discovery

Package discovery should be explicit or based on predictable conventions.

The build system should not accidentally package:

* tests not intended for distribution;
* temporary files;
* local configuration;
* secrets;
* caches;
* development-only artifacts.

Package boundaries must be intentional.

---

# Test Structure

Tests are not generally primary build artifacts, but they participate in build validation.

A canonical project may include:

```text id="fhskef"
tests/
├── unit/
├── integration/
└── ...
```

The Build Framework must be able to invoke testing without treating test outputs as application artifacts.

---

# Test Inputs

Test execution may consume:

* source;
* fixtures;
* test configuration;
* generated artifacts;
* installed packages.

The project structure must allow these dependencies to remain explicit.

---

# Documentation Structure

Documentation is both an engineering input and, potentially, a build output.

A canonical structure may include:

```text id="opaguy"
docs/
├── 00-foundation/
├── epics/
├── specifications/
├── reference/
└── ...
```

Documentation builds may consume this structure for generation or validation.

---

# Documentation Inputs

Build-related documentation inputs may include:

* Markdown;
* metadata;
* diagrams;
* indexes;
* manifests;
* specifications.

Generated documentation should remain distinguishable from authored sources.

---

# Project Configuration Structure

Build configuration should use canonical project-level configuration wherever supported.

In Python projects this may include:

```text id="iu9f7h"
pyproject.toml
```

This may define or reference:

* package metadata;
* build backend;
* dependencies;
* tool configuration;
* packaging rules.

The Build Framework does not require all configuration to exist in one file, but equivalent concerns should not be duplicated unnecessarily.

---

# Tool Configuration

Tool configuration may include:

* Ruff;
* MyPy;
* Pytest;
* packaging tools;
* documentation generators;
* code generation tools.

Where possible, configuration should be kept close to project-level engineering state.

This improves discoverability.

---

# Dependency Structure

Dependency declarations should have canonical locations.

For Python, the authoritative dependency model may be expressed through project metadata and associated lock mechanisms.

The exact mechanism may evolve.

The structural requirement is stable:

```text id="34dlks"
Dependency Declaration
       ↓
Known Location
       ↓
Controlled Resolution
```

---

# Lock Files

When lock files are used, they must have clearly defined ownership and purpose.

They should not exist as unexplained duplicates.

For example, separate lock states for different purposes must be intentional and documented.

---

# Build Tool Structure

Custom build tooling should be grouped predictably.

A future layout may conceptually resemble:

```text id="4dhfkw"
tools/
└── build/
    ├── ...
```

or another repository-approved location.

The exact directory name is less important than consistency and discoverability.

---

# Script Structure

Build scripts should have narrow and explicit responsibilities.

Avoid large script files that simultaneously perform:

* dependency installation;
* generation;
* packaging;
* validation;
* release publication.

Separation improves maintainability and governance.

---

# Generator Structure

Generators should have explicit source and destination relationships.

For example:

```text id="u4s9ok"
Generator Code
      ↓
Input Schema
      ↓
Generated Output
```

The location of generator code and generated content should make that relationship understandable.

---

# Generated Source Structure

Generated source may require special treatment.

Possible strategies include:

* generated at build time;
* generated and committed;
* generated into temporary build directories.

The selected strategy must be explicit.

---

# Generated Source Requirements

Generated source must have:

* authoritative source;
* generator identity;
* generation procedure;
* destination;
* freshness rules;
* validation.

Generated source should not become manually edited shadow source.

---

# Resource Structure

Resources may include:

* templates;
* configuration assets;
* schemas;
* static files;
* localization data.

If included in artifacts, their packaging rules must be explicit.

---

# Resource Inclusion

The Build Framework must prevent accidental inclusion or omission.

Resource inclusion should be governed through explicit package or build configuration.

---

# Plugin Structure

FamilyOS official plugins have their own project structure.

A plugin may contain:

```text id="fhjw1o"
plugin/
├── capabilities/
├── models/
├── entities/
├── services/
├── repositories/
├── policies/
├── rules/
├── templates/
├── cli/
└── metadata
```

The exact structure depends on the Plugin Architecture.

The Build Framework consumes this structure as build input.

---

# Plugin Build Inputs

Plugin-specific build inputs may include:

* plugin metadata;
* capability declarations;
* policies;
* rules;
* templates;
* configuration;
* compliance definitions.

These inputs must remain discoverable within the plugin structure.

---

# Plugin Artifact Structure

Plugin artifacts should have predictable packaging boundaries.

The build process should know:

```text id="v4o3mx"
What belongs to the plugin artifact?

What belongs only to development?

What belongs only to tests?

What belongs only to documentation?
```

---

# Compliance Structure

Plugin compliance evidence may exist in:

* validation output;
* reports;
* manifests;
* generated evidence bundles.

Compliance output should not be mixed with authoritative plugin source.

---

# Build Output Structure

Build output should be isolated from source.

A common conceptual output structure is:

```text id="nqpaeb"
build/
dist/
```

The Build Framework does not mandate these exact names.

The requirement is predictable separation.

---

# Build Output Categories

Outputs may be classified as:

```text id="ff25bb"
Intermediate
Temporary
Final Artifact
Validation Report
Evidence
```

These categories should not be conflated.

---

# Intermediate Output

Intermediate outputs are produced during transformation but are not final artifacts.

Examples include:

* temporary package staging;
* generated intermediate files;
* extracted metadata;
* compiler intermediates.

They should be safely regenerable.

---

# Final Artifact Output

Final artifacts are candidate technical outputs intended for validation and possible release handoff.

Examples include:

* wheels;
* source distributions;
* bundles;
* generated documentation packages.

Final artifact directories must be stable and easy to collect.

---

# Validation Output Structure

Validation may produce:

* reports;
* logs;
* coverage;
* compliance evidence;
* integrity reports.

These outputs should be distinguishable from distributable artifacts.

---

# Evidence Output Structure

Build evidence may eventually be stored in a structured area.

Conceptually:

```text id="5sjypc"
build-evidence/
├── build-manifest
├── validation-results
├── artifact-manifest
└── provenance
```

The exact physical structure may evolve.

---

# Release Input Structure

Trusted artifacts intended for release should be handed off through a controlled boundary.

The Release Framework should not discover arbitrary files throughout the repository.

The preferred relationship is:

```text id="tllq5h"
Build Output
     ↓
Validated Artifact Set
     ↓
Release Input
```

---

# Repository Cleanliness

Build execution must not unnecessarily dirty the repository.

A normal build should avoid modifying authoritative source unless generation is intentionally part of the workflow.

The preferred expectation is:

```text id="mvpc80"
Clean Repository
      ↓
Build
      ↓
Clean Repository
      +
Artifacts Outside Source
```

---

# Dirty Build State

If build execution changes tracked files unexpectedly, that indicates one of:

* stale generated content;
* misconfigured generation;
* unintended mutation;
* repository drift.

Such behavior should be investigated.

---

# Ignored Build Outputs

Temporary and generated build outputs should normally be represented appropriately in ignore configuration.

This may include:

* caches;
* virtual environments;
* build directories;
* distribution directories;
* tool caches.

Ignore rules should not conceal authoritative files.

---

# Version-Controlled Generated Outputs

Some generated content may intentionally remain version controlled.

If so, the project must define:

* why it is committed;
* how it is regenerated;
* how freshness is checked;
* who owns updates.

This prevents ambiguity.

---

# Build Path Portability

Build paths should be portable.

The project should prefer:

* repository-relative paths;
* normalized path resolution;
* configuration-derived locations.

It should avoid:

* user-specific absolute paths;
* workstation-specific mount points;
* shell-dependent assumptions.

---

# Path Resolution Model

The preferred model is:

```text id="9692re"
Repository Root
      ↓
Canonical Relative Path
      ↓
Resolved Build Input
```

---

# Repository Root Detection

Build tooling should have a reliable method for identifying project root.

It should not depend on arbitrary current working directory assumptions unless explicitly documented.

---

# Working Directory Independence

Where practical, canonical build commands should behave predictably when invoked through their documented entry point.

Internal path resolution should not rely excessively on invocation location.

---

# Monorepository Considerations

FamilyOS may contain multiple components within one repository.

The Build Framework must therefore support clear component boundaries.

A build target should be able to identify:

* component root;
* source set;
* dependency scope;
* artifact output;
* validation scope.

---

# Component Boundary

A component should not accidentally consume unrelated repository content.

The preferred model is:

```text id="3f2156"
Repository
│
├── Component A Inputs
│      ↓
│   Artifact A
│
└── Component B Inputs
       ↓
    Artifact B
```

Shared inputs must be explicit.

---

# Cross-Component Inputs

Shared schemas, templates, or libraries may be legitimate cross-component inputs.

Their ownership and versioning must be clear.

Cross-component dependencies should not emerge through relative path shortcuts without architectural intent.

---

# Build Target Structure

The build system may eventually define explicit build targets.

A conceptual target might include:

```text id="10sr94"
BuildTarget
│
├── Component Root
├── Source Set
├── Configuration
├── Dependencies
├── Artifact Definition
└── Validation Rules
```

The current implementation may remain simpler.

---

# Artifact Naming Structure

Artifacts should use predictable naming.

Naming should communicate enough information to avoid ambiguity.

Depending on artifact type, names may include:

* component;
* version;
* platform;
* architecture;
* package format.

The exact naming convention should align with release standards.

---

# Artifact Directory Isolation

Different build profiles should avoid overwriting each other's outputs unexpectedly.

For example:

```text id="a8sfzx"
development output
ci output
release-candidate output
```

may need separate logical identities even if physical storage is shared.

---

# Build Profile Structure

Profile-specific configuration should remain structured and predictable.

Profiles must not become collections of undocumented shell behavior.

Possible organization may include:

```text id="pkpncz"
build-profiles/
├── development
├── ci
└── release-candidate
```

or equivalent configuration.

The conceptual separation matters more than the exact directory.

---

# CI Structure

CI configuration should remain easy to locate.

It should reference canonical build commands rather than duplicate implementation logic.

The preferred structure is:

```text id="9vwewo"
CI Workflow
    ↓
Canonical Build Entry Point
```

---

# CI Artifact Collection

CI should collect artifacts from canonical output locations.

It should not need to search the entire repository for generated files.

---

# Local Development Structure

Local development should use the same canonical project layout.

Developers should not require personal directory structures to make builds succeed.

Virtual environments or local caches may exist outside authoritative source boundaries.

---

# Virtual Environment Structure

Virtual environments are execution environments, not project source.

They should remain clearly separated from authoritative inputs.

A local virtual environment may be:

```text id="rbxwq3"
.venv/
```

or another controlled location.

Its installed state must not become the only record of required dependencies.

---

# Cache Structure

Caches may include:

* dependency caches;
* tool caches;
* test caches;
* build caches.

Caches are optimizations.

They must not become authoritative inputs.

---

# Cache Independence

A valid clean build should remain possible without caches.

Conceptually:

```text id="qcpo8h"
Cache Present
     ↓
Fast Build

Cache Missing
     ↓
Valid Build
```

The semantic result should remain equivalent.

---

# Temporary Directory Structure

Temporary directories should be:

* disposable;
* isolated;
* excluded from authoritative source;
* safely cleanable.

The build should not depend on stale temporary state.

---

# Clean Build Structure

The project structure should make clean builds straightforward.

A clean operation should be able to remove:

* intermediates;
* caches where appropriate;
* generated temporary content;
* final build output if requested;

without deleting authoritative source.

---

# Structural Validation

The Build Framework may validate repository structure.

Possible checks include:

* required directory presence;
* required metadata;
* invalid duplicate configuration;
* misplaced build output;
* unexpected generated files;
* missing artifact directories.

These checks should remain proportional to actual value.

---

# Structural Drift

Structural drift occurs when build-related files accumulate outside the canonical model.

Examples include:

* additional build scripts in random directories;
* duplicate package configuration;
* abandoned output directories;
* obsolete generated folders.

Structural drift should be treated as technical debt.

---

# Repository And Reproducibility

A predictable project structure strengthens reproducibility.

When inputs are consistently located and outputs are isolated:

```text id="bi9hrd"
Known Repository Layout
        ↓
Reliable Input Discovery
        ↓
Repeatable Build
```

---

# Repository And Traceability

Project structure also supports traceability.

An artifact can be traced back through:

```text id="0z9i2m"
Artifact
   ↓
Build Target
   ↓
Input Paths
   ↓
Repository Revision
```

---

# Repository And Automation

Automation benefits from structural consistency.

CI should not require repository-specific heuristics for each build.

The canonical structure should expose enough information for deterministic automation.

---

# Repository And Security

Repository structure also influences security.

Sensitive material should not be placed in ordinary source or build-output directories.

Examples include:

* private keys;
* credentials;
* secret configuration.

Build structure must support clear secret boundaries.

---

# Repository And Governance

Changes to canonical project structure may affect multiple frameworks.

Significant structural changes should therefore consider:

* Engineering Foundation;
* Documentation Framework;
* Testing Framework;
* Build Framework;
* Plugin Architecture;
* Release Framework.

Architectural changes may require ADR governance.

---

# Structural Anti-Pattern — Build Outputs Inside Source

The following pattern should be avoided:

```text id="i22maz"
src/
├── source.py
├── generated-build-output.bin
└── package.zip
```

unless the output is intentionally authoritative generated source.

---

# Structural Anti-Pattern — Duplicate Configuration

Avoid:

```text id="2d21q6"
pyproject.toml
build-config.yaml
ci-build-config.yaml
release-build-config.yaml
```

all redefining overlapping rules without an explicit precedence model.

---

# Structural Anti-Pattern — Personal Tooling

Avoid canonical build dependencies such as:

```text id="t4o6yn"
/Users/developer/scripts/build.sh
```

Required build tooling must belong to controlled project state or governed external tooling.

---

# Structural Anti-Pattern — Unclear Generated Content

Avoid directories where engineers cannot determine whether files are:

* authored;
* generated;
* temporary;
* distributable.

Every important directory should have a clear role.

---

# Structural Anti-Pattern — Release Discovery By Guessing

The Release Framework should not need logic such as:

```text id="79plmd"
find repository -name "*.whl"
```

to determine official candidate artifacts.

Artifact handoff must be explicit.

---

# Structural Extensibility

The project structure must allow future build capabilities without uncontrolled growth.

Potential future additions may include:

* dedicated artifact metadata;
* provenance records;
* generated API schemas;
* multiple runtime targets;
* build manifests;
* signing outputs.

New directories should have explicit responsibilities.

---

# Structural Simplicity

The framework must avoid creating directories merely to mirror conceptual architecture.

Physical structure should remain as simple as possible.

The rule is:

```text id="2l9i18"
Conceptual Separation
        ≠
Mandatory Directory Explosion
```

Directory boundaries should exist where they improve clarity or tooling.

---

# Current FamilyOS Context

The current FamilyOS repository already contains established areas such as:

```text id="x9skv5"
src/
tests/
docs/
```

and project-level engineering configuration.

The Build Framework should evolve from this existing structure rather than introducing unnecessary parallel organization.

---

# Migration Principle

Existing project structure should be improved incrementally.

The preferred approach is:

```text id="ma97kr"
Existing Structure
       ↓
Identify Build Ambiguity
       ↓
Introduce Minimal Correction
       ↓
Validate
       ↓
Standardize
```

Large-scale restructuring should only occur when justified.

---

# Structure Ownership

Structural ownership should remain clear.

Conceptually:

```text id="9s1xy6"
Application Source
      → Engineering / Domain Owners

Build Configuration
      → Build / Engineering Owners

Plugin Structure
      → Plugin Owners + Platform Governance

Documentation Structure
      → Documentation Governance

Release Handoff
      → Build + Release Governance
```

Shared ownership should be documented.

---

# Structural Documentation

Important repository structure must be documented.

Documentation should explain:

* canonical source locations;
* build configuration;
* generated content;
* build outputs;
* artifact locations;
* temporary state;
* cleanup expectations.

This prevents architecture from becoming implicit.

---

# Structural Success Criteria

The project structure is build-ready when FamilyOS can answer:

1. where authoritative source lives;
2. where build configuration lives;
3. where dependency state is declared;
4. where build tooling lives;
5. where generated inputs live;
6. which generated content is authoritative;
7. where temporary state is stored;
8. where build outputs are produced;
9. where validation evidence is written;
10. which artifacts are eligible for release handoff;
11. which directories can safely be cleaned;
12. which paths must never contain secrets;
13. how plugins participate in build structure;
14. how automation discovers canonical inputs.

---

# Structural Invariants

The following invariants should remain true.

## Invariant 1

Authoritative source must be distinguishable from generated build output.

## Invariant 2

Temporary state must not become authoritative by accident.

## Invariant 3

Canonical build configuration must remain discoverable.

## Invariant 4

Required tooling must not depend on personal filesystem paths.

## Invariant 5

Artifacts must have predictable output locations.

## Invariant 6

Release handoff must use identified artifacts rather than arbitrary files.

## Invariant 7

Caches must remain optional optimizations.

## Invariant 8

Project structure must support clean builds.

---

# Structural Model Summary

The FamilyOS Build Project Structure can be summarized as:

```text id="nn930v"
Repository
│
├── Authoritative Inputs
│   ├── Source
│   ├── Configuration
│   ├── Dependencies
│   ├── Metadata
│   └── Documentation
│
├── Controlled Tooling
│   ├── Build
│   ├── Generation
│   └── Validation
│
├── Derived State
│   ├── Generated Inputs
│   ├── Temporary State
│   └── Cache
│
└── Outputs
    ├── Artifacts
    ├── Validation Evidence
    └── Release Handoff
```

---

# Final Principle

The FamilyOS Build Inputs and Project Structure model is founded on the following rule:

> The repository structure must make it obvious what the build consumes, what it transforms, what it generates, and what can safely progress downstream.

A predictable project structure reduces hidden state.

It improves reproducibility.

It strengthens automation.

It simplifies validation.

It improves artifact traceability.

And it ensures that FamilyOS build engineering remains maintainable as the platform grows.
