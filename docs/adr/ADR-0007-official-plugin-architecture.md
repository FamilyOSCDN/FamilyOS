# ADR-0007 — Official Plugin Architecture

**Identifier:** ADR-0007
**Title:** Official Plugin Architecture
**Status:** Accepted
**Date:** 2026-08-03
**Last Updated:** 2026-08-10
**Owner:** FamilyOS Project
**Layer:** Architecture Decision Records

---

# Status

Accepted

---

# Date

2026-08-03

Last architectural clarification:

```text
2026-08-10
```

---

# Context

FamilyOS is designed as an extensible platform capable of evolving through independent capabilities and domain extensions.

As the platform grows, new features cannot all be implemented directly inside the core system.

The platform requires an architecture that enables:

* independent feature development;
* controlled extension points;
* stable contracts;
* lifecycle management;
* dependency management;
* compatibility management;
* secure integration of external components;
* deterministic plugin identity;
* reliable dependency resolution.

The initial implementation introduced plugin concepts progressively through:

* Plugin Runtime;
* Plugin SDK;
* Plugin Lifecycle;
* Plugin Capabilities;
* Plugin Contributions;
* Plugin Discovery;
* Plugin Resolution;
* Dependency Graph Management;
* Plugin Diagnostics.

These components require an official architectural decision defining their relationship and responsibilities.

A subsequent architecture audit identified an additional requirement:

> plugin identity MUST remain consistent across manifests, descriptors, discovery, package models, dependency declarations, resolution, registries, and dependency graphs.

Without this rule, human-readable names, package representations, and canonical plugin identifiers can become incorrectly interchangeable.

---

# Problem Statement

FamilyOS requires a plugin architecture that allows extensions to integrate with the platform without creating direct dependencies between the core platform and individual plugins.

The architecture SHALL define:

* how plugins are identified;
* how plugins are discovered;
* how plugins are resolved;
* how plugins are loaded;
* how plugins participate in runtime execution;
* how plugins expose capabilities;
* how plugins contribute platform resources;
* how plugin dependencies identify their targets;
* how plugin identity propagates across ecosystem layers.

The architecture MUST distinguish between:

```text
Plugin Identifier
Plugin Display Name
Plugin Version
Plugin Package Identity
Implementation Module
Implementation Class
Capability Identifier
```

These concepts SHALL NOT be treated as interchangeable representations of plugin identity.

---

# Decision

FamilyOS adopts an official plugin architecture based on a contract-driven plugin ecosystem.

A plugin SHALL interact with the platform exclusively through defined plugin contracts.

The plugin architecture SHALL consist of the following major layers:

* Plugin Ecosystem;
* Plugin Runtime;
* Plugin SDK;
* Plugin Contributions;
* Plugin Capabilities.

Plugins SHALL NOT directly modify FamilyOS core implementation.

FamilyOS additionally adopts a canonical Plugin Identity Model.

The canonical Plugin Identifier SHALL be the stable logical identity propagated across plugin architecture boundaries.

---

# Architectural Principles

The plugin architecture follows these principles.

---

## Separation of Core and Extensions

The FamilyOS core SHALL remain independent from individual plugins.

Plugins SHALL integrate through controlled extension contracts.

---

## Contract-Based Integration

Plugins SHALL integrate through stable contracts instead of internal implementation details.

Public plugin contracts SHALL remain explicitly governed.

---

## Capability-Based Extension

Plugins SHALL expose functionality through declared capabilities.

Capabilities SHALL remain distinct from plugin implementation details.

---

## Controlled Lifecycle

Plugins SHALL follow a managed lifecycle controlled by the Plugin Runtime.

Plugins SHALL NOT independently redefine runtime lifecycle semantics.

---

## Explicit Dependencies

Plugin dependencies SHALL be declared and resolved explicitly.

Dependency identity SHALL reference stable plugin identity rather than human-readable labels.

---

## Versioned Evolution

Plugin contracts SHALL evolve through explicit versioning mechanisms.

Versions SHALL remain separate from canonical identifiers.

---

## Stable Identity

A plugin SHALL have one stable logical Plugin Identifier.

That identifier SHALL remain independent from:

* display name;
* version;
* implementation class;
* Python module;
* source path;
* package filename;
* distribution name.

---

## Identity Preservation

