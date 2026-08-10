# Build Framework

# 10 Dependency Management

## Overview

EPIC-BLD-001 — Build Framework defines how FamilyOS manages dependencies that influence build behavior, validation, artifact production, and reproducibility.

Dependencies are not secondary implementation details.

They are part of the effective build state.

A build may use identical FamilyOS source code and still produce different outcomes if dependency resolution changes.

The purpose of this document is therefore to define how dependencies are declared, classified, resolved, validated, locked, updated, secured, observed, and governed.

The central principle is:

> A trusted build requires dependency state that is explicit, controlled, and explainable.

---

# Purpose

The Dependency Management model establishes the engineering requirements that govern all dependencies participating in FamilyOS build execution.

It covers:

* runtime dependencies;
* build dependencies;
* development dependencies;
* validation dependencies;
* documentation dependencies;
* plugin dependencies;
* optional dependencies;
* transitive dependencies;
* external build artifacts;
* dependency metadata;
* dependency resolution;
* dependency locking;
* dependency validation;
* dependency security;
* dependency updates;
* dependency evidence.

The objective is to prevent dependency state from becoming an uncontrolled source of build drift.

---

# Dependency Definition

A dependency is any external software component, package, library, artifact, tool, or resource that a build requires or resolves in order to execute correctly.

Conceptually:

```text id="1dmg1a"
FamilyOS Source
      +
Dependencies
      ↓
Effective Build State
```

Dependencies influence both execution and artifact trust.

---

# Dependency Categories

The FamilyOS dependency model recognizes several categories.

```text id="bnijio"
Dependencies
│
├── Runtime Dependencies
├── Build Dependencies
├── Development Dependencies
├── Validation Dependencies
├── Documentation Dependencies
├── Plugin Dependencies
├── Optional Dependencies
└── External Artifact Dependencies
```

These categories may overlap in concrete implementation.

Their purpose is to clarify responsibility.

---

# Runtime Dependencies

Runtime dependencies are required by produced software when it executes.

Examples include libraries imported by FamilyOS components.

Runtime dependencies influence:

* package metadata;
* compatibility;
* deployment;
* release behavior.

They must therefore be explicitly declared.

---

# Build Dependencies

Build dependencies are required to construct artifacts.

Examples may include:

* build frontends;
* build backends;
* generators;
* packaging utilities.

Build dependencies may not become runtime dependencies unless intentionally required.

---

# Development Dependencies

Development dependencies support engineering workflows.

Examples include:

* linting tools;
* type-checking tools;
* test tools;
* local development utilities.

These dependencies should remain distinguishable from runtime requirements.

---

# Validation Dependencies

Validation dependencies are required to verify build readiness or artifact quality.

Examples include tools used for:

* static analysis;
* test execution;
* package inspection;
* artifact validation;
* compliance checks.

They form part of the validation environment.

---

# Documentation Dependencies

Documentation generation may require dedicated tooling or packages.

These dependencies should remain explicit when documentation generation participates in the build lifecycle.

---

# Plugin Dependencies

Official plugins may define additional dependencies.

Plugin dependencies must remain compatible with:

* FamilyOS dependency rules;
* plugin architecture;
* compliance requirements;
* build profiles;
* release constraints.

A plugin must not introduce uncontrolled dependency behavior.

---

# Optional Dependencies

Optional dependencies may support additional features or profiles.

They must be clearly associated with:

* purpose;
* activation condition;
* compatibility expectations.

Optional dependencies should not silently become mandatory.

---

# External Artifact Dependencies

A build may depend on artifacts produced by another build.

Examples include:

* generated schemas;
* plugin bundles;
* packaged libraries.

Such dependencies must have identifiable origin and validation state.

---

# Dependency Principle 1 — Dependencies Must Be Declared

All required dependencies MUST be explicitly declared through canonical project mechanisms.

The framework rejects hidden dependencies such as:

```text id="okdmat"
Installed Locally
      ↓
Build Happens To Work
```

The preferred model is:

```text id="1xvxnq"
Declared Dependency
      ↓
Resolved Dependency
      ↓
Build
```

---

