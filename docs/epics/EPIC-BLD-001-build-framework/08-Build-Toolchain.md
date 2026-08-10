# Build Framework

# 08 Build Toolchain

## Overview

EPIC-BLD-001 — Build Framework defines the toolchain model used to transform FamilyOS engineering state into validated build artifacts.

The build toolchain consists of the runtimes, package managers, build frontends, build backends, generators, validation tools, packaging tools, automation tools, and supporting utilities that participate in build execution.

The Build Framework does not define the toolchain merely as a collection of installed programs.

It defines the toolchain as a governed engineering dependency.

The central principle is:

> If a tool can materially influence build behavior or artifact output, it is part of the effective build context.

---

# Purpose

The purpose of the Build Toolchain model is to ensure that FamilyOS build behavior does not depend on arbitrary or undocumented tooling state.

The framework must provide clear expectations for:

* tool selection;
* tool purpose;
* supported versions;
* compatibility;
* installation;
* discovery;
* validation;
* upgrades;
* local usage;
* CI usage;
* traceability;
* security;
* governance.

The objective is not to freeze tooling indefinitely.

The objective is to allow tooling to evolve without losing build reliability.

---

# Toolchain Definition

A build toolchain is the collection of software capabilities required to execute, validate, package, and observe a build.

Conceptually:

```text
Build Toolchain
│
├── Runtime
├── Dependency Manager
├── Build Frontend
├── Build Backend
├── Packaging Tools
├── Generators
├── Validation Tools
├── Test Tools
├── Documentation Tools
├── Automation Tools
└── Supporting Utilities
```

Not every build profile requires every category.

---

# Toolchain As Build Input

The toolchain must be considered part of the build input model.

A simplified build relationship is:

```text
Source
   +
Configuration
   +
Dependencies
   +
Toolchain
   ↓
Build Result
```

Two builds using the same source but materially different toolchains may not be equivalent.

Therefore, significant toolchain state must remain identifiable.

---

# Toolchain Objectives

The FamilyOS Build Toolchain should provide:

* predictable behavior;
* reproducibility;
* local and CI consistency;
* maintainability;
* security;
* observability;
* upgradeability;
* compatibility with project architecture;
* minimal unnecessary complexity.

---

# Toolchain Principle 1 — Tools Follow Architecture

Tool selection must follow engineering requirements.

The correct decision flow is:

```text
Engineering Requirement
        ↓
Build Capability
        ↓
Architecture
        ↓
Tool Evaluation
        ↓
Tool Selection
```

The framework rejects the reverse model:

```text
Preferred Tool
      ↓
Build Architecture Designed Around Tool
```

Tools implement architecture.

They do not own it.

---

# Toolchain Principle 2 — Significant Tools Must Be Known

Any tool that can materially affect build output SHOULD have an identifiable version or supported version range.

Examples include:

* Python runtime;
* package builder;
* packaging backend;
* dependency manager;
* generator;
* formatter when generation depends on formatting;
* documentation generator;
* archive utility.

Unknown tooling weakens reproducibility.

---

# Toolchain Principle 3 — Tooling Must Be Discoverable

Canonical build tools must not depend on personal knowledge.

An engineer should be able to determine:

* which tools are required;
* where they are declared;
* how they are installed;
* how they are invoked;
* which versions are supported.

---

# Toolchain Principle 4 — Tooling Must Be Validated

The build process SHOULD validate important tooling prerequisites before execution.

For example:

```text
Required Python Version
        ↓
Detected Python Version
        ↓
Compatibility Check
        ↓
Proceed / Fail
```

This avoids late failures caused by unsupported tools.

---

# Toolchain Principle 5 — Local And CI Tooling Should Align

Local and CI execution should use compatible toolchain semantics.

The target is:

```text
Canonical Tool Requirements
          │
          ├── Local Environment
          └── CI Environment
```

The physical installation method may differ.

The effective tooling requirements should not.

---

# Toolchain Principle 6 — Toolchain Drift Must Be Controlled

Toolchain drift occurs when different environments silently use different versions or implementations.

For example:

```text
Developer A → Python X
Developer B → Python Y
CI          → Python Z
```

This may be acceptable only when all versions are intentionally supported.

Uncontrolled drift is not acceptable.

---