Once a Plugin Identifier enters the plugin architecture, architectural layers SHALL preserve its logical meaning.

A component SHALL NOT silently replace canonical plugin identity with a display name or unrelated package representation.

---

# Architecture Overview

The FamilyOS plugin architecture is composed of multiple layers with clearly defined responsibilities.

```text
                         FamilyOS Platform

                                │
                                ▼

                       Plugin Runtime Layer

                                │

             ┌──────────────────┼──────────────────┐
             ▼                  ▼                  ▼

      Plugin Lifecycle   Plugin Capabilities   Plugin Contributions

             │                  │                  │
             └──────────────────┼──────────────────┘
                                ▼

                         Plugin Instance


                         Plugin Ecosystem

        Discovery → Resolution → Verification → Installation → Loading
```

Plugin identity SHALL remain stable throughout these layers.

Conceptually:

```text
plugin.yaml
    │
    │ id
    ▼
PluginDescriptor
    │
    │ Plugin Identifier
    ▼
Plugin Discovery
    │
    ▼
Plugin Package
    │
    ├── Resolution
    ├── Dependency Graph
    ├── Installation
    └── Diagnostics
```

The logical identifier SHALL remain the same throughout this flow.

---

# Plugin Identity Model

FamilyOS defines the following distinct plugin identity-related concepts.

---

## Plugin Identifier

The Plugin Identifier is the stable logical identity of a plugin.

Examples:

```text
familyos.security
familyos.health
familyos.finance
familyos.education
familyos.documents
familyos.communication
```

The Plugin Identifier SHALL:

* comply with SPEC-0002;
* comply with SPEC-0008;
* remain stable across compatible versions;
* remain independent from display metadata;
* remain independent from implementation structure;
* serve as the primary logical reference to the plugin.

For official FamilyOS plugins, the canonical form SHALL be:

```text
familyos.<plugin-name>
```

---

## Plugin Display Name

The Plugin Display Name is human-readable metadata.

Examples:

```text
FamilyOS Security Plugin
FamilyOS Education Plugin
FamilyOS Documents Plugin
```

The display name MAY change when appropriate without changing plugin identity.

A Plugin Display Name SHALL NOT serve as:

* registry identity;
* dependency identity;
* resolver identity;
* graph identity;
* persisted canonical plugin reference.

---

## Plugin Version

The Plugin Version represents evolution of a plugin under a stable Plugin Identifier.

Example:

```text
Plugin Identifier:
familyos.education

Version:
1.0.0
```

Version semantics SHALL comply with SPEC-0004.

The version SHALL NOT be embedded into the canonical Plugin Identifier.

---

## Plugin Package Identity

A concrete plugin package represents a particular version of a plugin.

Its conceptual package identity SHALL therefore be:

```text
Plugin Identifier + Version
```

Example:

```text
familyos.education@1.0.0
```

This representation MAY be materialized differently by implementation models, but the architectural semantics SHALL remain equivalent.

Package identity SHALL NOT be derived from the Plugin Display Name.

---

## Implementation Identity

Implementation details include:

* Python module;
* implementation class;
* package path;
* source path;
* distribution name.

Example:

```text
Plugin Identifier:
familyos.education

Module:
familyos_cli.plugins.builtin.education.plugin

Class:
EducationPlugin
```

Implementation identity SHALL NOT replace logical plugin identity.

Refactoring implementation details SHALL NOT automatically require changing the Plugin Identifier.

---

# Plugin Manifest Identity

The Plugin Manifest SHALL be the authoritative package declaration of plugin identity and metadata.

A manifest SHALL distinguish:

```yaml
id: familyos.education
name: FamilyOS Education Plugin
version: 1.0.0
```

The semantics are:

```text
id
    → Plugin Identifier

name
    → Plugin Display Name

version
    → Plugin Version
```

These fields SHALL NOT be treated as synonyms.

The manifest identity model SHALL comply with SPEC-0009.

---

# Plugin Descriptor Identity

`PluginDescriptor.id` SHALL represent the canonical Plugin Identifier.

Conceptually:

```text
PluginDescriptor.id
=
Plugin Identifier
```

`PluginDescriptor.name` SHALL represent the human-readable Plugin Display Name.

Conceptually:

```text
PluginDescriptor.name
=
Plugin Display Name
```

The descriptor SHALL preserve the distinction established by the manifest.

---