# Dependency Principle 2 — Dependency Purpose Must Be Clear

A dependency should have a clear reason for existing.

Engineers should be able to understand whether it is:

* runtime;
* build;
* development;
* validation;
* documentation;
* plugin-specific.

This reduces unnecessary dependency growth.

---

# Dependency Principle 3 — Dependency Resolution Must Be Controlled

Dependency resolution must not be treated as an invisible operation.

The framework should make clear:

```text id="3dz60t"
Declaration
    ↓
Constraint
    ↓
Resolution
    ↓
Resolved Dependency Set
```

The resolved set influences build output.

---

# Dependency Principle 4 — Resolution Must Be Reproducible Enough For Purpose

Development environments may allow broader resolution flexibility.

Release-oriented builds require stronger reproducibility.

The principle is:

```text id="ghijpt"
Higher Artifact Trust
        ↓
Stronger Dependency Control
```

---

# Dependency Principle 5 — Transitive Dependencies Matter

A direct dependency may introduce many transitive dependencies.

Therefore:

```text id="zl3a8r"
Declared Dependency
      ↓
Transitive Graph
      ↓
Effective Dependency State
```

FamilyOS must recognize that the complete resolved graph may influence build trust.

---

# Dependency Principle 6 — Mutable Dependencies Must Be Minimized

Dependency references that can change without an explicit version transition weaken reproducibility.

Examples include:

```text id="wbe6os"
latest
main branch
unversioned remote archive
mutable URL
```

Such mechanisms should not become canonical release-build dependencies without explicit justification.

---

# Dependency Principle 7 — Dependency Changes Are Build Changes

Updating a dependency may change:

* runtime behavior;
* build output;
* package metadata;
* validation results;
* security characteristics;
* compatibility.

Dependency updates must therefore be reviewed as engineering changes.

---

# Dependency Principle 8 — Dependency Security Is Build Security

A compromised dependency can affect the build or resulting artifact.

Dependencies therefore participate directly in software supply-chain risk.

Security considerations must be integrated into dependency management.

---

# Dependency Declaration

Dependency declarations should exist in canonical project configuration.

For Python-based FamilyOS components, this may be represented through project metadata.

The specific representation may evolve.

The invariant is:

> There must be one authoritative and discoverable declaration model.

---

# Canonical Dependency Source

The framework should avoid multiple conflicting dependency definitions.

The anti-pattern is:

```text id="fdgsiq"
pyproject configuration
requirements file
CI installation list
developer notes
```

all defining different dependency states.

If multiple files are necessary, ownership and precedence must be explicit.

---

# Dependency Constraints

Dependencies should have deliberate version constraints.

Possible strategies include:

* exact versions;
* compatible ranges;
* minimum versions;
* bounded ranges.

Each strategy has tradeoffs.

---

# Exact Version Constraints

Exact version constraints improve predictability.

They may be appropriate when:

* reproducibility is critical;
* compatibility is narrow;
* output changes materially between versions.

They also increase maintenance effort.

---

# Compatible Version Ranges

Compatible ranges allow dependency evolution without constant manual updates.

They may be appropriate when:

* APIs are stable;
* compatibility is tested;
* release reproducibility is enforced through locking elsewhere.

---

# Minimum Version Constraints

Minimum versions can support broader compatibility but may produce variable resolution.

They should be used carefully for trusted artifact generation.

---

# Upper Bounds

Upper bounds may prevent unexpected incompatibility when dependencies are known to introduce breaking changes outside a supported range.

They should not be added without a concrete compatibility reason.

---

# Dependency Locking

Dependency locking strengthens reproducibility by preserving a resolved dependency state.

Conceptually:

```text id="ctckf3"
Dependency Declaration
       ↓
Resolution
       ↓
Lock State
       ↓
Repeatable Installation
```

The exact lock mechanism depends on tooling.

---

# Lock State Purpose

A lock state may record:

* exact package versions;
* transitive dependencies;
* hashes;
* platform-specific resolution;
* dependency sources.

Its purpose is to reduce uncertainty.

---

# Lock State Scope