# Toolchain Principle 7 — Tool Upgrades Are Engineering Changes

A toolchain upgrade can change:

* build output;
* validation behavior;
* dependency resolution;
* performance;
* generated files;
* packaging metadata;
* compatibility.

Therefore, tool upgrades must be treated as engineering changes rather than routine background updates.

---

# Toolchain Layers

The FamilyOS toolchain can be understood through several layers.

```text
Toolchain
│
├── Runtime Layer
├── Dependency Layer
├── Build Layer
├── Validation Layer
├── Packaging Layer
├── Generation Layer
├── Documentation Layer
└── Automation Layer
```

These layers may use overlapping tools.

Their responsibilities should remain explicit.

---

# Runtime Layer

The runtime layer provides the execution environment for build tooling.

For the current FamilyOS implementation, Python is a central runtime.

Runtime requirements may include:

* supported Python version;
* virtual environment support;
* standard library compatibility;
* architecture compatibility.

The runtime is one of the most important toolchain inputs.

---

# Runtime Requirements

The runtime SHOULD be:

* explicitly supported;
* easy to reproduce;
* validated before canonical builds;
* consistent with package metadata;
* compatible with CI.

Unsupported runtime versions should fail clearly.

---

# Multiple Runtime Versions

FamilyOS may eventually support multiple runtime versions.

When this occurs, the build model must distinguish between:

```text
Supported Runtime Matrix
```

and:

```text
Canonical Build Runtime
```

The framework may support several runtime versions while selecting a canonical version for artifact creation.

---

# Dependency Management Layer

Dependency management tooling resolves and installs required packages.

Its responsibilities may include:

* dependency resolution;
* installation;
* lock handling;
* environment preparation;
* conflict detection.

Dependency management behavior directly affects reproducibility.

---

# Dependency Tool Requirements

Dependency tooling should support:

* explicit dependency declarations;
* repeatable installation;
* controlled resolution;
* compatible lock strategy;
* CI usage;
* local usage.

The build process should not depend on manually installed undeclared packages.

---

# Build Frontend Layer

A build frontend provides a user-facing mechanism for initiating package builds.

Conceptually:

```text
Build Command
    ↓
Build Frontend
    ↓
Build Backend
```

For Python packaging, this may involve standards-compatible tooling.

The exact implementation may evolve.

---

# Build Backend Layer

The build backend performs package construction according to project metadata.

Its responsibilities may include:

* source distribution generation;
* wheel generation;
* metadata processing;
* package discovery;
* resource inclusion.

The backend is a critical build dependency.

---

# Backend Requirements

The selected backend should be:

* standards-compatible where practical;
* maintainable;
* widely understood;
* compatible with FamilyOS packaging;
* automation-friendly;
* reproducible enough for platform needs.

Custom backends should not be introduced without clear justification.

---

# Packaging Layer

Packaging tools transform implementation state into distributable package formats.

For Python, artifact types may include:

```text
Wheel
Source Distribution
```

Future FamilyOS components may introduce additional formats.

The toolchain model must remain extensible.

---

# Packaging Requirements

Packaging tooling must support:

* canonical metadata;
* explicit package discovery;
* deterministic behavior where practical;
* validation;
* CI execution;
* release handoff.

---

# Validation Layer

Validation tools determine whether source, configuration, and artifacts satisfy engineering requirements.

Current FamilyOS validation capabilities may include tools for:

* linting;
* static typing;
* testing;
* packaging validation;
* documentation validation.

Validation tooling forms part of build trust.

---

# Static Analysis Tools

Static analysis may identify defects before artifact generation.

Examples include:

* lint errors;
* syntax problems;
* import issues;
* structural violations.

The Build Framework may invoke static analysis as part of validation profiles.

---

# Type Validation Tools

Static type validation strengthens source correctness.

For Python components, type checking may participate in the canonical validation pipeline.

Type validation remains governed by engineering and testing standards, while the Build Framework defines its role in build readiness.

---

# Test Tooling

Test tooling may execute:

* unit tests;
* integration tests;
* system tests;
* regression tests.

The Testing Framework owns test architecture.

The Build Toolchain owns how required test tooling becomes available to build validation.

---

# Artifact Validation Tools

Artifacts may require specialized validation.

Possible checks include:

* package structure;
* metadata;
* installability;
* archive integrity;
* dependency metadata;
* artifact contents.

Artifact validation tools should operate after artifact generation.

---

# Generation Layer

Generators transform controlled inputs into derived outputs.

Examples include:

* source generators;
* schema generators;
* metadata generators;
* manifest generators;
* documentation generators.

Generators are high-impact tooling because they directly create build inputs or outputs.

---

# Generator Requirements

Generators SHOULD be:

* versioned or identifiable;
* deterministic where feasible;
* documented;
* validated;
* associated with explicit source inputs;
* safe to rerun.

---

# Generated Output Stability

Generator upgrades may alter generated content even when source inputs remain unchanged.

Therefore, generator version changes should be evaluated for artifact impact.

---

# Documentation Toolchain

Documentation generation may participate in the build lifecycle.

Documentation tooling may perform:

* Markdown validation;
* index generation;
* API documentation generation;
* reference generation;
* packaging of documentation artifacts.

The Documentation Framework defines documentation standards.

The Build Framework governs execution and artifact production.

---

# Automation Layer

Automation tooling coordinates build execution in CI or other controlled environments.

Automation may include:

* CI runners;
* workflow systems;
* task runners;
* shell wrappers;
* orchestration scripts.

Automation tooling should call canonical build interfaces.

---

# CI Tooling Principle

The preferred relationship is:

```text
CI Platform
    ↓
Canonical Build Commands
```

The anti-pattern is:

```text
CI Platform
    ↓
Unique Build Implementation
```

---

# Supporting Utilities

Builds may rely on supporting utilities such as:

* archive tools;
* checksum tools;
* filesystem utilities;
* Git;
* shell utilities.

If such tools materially affect build output, their assumptions must be documented.

---

# Git As Toolchain Component

Git participates in build context when build identity or source state depends on:

* commit revision;
* tags;
* working tree status;
* branch metadata.

Git should therefore be treated as a relevant supporting tool for traceable builds.

---

# Shell Dependency

Shell scripts may provide useful orchestration.

However, build semantics should not depend excessively on shell-specific behavior.

Shell tooling should be:

* portable where required;
* explicit;
* simple;
* well-documented.

Complex build logic should not accumulate indefinitely in shell.

---

# Tool Installation Model

The Build Framework should support a clear method for acquiring required tooling.

A conceptual model is:

```text
Repository Configuration
        ↓
Tool Requirements
        ↓
Environment Preparation
        ↓
Installed Toolchain
```

The toolchain should not depend on ad hoc manual installation.

---

# Development Toolchain

The local development toolchain should enable engineers to:

* install dependencies;
* validate code;
* run tests;
* execute canonical builds;
* inspect artifacts.

It should remain close to CI semantics.

---

# CI Toolchain

CI should provision tooling from explicit definitions.

The target model is:

```text
Fresh CI Environment
       ↓
Declared Toolchain
       ↓
Canonical Build
```

A fresh CI environment is especially useful for detecting hidden local dependencies.

---

# Release Candidate Toolchain

Release-candidate builds may require stronger toolchain control.

Possible requirements include:

* canonical runtime version;
* explicit build-tool versions;
* reproducible dependency resolution;
* clean environment;
* validated packaging tools.

The exact rules should remain aligned with the Release Framework.

---

# Toolchain Version Policy

Tool versions may be controlled through:

* exact pins;
* compatible ranges;
* lock files;
* environment definitions;
* CI configuration.

The appropriate mechanism depends on tool criticality.

---

# Exact Pinning

Exact versions improve reproducibility but increase maintenance responsibility.

They are appropriate when:

* output varies by version;
* tool behavior is unstable;
* release trust requires exact identification.

---

# Version Ranges

Version ranges provide flexibility.

They may be appropriate when:

* compatibility is well-defined;
* tool behavior is stable;
* exact reproducibility is not required.

The tradeoff must be deliberate.

---

# Toolchain Locking

Future FamilyOS build environments may use stronger toolchain locking.

A conceptual toolchain lock could describe:

```text
Runtime Version
Build Frontend Version
Build Backend Version
Generator Versions
Validation Tool Versions
```

This is a maturity mechanism rather than an immediate universal requirement.

---

# Toolchain Compatibility Matrix