# Plugin Metadata

Plugin metadata MAY contain:

* display name;
* version;
* author;
* description;
* homepage;
* license;
* API version.

Metadata SHALL describe a plugin.

Metadata SHALL NOT replace canonical plugin identity.

The Plugin Identifier SHALL remain independently accessible from metadata.

---

# Plugin Ecosystem

The Plugin Ecosystem is responsible for managing plugins outside the runtime execution environment.

It provides:

* discovery;
* repository management;
* package handling;
* verification;
* installation;
* dependency resolution;
* diagnostics.

The Plugin Ecosystem SHALL operate independently from plugin runtime execution while preserving canonical Plugin Identifiers.

---

# Plugin Discovery

Plugin Discovery identifies available plugins from configured sources.

Discovery SHALL provide:

* Plugin Identifier;
* plugin metadata;
* available versions;
* plugin manifests;
* source information.

Discovery SHALL NOT activate plugins.

Discovery SHALL preserve canonical Plugin Identifier semantics when transforming a `PluginDescriptor` into an ecosystem package representation.

Conceptually:

```text
PluginDescriptor.id
        │
        ▼
PluginPackage Plugin Identifier
```

The following transformation is architecturally invalid as an identity mechanism:

```text
PluginDescriptor.name
        │
        ▼
PluginPackage technical identity
```

because `PluginDescriptor.name` represents display metadata.

---

# Plugin Package

A `PluginPackage` represents a concrete plugin package available through the Plugin Ecosystem.

Architecturally, it SHALL expose or preserve:

* Plugin Identifier;
* Plugin Version;
* source information;
* manifest information where available;
* dependency information where available.

The combination:

```text
Plugin Identifier + Version
```

SHALL distinguish a concrete plugin package version.

A package MAY additionally expose a human-readable display name.

The display name SHALL NOT determine package identity.

---

# Plugin Repository

A Plugin Repository provides available plugin packages to discovery and resolution mechanisms.

Repository identity SHALL remain separate from plugin identity.

A repository MAY contain:

```text
familyos.education@1.0.0
familyos.education@1.1.0
familyos.documents@1.0.0
```

without altering the underlying logical Plugin Identifiers.

---

# Plugin Resolution

Plugin Resolution determines a valid set of plugins based on:

* requested plugins;
* Plugin Identifiers;
* version constraints;
* dependency requirements;
* compatibility rules.

Resolution SHALL produce an explicit resolution result.

Resolver matching SHALL use Plugin Identifiers as logical dependency targets.

Conceptually:

```text
Requested Plugin Identifier
        │
        ▼
Available packages for Plugin Identifier
        │
        ▼
Version constraint evaluation
        │
        ▼
Selected package version
```

Display names SHALL NOT be used as canonical resolver keys.

---

# Plugin Dependency Identity

A plugin dependency SHALL identify its target using a Plugin Identifier.

Example:

```text
Dependency target:
familyos.security
```

with an independent version constraint:

```text
>=1.0.0
```

Conceptually:

```text
PluginDependency
    ├── plugin_id
    └── version_constraint
```

An implementation MAY temporarily expose legacy property names such as:

```text
name
```

for compatibility.

However, the architectural meaning of that field SHALL be Plugin Identifier when it participates in dependency resolution.

A dependency SHALL NOT target a plugin solely through its display name.

---

# Dependency Graph Identity

The Dependency Graph SHALL represent plugin relationships using canonical Plugin Identifiers.

Logical graph identity SHALL use:

```text
Plugin Identifier
```

Concrete versioned graph nodes MAY use:

```text
Plugin Identifier + Version
```

Example:

```text
familyos.education@1.0.0
        │
        └── familyos.security@1.2.0
```

Graph construction SHALL NOT depend on human-readable plugin display names.

---

# Plugin Installation

Plugin Installation manages the transition of resolved plugin packages into the local plugin environment.

Installation SHALL verify:

* package integrity;
* required metadata;
* compatibility constraints;
* canonical plugin identity.

Installation SHALL preserve the Plugin Identifier selected during resolution.

---

# Plugin Runtime

The Plugin Runtime manages the execution lifecycle of loaded plugins.

The Plugin Runtime is responsible for:

* loading plugins;
* initializing plugins;
* activating plugins;
* stopping plugins;
* managing runtime state.