FamilyOS may eventually distinguish lock requirements by profile.

For example:

```text id="13o6d5"
Development
   ↓
Flexible Lock Usage

CI
   ↓
Controlled Lock Usage

Release Candidate
   ↓
Strict Lock Usage
```

The exact policy should evolve with implementation maturity.

---

# Lock File Ownership

When lock files exist, their ownership must be clear.

They should not be casually regenerated without understanding resulting changes.

A lock-file update is a dependency change.

---

# Dependency Resolution

Dependency resolution transforms declarations into an effective dependency graph.

The resolution process must be deterministic enough for the selected build profile.

---

# Resolution Inputs

Resolution may depend on:

* version constraints;
* package indexes;
* lock files;
* platform;
* runtime version;
* optional dependency selection;
* environment markers.

These factors must remain understandable.

---

# Resolution Environment

Dependency resolution itself may vary by environment.

For example:

```text id="lpp1vm"
Operating System
Runtime Version
Architecture
      ↓
Resolved Dependency Set
```

If this affects artifacts, it becomes part of build context.

---

# Dependency Graph

The complete resolved graph may conceptually be represented as:

```text id="731x6i"
Application
│
├── Dependency A
│   ├── Dependency A1
│   └── Dependency A2
│
└── Dependency B
    └── Dependency B1
```

Build trust depends on more than direct dependencies.

---

# Dependency Graph Validation

The resolved graph may require validation for:

* conflicts;
* unsupported versions;
* duplicate incompatible packages;
* prohibited dependencies;
* security findings.

---

# Dependency Compatibility

Dependencies must be compatible with:

* runtime version;
* platform architecture;
* FamilyOS source;
* other dependencies;
* build tooling.

Compatibility must not be assumed solely because installation succeeds.

---

# Runtime Compatibility

A dependency may support only specific runtime versions.

The Build Framework should detect incompatible combinations before trusted artifact creation.

---

# Platform Compatibility

Some dependencies may behave differently across platforms.

Where platform-specific resolution occurs, the build profile must account for this explicitly.

---

# Dependency Conflict

A dependency conflict occurs when requirements cannot be satisfied simultaneously.

The build should fail clearly.

The preferred result is:

```text id="5ghgde"
Conflict Detected
      ↓
Actionable Failure
```

not silent fallback to unpredictable state.

---

# Dependency Isolation

Project dependency state should remain isolated from global environments where practical.

For Python, virtual environments are a primary mechanism.

Isolation reduces accidental package leakage.

---

# Dependency Environment Reconstruction

A canonical dependency environment should be reconstructable from project declarations and associated resolution state.

The target model is:

```text id="tdx0hv"
Fresh Environment
       ↓
Canonical Dependency Definition
       ↓
Resolved Dependency Set
       ↓
Valid Build Environment
```

---

# Dependency Installation

Dependency installation should be repeatable and automation-friendly.

Installation should not require undocumented manual steps.

---

# Dependency Source

Dependencies may be acquired from:

* public package registries;
* private registries;
* local artifacts;
* version-controlled sources;
* internal repositories.

Dependency origin must be clear.

---

# Trusted Dependency Sources

Canonical builds should use governed dependency sources.

Unknown or ad hoc package sources increase supply-chain risk.

---

# Registry Configuration

If FamilyOS uses package registries, registry configuration should remain explicit.

Authentication secrets must remain separated from ordinary dependency metadata.

---

# Dependency Integrity

Where supported, dependency integrity may be strengthened through:

* cryptographic hashes;
* signed metadata;
* trusted registries;
* lock-file hashes;
* artifact validation.

These mechanisms can be introduced progressively.

---

# Dependency Provenance

Future FamilyOS build profiles may require stronger dependency provenance.

This may include information about:

* package source;
* version;
* integrity;
* upstream origin.

Provenance should be introduced when supply-chain maturity justifies it.

---

# Dependency Security

Dependency management must consider known security risks.

Possible controls include:

* vulnerability scanning;
* dependency review;
* update policies;
* source restrictions;
* integrity validation.

The Build Framework defines integration points.

Security Architecture defines broader policy.

---