As FamilyOS grows, tool compatibility may need explicit modeling.

For example:

```text
Python Version
      ×
Build Backend
      ×
Dependency Set
      ↓
Supported Combination
```

A formal matrix should only be introduced when complexity justifies it.

---

# Toolchain Discovery

Build tooling should support discovering its effective toolchain.

A future command may conceptually expose:

```text
familyos build toolchain
```

with information such as:

```text
Python: ...
Builder: ...
Backend: ...
Ruff: ...
MyPy: ...
Pytest: ...
```

The specific command is not yet normative.

The capability is strategically useful.

---

# Toolchain Validation Flow

The canonical validation flow is:

```text
Identify Required Tools
        ↓
Discover Installed Tools
        ↓
Read Versions
        ↓
Check Compatibility
        ↓
Validated Toolchain
```

A mismatch should produce an actionable error.

---

# Toolchain Failure Classification

Possible failure categories include:

```text
MISSING_TOOL
UNSUPPORTED_TOOL_VERSION
INCOMPATIBLE_TOOLCHAIN
TOOL_EXECUTION_FAILURE
TOOL_CONFIGURATION_FAILURE
```

Formal machine-readable codes may be introduced later.

---

# Toolchain Observability

Build diagnostics should identify relevant tools.

For significant builds, evidence may include:

* runtime version;
* build frontend version;
* backend version;
* generator versions;
* validation tool versions.

This improves reproducibility and incident investigation.

---

# Toolchain Evidence

Toolchain evidence can become part of the Build Evidence model.

Conceptually:

```text
Build Evidence
│
└── Toolchain
    ├── Runtime
    ├── Builder
    ├── Backend
    ├── Validators
    └── Generators
```

Evidence strength depends on profile.

---

# Toolchain Security

Build tools execute with access to source and may produce trusted artifacts.

They therefore form part of the software supply chain.

Security considerations include:

* trusted distribution source;
* dependency integrity;
* compromised packages;
* malicious plugins;
* unsafe generators;
* excessive permissions.

Tool acquisition must remain controlled.

---

# Tool Source Trust

Canonical build tools should come from trusted and documented sources.

Unverified binaries or scripts should not become required build dependencies.

---

# Tool Integrity

Future stronger build profiles may verify tooling integrity through:

* hashes;
* signed packages;
* locked dependency sets;
* trusted registries.

These controls may be added as FamilyOS supply-chain maturity grows.

---

# Tool Privileges

Build tools should operate with minimum required privileges.

They should not automatically receive:

* release publication credentials;
* deployment access;
* production secrets.

This preserves separation of responsibilities.

---

# Tool Configuration

Tool configuration is part of the effective toolchain.

A tool and its configuration together determine behavior.

Therefore:

```text
Tool Version
    +
Tool Configuration
    ↓
Tool Behavior
```

Both should remain controlled.

---

# Shared Tool Configuration

Where multiple environments use the same tool, configuration should be shared where practical.

The preferred model is:

```text
Canonical Tool Configuration
          │
          ├── Local
          └── CI
```

This reduces drift.

---

# Local Overrides

Local overrides may be useful for developer ergonomics.

They must not silently redefine canonical build behavior.

Overrides that affect trusted build output should be explicit.

---

# Toolchain Upgrades

Toolchain upgrades should follow a controlled lifecycle.

```text
Identify Upgrade
      ↓
Review Changes
      ↓
Update Tool
      ↓
Run Validation
      ↓
Compare Artifacts
      ↓
Document Impact
      ↓
Adopt
```

The depth of review depends on tool significance.

---

# Runtime Upgrade

A runtime upgrade may affect:

* syntax;
* dependency compatibility;
* package output;
* type checking;
* tests;
* performance.

Runtime upgrades are therefore high-impact toolchain changes.

---

# Builder Upgrade

A package builder upgrade may affect:

* metadata;
* archive layout;
* package discovery;
* generated filenames;
* reproducibility.

Artifacts should be compared when such changes are significant.

---

# Validation Tool Upgrade

Validation tools may introduce:

* new rules;
* stricter behavior;
* removed checks;
* changed defaults.

Tool upgrades should not silently alter quality expectations.

---

# Toolchain Deprecation

Obsolete tools should be removed from canonical build workflows.