A plugin SHALL NOT control its own lifecycle transitions.

Runtime registration SHALL use canonical Plugin Identifiers.

---

# Plugin Registry

Plugin registries SHALL use Plugin Identifiers as logical registry keys.

Conceptually:

```text
PluginRegistry[
    PluginIdentifier
]
```

Example:

```text
PluginRegistry[
    "familyos.education"
]
```

A display name such as:

```text
FamilyOS Education Plugin
```

SHALL NOT serve as canonical registry identity.

---

# Plugin Manager

A Plugin Manager coordinating descriptors or runtime plugins SHALL preserve canonical Plugin Identifier semantics.

Operations such as:

```text
register
get
enable
disable
activate
```

SHOULD identify plugins using Plugin Identifiers.

---

# Plugin Lifecycle

Plugins SHALL follow the managed lifecycle defined by the Plugin Runtime.

The lifecycle model SHALL include:

```text
LOADED

↓

INITIALIZED

↓

ACTIVE

↓

STOPPING

↓

STOPPED
```

Invalid lifecycle transitions SHALL be rejected.

Lifecycle state SHALL NOT alter plugin identity.

---

# Plugin SDK

The Plugin SDK defines the public contracts available to plugin developers.

The SDK SHALL provide:

* plugin contract;
* lifecycle contract;
* capability contract;
* contribution contract;
* identity-related contracts where required.

Plugin implementations SHALL depend only on SDK contracts.

Public SDK contracts involving plugin identity SHALL use canonical Plugin Identifier semantics.

---

# Plugin Capabilities

Capabilities define the functional services exposed by plugins.

A capability SHALL:

* have a unique identifier;
* declare its purpose;
* expose a stable contract.

Capabilities SHALL NOT depend on plugin implementation details.

Capability identity SHALL remain distinct from Plugin Identifier identity.

Official plugin capability identifiers SHALL follow SPEC-0010.

Example:

```text
Plugin:
familyos.education

Capabilities:
familyos.education.learner
familyos.education.course
familyos.education.record
```

---

# Plugin Contributions

Contributions define resources provided by plugins to the FamilyOS platform.

Supported contributions include:

* generation contributions;
* recipe contributions;
* template contributions;
* domain contributions.

Contributions SHALL be registered through official extension points.

Contribution identity SHALL remain distinct from Plugin Identifier identity.

---

# Plugin Isolation

Plugins SHALL remain isolated from each other's internal implementation.

A plugin MAY consume another plugin capability only through declared contracts.

Implementation modules SHALL NOT become cross-plugin identity mechanisms.

---

# Plugin Communication

Plugin communication SHALL occur through:

* runtime services;
* capability contracts;
* contribution registries.

Direct plugin-to-plugin implementation dependencies SHALL NOT be permitted.

---

# Identity Propagation

Canonical Plugin Identifier semantics SHALL propagate through the complete architecture.

The target model is:

```text
Manifest
    │
    │ id
    ▼
PluginDescriptor.id
    │
    ▼
Discovery
    │
    ▼
PluginPackage.plugin_id
    │
    ├───────────────┐
    ▼               ▼
Resolver      Dependency Graph
    │               │
    └───────┬───────┘
            ▼
       Installation
            │
            ▼
          Runtime
            │
            ▼
         Registry
```

The exact implementation property names MAY evolve.

The semantic identity SHALL remain the Plugin Identifier.

---

# Current Implementation Assessment

An architecture audit performed on 2026-08-10 identified that the current implementation already preserves identity correctly through part of the runtime path.

The current loader maps:

```text
plugin.yaml id
        ↓
PluginDescriptor.id
```

and:

```text
plugin.yaml name
        ↓
PluginDescriptor.name
```

This separation is architecturally correct.

The runtime registry and manager also use:

```text
PluginDescriptor.id
```

as plugin identity.

However, the Plugin Ecosystem currently contains an identity-model inconsistency.

---

# Current Ecosystem Identity Debt

The current discovery implementation conceptually performs:

```text
PluginDescriptor.name
        ↓
PluginPackage.name
```

while `PluginPackage.name` is subsequently used as a technical key by:

* package selection;
* dependency resolution;
* dependency graph construction;
* related diagnostics.

This means a human-readable display name can become a technical resolution identity.

Example:

```text
PluginDescriptor.id:
familyos.finance

PluginDescriptor.name:
FamilyOS Finance Plugin
```

may currently become conceptually:

```text
PluginPackage.name:
FamilyOS Finance Plugin
```

while a dependency correctly referencing:

```text
familyos.finance
```

expects canonical plugin identity.

This is an architectural inconsistency.

---

# Target Ecosystem Identity Model

The target architecture SHALL preserve:

```text
PluginDescriptor.id
        ↓
PluginPackage Plugin Identifier
        ↓
Resolver / Dependency Graph
```

while preserving display metadata independently:

```text
PluginDescriptor.name
        ↓
PluginPackage Display Name
```

if the ecosystem package model requires display metadata.

The implementation MAY achieve this through:

* a new `plugin_id` field;
* a dedicated `PluginId` value object;
* a compatible restructuring of `PluginPackage`;
* another explicitly approved implementation.

This ADR defines semantics, not the final Python field design.

---

# Legacy Plugin Identifiers

Some official plugins currently use legacy short Plugin Identifiers.

Known legacy identifiers include:

```text
education
documents
communication
documentation
```

Their canonical targets are:

```text
education
→ familyos.education

documents
→ familyos.documents

communication
→ familyos.communication

documentation
→ familyos.documentation
```

These mappings establish canonical target identity.

They DO NOT authorize immediate migration.

---

# Legacy Compatibility Policy

Existing legacy Plugin Identifiers SHALL NOT be renamed automatically.

Before migration, FamilyOS SHALL evaluate:

* runtime lookup consumers;
* Plugin Registry usage;
* Plugin Manager usage;
* Plugin Ecosystem usage;
* dependency declarations;
* Dependency Graph usage;
* CLI references;
* configuration;
* persisted state;
* generated artifacts;
* tests;
* public documentation.

A migration MAY require aliases or explicit compatibility adapters.

Legacy identifiers SHALL NOT be reassigned to unrelated plugins.

---

# Plugin Identity Migration

Changing a stable Plugin Identifier is an identity migration.

A Plugin Identifier migration SHALL require:

1. identification of affected consumers;
2. dependency impact analysis;
3. runtime lookup analysis;
4. resolver impact analysis;
5. dependency graph impact analysis;
6. persisted-reference analysis;
7. alias strategy where required;
8. deprecation strategy where required;
9. test migration;
10. documentation migration;
11. release notes;
12. architectural approval.

A global textual replacement SHALL NOT be considered a valid migration strategy.

---

# Capability Migration Independence

Plugin Identifier migration and Capability Identifier migration are distinct architectural operations.

For example:

```text
Plugin:
education
→ familyos.education
```

does not automatically authorize changing:

```text
familyos.education.course
```

because that capability identifier may already be canonical.

Likewise:

```text
Plugin:
familyos.security
```

does not automatically migrate a legacy capability such as:

```text
security.validation
```

to:

```text
familyos.security.validation
```

Capability migration SHALL be governed independently by SPEC-0010.

---

# Manifest Dependency Evolution

The current runtime manifest loader does not establish a dependency-declaration contract merely because the ecosystem supports `PluginDependency`.

Manifest dependency declarations SHALL be introduced or activated only through an explicit supported contract.

This ADR SHALL NOT be interpreted as requiring immediate addition of:

```yaml
dependencies:
```

to existing plugin manifests.

Dependency parsing, validation, and manifest integration MAY evolve separately.

---

# Consequences

The adoption of this architecture introduces the following consequences.

---

## Positive Consequences

### Stable Plugin Identity

Plugins have one logical identity independent from presentation and implementation details.

---

### Deterministic Resolution

Dependency resolution can operate on canonical Plugin Identifiers rather than ambiguous display names.

---

### Consistent Runtime Lookup

Registry, manager, resolver, and dependency graph semantics can converge on the same logical identity.

---

### Safe Refactoring

Changing:

* Python module;
* implementation class;
* package path;
* display name;

does not automatically change plugin identity.

---

### Better Ecosystem Interoperability

Third-party plugins can reference stable plugin identities without depending on implementation details.

---

### Clear Version Semantics

Plugin versions remain independent from logical plugin identity.

Concrete package versions can be represented using:

```text
Plugin Identifier + Version
```

without modifying the canonical identifier.

---

### Controlled Legacy Migration