# Vulnerability Findings

A dependency vulnerability may affect:

* local development;
* build execution;
* runtime artifacts;
* release approval.

Severity and action thresholds should be governed through Security and Quality frameworks.

---

# Build Dependency Risk

Build-only dependencies are also security-sensitive.

A malicious build dependency can modify generated artifacts even if it is absent at runtime.

Therefore:

```text id="y9l0z4"
Build Dependency Risk
        =
Supply Chain Risk
```

---

# Development Dependency Risk

Development tools may influence source or artifacts through:

* formatting;
* generation;
* validation;
* packaging.

Their risk should remain proportional to their impact.

---

# Dependency Update Lifecycle

Dependency updates should follow a controlled process.

```text id="9bxzyc"
Identify Update
      ↓
Review Change
      ↓
Update Declaration
      ↓
Update Lock State
      ↓
Resolve
      ↓
Validate
      ↓
Build
      ↓
Compare Results
      ↓
Adopt
```

Not every update requires the same level of review.

---

# Patch Updates

Patch updates may be low-risk but still require validation.

Automated update mechanisms may be appropriate if quality gates remain intact.

---

# Minor Updates

Minor updates may add features or behavior changes.

They should be validated against:

* tests;
* static analysis;
* build output;
* compatibility.

---

# Major Updates

Major dependency updates may introduce breaking changes.

They should receive stronger review and may require:

* migration work;
* ADR updates;
* release coordination.

---

# Dependency Removal

Unused dependencies should be removed.

Every dependency increases:

* maintenance surface;
* installation time;
* security surface;
* compatibility complexity.

The preferred rule is:

```text id="ctc4uq"
No Proven Need
     ↓
No Dependency
```

---

# Dependency Minimalism

FamilyOS should prefer the minimum dependency set required to provide intended capability.

Dependency convenience alone is not sufficient justification for permanent adoption.

---

# Dependency Duplication

Multiple dependencies solving the same problem should be avoided without clear architectural reason.

Duplication increases:

* bundle complexity;
* cognitive load;
* security review surface.

---

# Optional Dependency Governance

Optional dependency groups must remain clear.

Examples may include:

```text id="kyoo4m"
testing
documentation
development
plugin-specific
```

Their activation should be explicit.

---

# Build Profile Dependency Sets

Different build profiles may use different dependency sets.

For example:

```text id="fm0d0r"
Development
├── Runtime
├── Dev
├── Test
└── Build
```

while:

```text id="obfr8r"
Release Candidate
├── Runtime
├── Build
├── Validation
└── Artifact Validation
```

Profile differences must remain documented.

---

# Plugin Dependency Management

Official plugins must declare their dependencies through governed mechanisms.

Plugin dependencies must not:

* bypass platform compatibility rules;
* introduce undeclared package requirements;
* conflict silently with core dependencies.

---

# Plugin Dependency Compatibility

A plugin dependency should be evaluated against:

* core runtime;
* official plugin ecosystem;
* platform version;
* compliance rules.

This prevents isolated plugin success from destabilizing the platform.

---

# Cross-Component Dependencies

FamilyOS components may depend on other internal components.

These relationships should remain explicit.

Avoid filesystem coupling such as:

```text id="vnkwgf"
../../other-component/internal-file
```

when a proper package or architectural dependency should exist.

---

# Internal Dependency Versioning

Internal artifacts may eventually require explicit version relationships.

This will become more important as FamilyOS distribution architecture matures.

---

# External Build Artifact Dependencies

A build consuming an upstream artifact must validate that artifact before use.

A canonical flow is:

```text id="noxm75"
Upstream Build
      ↓
Validated Artifact
      ↓
Dependency Input
      ↓
Downstream Build
```

---

# Dependency Caching

Dependency caches may improve performance.

Caches may contain:

* downloaded packages;
* resolved metadata;
* built wheels.

Caches are optimization layers.

They must not become authoritative dependency state.

---

# Cache Safety

A cache must only be reused when its validity conditions remain satisfied.

The principle is:

```text id="urujwx"
Dependency Correctness
        >
Cache Performance
```

---