Deprecation should include:

* replacement path;
* migration period where needed;
* configuration cleanup;
* documentation updates.

Leaving multiple obsolete paths creates toolchain ambiguity.

---

# Single Toolchain Source Of Truth

FamilyOS should avoid maintaining conflicting toolchain definitions.

The anti-pattern is:

```text
Developer Guide Version
CI Version
Shell Script Version
Local Setup Version
```

with different values.

The target is:

```text
Canonical Tool Requirements
         ↓
All Execution Environments
```

---

# Toolchain And Build Profiles

Different profiles may use different subsets of the toolchain.

For example:

```text
Development
├── Runtime
├── Linter
├── Type Checker
├── Tests
└── Builder
```

while:

```text
Release Candidate
├── Runtime
├── Dependency Manager
├── Linter
├── Type Checker
├── Tests
├── Builder
├── Artifact Validator
└── Evidence Tools
```

Profile differences must remain explicit.

---

# Toolchain And Plugins

Official plugins may require additional tooling.

Examples include:

* schema generation;
* plugin packaging;
* compliance validation.

Plugin-specific tools must not weaken platform toolchain governance.

---

# Toolchain And Documentation

Documentation tooling should be integrated through the same principles:

* declared;
* version-aware;
* automation-friendly;
* reproducible where practical.

Generated documentation should not depend on undocumented local tools.

---

# Toolchain And Testing

Testing tools are governed primarily by the Testing Framework.

The Build Framework ensures that required testing tools are available and correctly integrated into build validation.

---

# Toolchain And Quality

Quality tools may participate in build gates.

The Build Framework must expose their results but should not redefine quality governance.

---

# Toolchain And Release

The Release Framework may require stronger toolchain controls for official artifacts.

The Build Framework should provide enough toolchain evidence to support release decisions.

---

# Toolchain Portability

The Build Framework should avoid unnecessary platform-specific tooling.

Where platform-specific tools are required, that dependency must be explicit.

Portability supports:

* developer consistency;
* CI flexibility;
* future platform support.

---

# Toolchain Isolation

Build environments should isolate tool versions sufficiently to prevent accidental interference from globally installed tooling.

Virtual environments are one practical mechanism for Python.

Future mechanisms may include containers or dedicated builders.

The principle is more important than the specific technology.

---

# Global Tool Anti-Pattern

The canonical build should not rely on undocumented globally installed packages.

For example:

```text
pip install some-tool
```

performed months earlier on a developer machine must not be the only reason the build succeeds.

---

# CI-Only Tool Anti-Pattern

Critical tools must not exist only inside CI configuration without local documentation or equivalent setup.

Developers should be able to understand the canonical toolchain.

---

# Latest-Version Anti-Pattern

Build definitions should avoid uncontrolled dependencies such as:

```text
install latest version
```

when tool behavior can materially change build output.

Tool version strategy must be intentional.

---

# Hidden Generator Anti-Pattern

Generated output should not depend on unknown local generator versions.

Generator identity must remain traceable where output matters.

---

# Duplicate Tool Anti-Pattern

FamilyOS should avoid multiple tools solving the same build concern without a clear reason.

Examples include multiple:

* formatters;
* package builders;
* dependency managers;
* task runners.

Tool proliferation increases cognitive and maintenance cost.

---

# Tool Selection Criteria

When evaluating a new build tool, FamilyOS should consider:

* architectural fit;
* standards compatibility;
* maintenance activity;
* security posture;
* community maturity;
* documentation quality;
* reproducibility;
* automation support;
* local usability;
* migration cost;
* lock-in risk.

Tool popularity alone is insufficient.

---

# Tool Introduction Process

A new significant tool should follow:

```text
Need Identified
     ↓
Existing Capability Review
     ↓
Tool Evaluation
     ↓
Impact Analysis
     ↓
Adoption Decision
     ↓
Documentation
     ↓
Validation
```

Architectural tools may require ADR governance.

---

# Tool Removal Process

Removing a tool should verify:

* no canonical workflow depends on it;
* documentation is updated;
* CI no longer uses it;
* configuration is removed;
* replacement behavior is validated.

---

# Toolchain Governance

Significant toolchain decisions should remain governed.

Examples include:

* changing primary runtime;
* changing build backend;
* changing dependency management architecture;
* introducing custom build orchestration;
* introducing artifact signing tools;
* introducing remote build infrastructure.

These may require ADR or RFC treatment.

---

# Toolchain Debt

Toolchain debt includes:

* obsolete tools;
* duplicated tools;
* unpinned critical tools;
* undocumented dependencies;
* CI-only tooling;
* fragile scripts;
* incompatible version ranges.

Toolchain debt should be tracked and reduced.

---

# Toolchain Metrics

Potential future toolchain metrics include:

* setup failure rate;
* tool mismatch rate;
* runtime incompatibility rate;
* tool upgrade frequency;
* build failures caused by tooling;
* CI/local toolchain divergence.

Metrics should only be introduced when they support real decisions.

---

# Toolchain Maintenance

Toolchain maintenance should be continuous but controlled.

Regular activities may include:

* dependency updates;
* runtime upgrades;
* tool updates;
* configuration cleanup;
* security review;
* deprecation removal.

Maintenance must not become uncontrolled version churn.

---

# Toolchain Reproducibility

Reproducible builds require sufficient control over toolchain state.

A stronger future model may be:

```text
Toolchain Definition
        ↓
Environment Provisioning
        ↓
Validated Toolchain
        ↓
Build
```

This can evolve toward immutable or declarative build environments if needed.

---

# Toolchain Maturity Model

FamilyOS toolchain maturity may progress through:

```text
Level 1
Documented Tools

    ↓

Level 2
Declared Tool Requirements

    ↓

Level 3
Version-Controlled Tooling

    ↓

Level 4
Automated Tool Validation

    ↓

Level 5
Reproducible Tool Environments

    ↓

Level 6
Toolchain Provenance
```

The framework supports this progression without requiring immediate implementation of every level.

---

# Current FamilyOS Toolchain Context

The current FamilyOS engineering environment already uses a coherent Python-oriented toolchain.

Examples include capabilities for:

* Python execution;
* virtual environments;
* dependency management;
* Ruff validation;
* MyPy validation;
* Pytest execution;
* Git version control.

EPIC-BLD-001 formalizes how such tools participate in a canonical Build Framework.

The framework does not require replacing stable tools merely to achieve architectural symmetry.

---

# Toolchain Success Criteria

The Build Toolchain model is successful when FamilyOS can answer:

1. which runtime is required;
2. which build tools are required;
3. which versions are supported;
4. how tools are installed;
5. how tool compatibility is validated;
6. whether local and CI toolchains are aligned;
7. which tools influenced a particular build;
8. how tool upgrades are governed;
9. which tool generated a particular derived output;
10. whether unsupported tooling can be detected before execution;
11. how security-sensitive tool acquisition is controlled;
12. how obsolete tooling is retired.

---

# Toolchain Invariants

The following invariants should remain true.

## Invariant 1

Critical build tools must be identifiable.

## Invariant 2

Required tools must be discoverable from project documentation or configuration.

## Invariant 3

Unsupported critical tool versions must not silently proceed.

## Invariant 4

CI must not invent independent build semantics through different tools.

## Invariant 5

Tool upgrades must remain reviewable.

## Invariant 6

Required tooling must not depend on personal workstation state.

## Invariant 7

Toolchain changes must not bypass validation.

## Invariant 8

Tool privileges must remain proportional to build responsibility.

---

# Toolchain Summary

The canonical FamilyOS Build Toolchain model is:

```text
Engineering Requirements
        ↓
Tool Requirements
        ↓
Tool Selection
        ↓
Tool Version Strategy
        ↓
Environment Provisioning
        ↓
Tool Validation
        ↓
Canonical Build Execution
        ↓
Toolchain Evidence
```

This model transforms tooling from an implicit workstation characteristic into a governed part of the Build Framework.

---

# Final Principle

The FamilyOS Build Toolchain is founded on the following rule:

> Tools may change, but the build must never become dependent on tooling that FamilyOS cannot identify, validate, reproduce, or govern.

The Build Framework therefore treats the toolchain as part of the engineering system itself.

A reliable source tree with an uncontrolled toolchain does not produce a reliable build.

A trustworthy FamilyOS build requires both controlled engineering inputs and controlled transformation mechanisms.