Legacy IDs can remain temporarily supported without redefining the canonical architecture.

---

### Clearer Capability Boundaries

Plugin identity and capability identity remain distinct contracts with independent migration governance.

---

## Negative Consequences

### Implementation Refactoring

The current Plugin Ecosystem package and dependency models require future alignment with the canonical identity model.

---

### Compatibility Work

Existing short Plugin Identifiers may require aliases, deprecation mechanisms, or compatibility adapters.

---

### Additional Model Explicitness

Some existing generic fields such as:

```text
name
```

may eventually require more precise semantics such as:

```text
plugin_id
display_name
```

---

### Migration Complexity

The ecosystem cannot safely migrate through simple search-and-replace operations.

---

# Alternatives Considered

## Use Display Name as Plugin Identity

Rejected.

Example:

```text
FamilyOS Education Plugin
```

is presentation metadata and may change independently from logical identity.

Using it for dependency resolution creates unnecessary coupling.

---

## Use Distribution Package Name as Plugin Identity

Rejected.

Example:

```text
familyos-education-plugin
```

belongs to package/distribution naming and SHALL remain separate from ecosystem identity.

---

## Use Python Module as Plugin Identity

Rejected.

Example:

```text
familyos_cli.plugins.builtin.education.plugin
```

is an implementation location and may change during refactoring.

---

## Use Implementation Class as Plugin Identity

Rejected.

Example:

```text
EducationPlugin
```

is an implementation type and does not provide stable ecosystem identity.

---

## Preserve Short IDs as the Canonical Convention

Rejected for new official plugins.

Short identifiers such as:

```text
education
documents
communication
```

do not express namespace ownership and create potential ecosystem collisions.

They MAY remain temporarily supported as legacy identifiers.

---

## Immediately Rename All Legacy Plugin IDs

Rejected.

Existing identifiers may participate in:

* runtime contracts;
* tests;
* dependency resolution;
* CLI behavior;
* generated artifacts;
* public documentation.

Migration requires explicit compatibility analysis.

---

# Governance

The Plugin Architecture SHALL evolve through:

* Architecture Decision Records;
* Specifications;
* Requests for Comments.

Changes affecting plugin identity SHALL require explicit architectural review.

Plugin SDK changes SHALL preserve backward compatibility whenever practical.

Changes affecting canonical Plugin Identifier semantics SHALL be aligned with:

* SPEC-0002;
* SPEC-0008;
* SPEC-0009;
* relevant reference documentation.

Changes affecting capability identity SHALL additionally align with SPEC-0010.

---

# Implementation Status

The broader architecture defined by this ADR has been implemented through:

* Plugin Runtime;
* Plugin SDK v2;
* Plugin Lifecycle Management;
* Plugin Capabilities;
* Plugin Contributions;
* Plugin Discovery;
* Plugin Resolution;
* Dependency Graph Resolution;
* Plugin Diagnostics;
* Generation Integration.

The canonical Plugin Identity Model is partially implemented.

Correctly aligned areas include:

```text
plugin.yaml id
→ PluginDescriptor.id

PluginDescriptor.id
→ Plugin Registry identity

PluginDescriptor.id
→ Plugin Manager identity
```

Known implementation debt remains in the Plugin Ecosystem identity path:

```text
PluginDescriptor.name
→ PluginPackage.name
→ resolution identity
```

This debt SHALL be addressed through a dedicated implementation change after migration design and test planning.

---

# Required Follow-Up

The following work SHALL occur before legacy Plugin Identifier migration:

1. align Plugin Ecosystem package identity with Plugin Identifier semantics;
2. align dependency targets with Plugin Identifier semantics;
3. align resolver lookup with Plugin Identifier semantics;
4. align Dependency Graph identity with Plugin Identifier semantics;
5. define compatibility behavior for legacy IDs;
6. establish tests for canonical and legacy lookup;
7. define migration sequencing;
8. update manifests only after compatibility behavior is established.

No legacy Plugin Identifier SHALL be changed solely as part of documenting this ADR.

---

# Related Specifications

This ADR depends on:

* SPEC-0002 — Identifier;
* SPEC-0003 — Metadata;
* SPEC-0004 — Versioning;
* SPEC-0007 — File Format;
* SPEC-0008 — Naming Conventions;
* SPEC-0009 — Plugin Manifest;
* SPEC-0010 — Plugin Capability Contract.