# Offline Dependency Resolution

Future stronger builds may use pre-fetched or mirrored dependencies to reduce external variability.

Potential benefits include:

* reproducibility;
* resilience;
* supply-chain control.

This is a future capability, not an immediate requirement.

---

# Dependency Mirrors

A controlled mirror may eventually provide:

* package availability;
* integrity control;
* reduced external dependency;
* auditability.

Such infrastructure should only be introduced when justified.

---

# Dependency Observability

Build diagnostics should expose relevant dependency state.

For significant builds, useful information may include:

* direct dependency versions;
* lock-state identifier;
* resolution status;
* dependency conflicts;
* package source.

---

# Dependency Evidence

Dependency state may become part of build evidence.

A conceptual evidence model is:

```text id="8g7te9"
Build Evidence
│
└── Dependencies
    ├── Declaration State
    ├── Lock State
    ├── Resolved Versions
    └── Source Information
```

Evidence detail should remain proportional to profile.

---

# Dependency Fingerprinting

Future builds may fingerprint dependency state.

For example:

```text id="09nucq"
Dependency Graph
      ↓
Canonical Representation
      ↓
Dependency Fingerprint
```

This could support:

* cache correctness;
* provenance;
* reproducibility;
* artifact comparison.

---

# Dependency Change Detection

A build system may eventually detect when dependency state has changed relative to prior trusted builds.

This may trigger:

* stronger validation;
* artifact comparison;
* release review.

---

# Dependency Failure Categories

Possible conceptual failure categories include:

```text id="bcde6k"
MISSING_DEPENDENCY
UNRESOLVED_DEPENDENCY
INCOMPATIBLE_DEPENDENCY
CONFLICTING_DEPENDENCIES
UNTRUSTED_DEPENDENCY_SOURCE
DEPENDENCY_INTEGRITY_FAILURE
DEPENDENCY_POLICY_VIOLATION
```

Formal machine-readable implementation may come later.

---

# Dependency Failure Diagnostics

A useful dependency failure should identify:

* affected dependency;
* requested constraint;
* resolved candidate;
* conflict or policy reason;
* corrective direction.

Opaque package-manager errors should be wrapped or documented where practical.

---

# Dependency And Reproducibility

Dependency management is one of the strongest determinants of build reproducibility.

The relationship is:

```text id="7i205w"
Controlled Dependency State
          ↓
Reduced Build Variability
          ↓
Improved Reproducibility
```

---

# Dependency And Determinism

Mutable dependency resolution introduces non-determinism.

Locking and controlled sources can progressively reduce it.

---

# Dependency And Security

Dependency compromise can affect every downstream artifact.

Dependency management is therefore one of the principal build supply-chain controls.

---

# Dependency And Quality

Dependency state can influence quality through:

* defects;
* compatibility issues;
* security findings;
* test instability;
* artifact differences.

Dependency changes may therefore participate in quality gates.

---

# Dependency And Testing

The Testing Framework validates behavior after dependency changes.

Dependency updates should trigger appropriate regression testing.

---

# Dependency And Release

Official releases may require stronger dependency evidence.

The Release Framework may impose:

* lock-state requirements;
* vulnerability thresholds;
* dependency review;
* provenance requirements.

The Build Framework should expose necessary data.

---

# Dependency And Documentation

Dependency requirements must be documented clearly enough that contributors can reconstruct supported environments.

Documentation should explain:

* installation;
* groups;
* optional dependencies;
* update workflow;
* common conflicts.

---

# Dependency Governance

Significant dependency architecture changes may require formal governance.

Examples include:

* changing dependency manager;
* introducing private registries;
* changing lock strategy;
* introducing vendoring;
* introducing dependency mirrors;
* changing core runtime dependency model.

---

# Dependency Technical Debt

Dependency debt includes:

* unused dependencies;
* overly broad version ranges;
* abandoned packages;
* duplicated libraries;
* unresolved warnings;
* undocumented optional dependencies;
* stale lock state;
* insecure package sources.

Dependency debt should be reviewed continuously.

---

# Dependency Maintenance Policy

Dependency maintenance should balance:

* stability;
* security;
* compatibility;
* reproducibility;
* engineering effort.

The objective is neither permanent freezing nor constant churn.

The target is controlled evolution.

---

# Dependency Review Questions

When introducing or updating a dependency, engineers should ask:

```text id="g1h8kp"
Why is this dependency needed?

Is an existing dependency sufficient?

Is the package maintained?

Is its license acceptable?

Is its security posture acceptable?

Does it support our runtime?

Does it affect build reproducibility?

How will it be versioned?

How will it be validated?

Can it be removed later?
```

---

# Dependency Anti-Pattern — Undeclared Installation

The framework rejects dependencies installed manually outside project definitions.

---

# Dependency Anti-Pattern — Latest Everywhere

Uncontrolled use of the newest available version can make builds change without source changes.

---

# Dependency Anti-Pattern — CI-Only Dependency

CI must not install critical dependencies that are absent from canonical project declarations.

---

# Dependency Anti-Pattern — Local Package Leakage

A build must not succeed because a package exists globally but is missing from project dependencies.

---

# Dependency Anti-Pattern — Stale Lock State

A lock file that no longer corresponds to declarations weakens rather than strengthens reproducibility.

---

# Dependency Anti-Pattern — Unreviewed Build Dependency

Build dependencies can alter artifacts and therefore require review proportional to impact.

---

# Dependency Anti-Pattern — Excessive Dependency Surface

Adding packages for trivial tasks can create long-term maintenance and supply-chain cost.

---

# Dependency Maturity Model

FamilyOS dependency maturity may progress through:

```text id="n2db26"
Level 1
Declared Dependencies

    ↓

Level 2
Structured Dependency Groups

    ↓

Level 3
Controlled Version Constraints

    ↓

Level 4
Lock-Based Reproducibility

    ↓

Level 5
Automated Dependency Validation

    ↓

Level 6
Dependency Integrity Verification

    ↓

Level 7
Dependency Provenance
```

The framework supports progressive adoption.

---

# Dependency Success Criteria

The Dependency Management model is successful when FamilyOS can answer:

1. which dependencies are required;
2. why each significant dependency exists;
3. which dependency set applies to each build profile;
4. how versions are constrained;
5. how dependency resolution occurs;
6. whether the resolved graph is reproducible;
7. how conflicts are detected;
8. how dependency state is validated;
9. how updates are governed;
10. how security findings are handled;
11. how dependency state contributes to build evidence;
12. how plugin dependencies remain compatible with the platform;
13. how unused dependencies are removed;
14. how external dependency sources are controlled.

---

# Dependency Invariants

The following invariants should remain true.

## Invariant 1

Required dependencies must be explicitly declared.

## Invariant 2

Dependency resolution must not rely on undocumented installed state.

## Invariant 3

Critical dependency changes must remain reviewable.

## Invariant 4

Unresolved dependency conflicts must prevent trusted artifact creation.

## Invariant 5

Dependency sources must remain governable.

## Invariant 6

Build-only dependencies must receive supply-chain consideration.

## Invariant 7

Release candidate builds should use stronger dependency reproducibility controls.

## Invariant 8

Dependency caches must not become authoritative.

## Invariant 9

Plugin dependencies must remain compatible with platform rules.

## Invariant 10

Dependency state must remain explainable for trusted builds.

---

# Dependency Model Summary

The canonical FamilyOS dependency lifecycle is:

```text id="n1w13b"
Declare
   ↓
Constrain
   ↓
Resolve
   ↓
Lock When Required
   ↓
Validate
   ↓
Install
   ↓
Execute Build
   ↓
Record Relevant State
   ↓
Review And Maintain
```

This converts dependencies from invisible external conditions into governed components of the Build Framework.

---

# Final Principle

The FamilyOS Dependency Management model is founded on the following rule:

> Source code does not define a build by itself; the resolved dependency state is part of what is actually built.

A dependency that cannot be identified, reproduced, validated, or governed weakens the trust of every artifact produced with it.

FamilyOS must therefore treat dependency management as a permanent part of build engineering, not as a package installation detail.