Future plugin-specific specifications SHALL reference this ADR as the architectural foundation.

---

# Related Reference Documents

This ADR is aligned with:

```text
docs/04-reference/Naming-Conventions.md
docs/04-reference/Reserved-Words.md
```

These reference documents define canonical representation and reserved namespace ownership.

This ADR defines the architectural semantics of plugin identity.

---

# Related RFCs

This ADR is based on the plugin architecture work represented by:

* RFC-000Y — Plugin SDK v2;
* RFC-000Z — Plugin Discovery & Distribution;
* RFC-000AA — Plugin Versioning & Compatibility;
* RFC-000AB — Plugin Dependency Graph;
* RFC-000AC — Plugin Resolution Diagnostics;
* RFC-000AD — Plugin Resolution User Experience;
* RFC-000AG — Plugin Generated Artifacts.

Historical placeholder RFC identifiers SHALL be replaced by their canonical identifiers when formally assigned through RFC governance.

---

# Related ADRs

Related decisions include:

* ADR-0008 — Specification-Driven Platform;
* ADR-0009 — Normative Validation Architecture.

Future decisions MAY define:

* plugin identity migration;
* plugin compatibility aliases;
* ecosystem package identity implementation;
* dependency declaration architecture.

---

# Architectural Invariants

The following invariants SHALL hold for the target architecture.

### Invariant 1 — Stable Logical Identity

```text
Plugin Identifier
```

is the stable logical identity of a plugin.

---

### Invariant 2 — Display Separation

```text
Plugin Display Name
≠
Plugin Identifier
```

---

### Invariant 3 — Version Separation

```text
Plugin Version
∉
Plugin Identifier
```

---

### Invariant 4 — Package Identity

```text
Concrete Plugin Package Identity
=
Plugin Identifier + Plugin Version
```

---

### Invariant 5 — Dependency Target

```text
Plugin Dependency Target
=
Plugin Identifier
```

---

### Invariant 6 — Registry Identity

```text
Plugin Registry Key
=
Plugin Identifier
```

---

### Invariant 7 — Resolution Identity

```text
Plugin Resolver Logical Key
=
Plugin Identifier
```

---

### Invariant 8 — Graph Identity

```text
Dependency Graph Logical Identity
=
Plugin Identifier
```

A concrete versioned node MAY additionally include Plugin Version.

---

### Invariant 9 — Implementation Independence

```text
Plugin Identifier
≠
Python Module
≠
Implementation Class
≠
Distribution Name
```

---

### Invariant 10 — Identity Preservation

```text
Manifest
→ Descriptor
→ Discovery
→ Package
→ Resolver
→ Dependency Graph
→ Runtime
```

SHALL preserve the same logical Plugin Identifier.

---

# Decision Summary

FamilyOS adopts a canonical, namespace-aware Plugin Identity Model.

Official Plugin Identifiers SHALL use:

```text
familyos.<plugin-name>
```

The Plugin Identifier is the stable logical identity of the plugin.

The Plugin Display Name is presentation metadata.

The Plugin Version describes evolution under a stable identity.

A concrete package is identified conceptually by:

```text
Plugin Identifier + Version
```

Plugin dependencies target Plugin Identifiers.

Registries, resolvers, dependency graphs, discovery mechanisms, and runtime components SHALL preserve canonical Plugin Identifier semantics.

The current use of human-readable `PluginDescriptor.name` as `PluginPackage.name` and subsequent resolution identity is classified as implementation debt.

Existing legacy identifiers:

```text
education
documents
communication
documentation
```

MAY remain temporarily supported.

Their canonical targets are:

```text
familyos.education
familyos.documents
familyos.communication
familyos.documentation
```

No automatic migration is authorized by this ADR.

Migration SHALL occur only after compatibility design, test coverage, and explicit implementation planning.

---

# Revision History

| Version | Status   | Description                                                                                                                                                                                                                                                                                          |
| ------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0.0   | Accepted | Initial publication of the Official Plugin Architecture decision.                                                                                                                                                                                                                                    |
| 1.1.0   | Accepted | Formalizes the canonical Plugin Identity Model, separates Plugin Identifier from display and package representations, defines dependency/resolution/graph identity semantics, documents current Plugin Ecosystem identity debt, and establishes controlled legacy identifier migration requirements. |
