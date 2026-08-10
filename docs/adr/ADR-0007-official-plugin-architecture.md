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
familyos.documentation
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
Documentation Plugin
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
PluginPackage.plugin_id
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

The canonical implementation identity property is:

```text
PluginPackage.plugin_id
```

The combination:

```text
Plugin Identifier + Version
```

SHALL distinguish a concrete plugin package version.

A package MAY expose the historical property:

```text
PluginPackage.name
```

as a compatibility alias.

Such an alias SHALL resolve to the same canonical Plugin Identifier and SHALL NOT create an independent identity.

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

The canonical implementation property is:

```text
PluginDependency.plugin_id
```

Conceptually:

```text
PluginDependency
    ├── plugin_id
    └── version_constraint
```

The historical property or constructor input:

```text
name
```

MAY remain available as a compatibility alias.

When present, it SHALL represent the same Plugin Identifier as `plugin_id`.

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

`PluginNode.plugin_id` SHALL expose canonical logical graph identity.

A historical `PluginNode.name` property MAY remain as a compatibility alias but SHALL NOT establish a separate graph identity.

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

Known legacy Plugin Identifier aliases MAY be accepted as lookup inputs.

Such aliases SHALL be normalized to canonical identity before lookup.

A registry SHALL NOT create multiple stored identities for the same plugin solely to support legacy aliases.

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
deactivate
```

SHOULD identify plugins using Plugin Identifiers.

Known legacy Plugin Identifier aliases MAY be accepted at compatibility boundaries.

Internal storage SHALL remain canonical.

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

The implemented model is:

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

# Legacy Plugin Identifiers

Historical official Plugin Identifiers include:

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

The canonical forms are now used by official plugin manifests.

Historical identifiers MAY remain accepted as compatibility inputs.

They SHALL NOT define canonical plugin identity.

---

# Legacy Compatibility Policy

FamilyOS supports explicitly governed Plugin Identifier compatibility aliases.

The currently supported aliases are:

```text
education      → familyos.education
documents      → familyos.documents
communication  → familyos.communication
documentation  → familyos.documentation
```

Compatibility normalization SHALL satisfy the following properties:

* canonical identifiers remain unchanged;
* known legacy identifiers resolve to canonical identifiers;
* unknown third-party identifiers remain unchanged;
* normalization is idempotent;
* aliases SHALL NOT create independent plugin identities;
* aliases SHALL NOT be used by new official manifests;
* aliases SHALL NOT define new production identity contracts;
* retired aliases SHALL NOT be reassigned to unrelated plugins.

Legacy support is currently classified as:

```text
legacy-compatible
```

and not as:

```text
deprecated
```

No removal schedule is established by this ADR.

Removal or deprecation SHALL require separate compatibility analysis and migration governance.

---

# Model Compatibility Aliases

The following historical model surfaces MAY remain available for compatibility:

```text
PluginPackage.name
PluginDependency.name
PluginNode.name
PluginManifest.name
```

Their canonical counterparts are:

```text
PluginPackage.plugin_id
PluginDependency.plugin_id
PluginNode.plugin_id
PluginManifest.plugin_id
```

Compatibility aliases SHALL return or represent the same canonical Plugin Identifier.

New production code SHOULD use `plugin_id`.

Compatibility aliases SHALL NOT be used to establish new architectural contracts.

No deprecation or removal schedule is established by this ADR.

---

# Plugin Identity Normalization

Legacy Plugin Identifier compatibility SHALL be implemented through an explicit normalization boundary.

Conceptually:

```text
Legacy input
    │
    ▼
Plugin Identifier Normalization
    │
    ▼
Canonical Plugin Identifier
    │
    ├── Registry
    ├── Manager
    ├── Resolver
    ├── Dependency Graph
    └── Runtime
```

Canonical storage SHALL NOT duplicate entries under both legacy and canonical identifiers.

For example:

```text
Input:
education

Normalized:
familyos.education

Stored identity:
familyos.education
```

The following storage model is prohibited:

```text
education
familyos.education
```

when both keys represent the same plugin.

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

The migration of the historical official Plugin Identifiers has followed this controlled process.

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

The runtime manifest loader does not establish a dependency-declaration implementation contract merely because the ecosystem supports `PluginDependency`.

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

Dependency resolution operates on canonical Plugin Identifiers rather than ambiguous display names.

---

### Consistent Runtime Lookup

Registry, manager, resolver, and dependency graph semantics converge on the same logical identity.

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

### Controlled Legacy Compatibility

Historical Plugin Identifiers remain available at approved compatibility boundaries without redefining canonical identity.

---

### Clearer Capability Boundaries

Plugin identity and capability identity remain distinct contracts with independent migration governance.

---

## Negative Consequences

### Compatibility Surface

Legacy aliases introduce an additional compatibility surface that must remain tested and governed.

---

### Long-Term Maintenance

Historical identifier aliases and model compatibility aliases may require maintenance until formally retired.

---

### Migration Governance

Removing compatibility aliases cannot be performed as a local refactoring.

It requires compatibility analysis and explicit governance.

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

Rejected for official plugins.

Short identifiers such as:

```text
education
documents
communication
documentation
```

do not express namespace ownership and create potential ecosystem collisions.

They MAY remain supported as compatibility aliases.

---

## Register Legacy and Canonical IDs Simultaneously

Rejected.

For example:

```text
education
familyos.education
```

MUST NOT be stored as two independent registry identities for the same plugin.

Compatibility aliases SHALL normalize to one canonical identity.

---

## Immediately Remove Legacy IDs

Rejected.

Historical identifiers may remain referenced by:

* CLI invocations;
* configuration;
* persisted state;
* generated artifacts;
* integrations;
* tests;
* external consumers.

Removal requires separate compatibility governance.

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

The architecture defined by this ADR has been implemented through:

* Plugin Runtime;
* Plugin SDK v2;
* Plugin Lifecycle Management;
* Plugin Capabilities;
* Plugin Contributions;
* Plugin Discovery;
* Plugin Resolution;
* Dependency Graph Resolution;
* Plugin Diagnostics;
* Generation Integration;
* canonical Plugin Identifier propagation;
* explicit Plugin Package identity;
* explicit Plugin Dependency identity;
* legacy Plugin Identifier normalization;
* registry and manager compatibility lookup;
* canonical official Plugin Manifest identifiers.

The implemented identity flow is:

```text
plugin.yaml id
→ PluginDescriptor.id
→ PluginPackage.plugin_id
→ PluginDependency.plugin_id
→ Plugin Resolver
→ Dependency Graph
→ diagnostics
→ runtime identity
```

Human-readable plugin names are presentation metadata and SHALL NOT be used as logical plugin identity.

---

# Migration Status

The canonical Plugin Identifier migration has been implemented for official FamilyOS plugins.

The official Plugin Identifier set is:

```text
familyos.documentation
familyos.security
familyos.health
familyos.finance
familyos.education
familyos.documents
familyos.communication
```

The completed migration includes:

1. Plugin Ecosystem package identity aligned with Plugin Identifier semantics;
2. dependency targets aligned with Plugin Identifier semantics;
3. resolver lookup aligned with Plugin Identifier semantics;
4. Dependency Graph identity aligned with Plugin Identifier semantics;
5. explicit compatibility normalization for supported legacy identifiers;
6. canonical and legacy lookup test coverage;
7. controlled migration sequencing;
8. official plugin manifests migrated to canonical identifiers;
9. production identity usage migrated from historical `.name` access to `plugin_id`;
10. diagnostic identity matching aligned with canonical Plugin Identifiers.

Legacy identifiers remain compatibility inputs only.

They SHALL NOT create independent plugin identities and SHALL NOT be used by new official plugin manifests or new production identity contracts.

---

# Validation Status

The migration has been validated through:

* canonical Plugin Identifier contract tests;
* Plugin Registry compatibility tests;
* Plugin Manager compatibility tests;
* Plugin Identifier normalizer tests;
* Plugin Package identity tests;
* Plugin Dependency identity tests;
* Plugin Manifest identity tests;
* Plugin Discovery tests;
* Plugin Resolver tests;
* Dependency Graph tests;
* resolution diagnostics tests;
* official builtin plugin runtime tests;
* full Ruff validation;
* full MyPy validation;
* full Pytest validation.

The validated repository baseline following the migration was:

```text
Ruff
PASS

MyPy
522 source files
PASS

Pytest
1122 tests
PASS
```

---

# Required Follow-Up

No further runtime migration is required for canonical official Plugin Identifiers.

Future work MAY include:

1. formal deprecation of legacy short Plugin Identifier aliases;
2. formal deprecation of historical `.name` identity aliases;
3. compatibility telemetry where appropriate;
4. release-note documentation of future alias retirement;
5. removal only after explicitly governed compatibility analysis.

Until such work is approved:

* legacy aliases MAY remain supported;
* canonical identity SHALL remain authoritative;
* new production code SHOULD use `plugin_id`;
* new official manifests MUST use canonical Plugin Identifiers;
* legacy aliases MUST NOT create duplicate stored identities.

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

These reference documents define canonical representation, reserved namespace ownership, compatibility aliases, and migration governance.

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

* plugin alias deprecation;
* plugin alias retirement;
* dependency declaration architecture;
* further plugin ecosystem compatibility mechanisms.

---

# Architectural Invariants

The following invariants SHALL hold.

---

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

### Invariant 11 — Alias Non-Identity

```text
Legacy Alias
≠
Independent Plugin Identity
```

A legacy alias MAY resolve to a canonical Plugin Identifier.

It SHALL NOT establish a second identity.

---

### Invariant 12 — Canonical Storage

```text
Canonical stored identity
=
familyos.<plugin-name>
```

Compatibility aliases SHALL NOT require duplicate storage keys for the same plugin.

---

### Invariant 13 — New Contract Canonicality

New official:

* manifests;
* dependencies;
* runtime identity contracts;
* registry integrations;
* resolver integrations;
* dependency graph integrations;

SHALL use canonical Plugin Identifiers.

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

Registries, resolvers, dependency graphs, discovery mechanisms, diagnostics, and runtime components SHALL preserve canonical Plugin Identifier semantics.

The historical identity path based on generic `.name` fields has been replaced internally by explicit `plugin_id` semantics.

The canonical official Plugin Identifier set is:

```text
familyos.documentation
familyos.security
familyos.health
familyos.finance
familyos.education
familyos.documents
familyos.communication
```

Historical identifiers:

```text
education
documents
communication
documentation
```

remain supported as governed compatibility aliases.

Their mappings are:

```text
education      → familyos.education
documents      → familyos.documents
communication  → familyos.communication
documentation  → familyos.documentation
```

Legacy aliases SHALL NOT create independent plugin identities.

New production identity contracts SHOULD use `plugin_id`.

New official plugin manifests MUST use canonical Plugin Identifiers.

No deprecation or removal schedule for the current compatibility aliases is established by this ADR.

Future retirement SHALL require explicit compatibility analysis, migration governance, tests, documentation, and release management.

---

# Revision History

| Version | Status   | Description                                                                                                                                                                                                                                                                                                                                    |
| ------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0.0   | Accepted | Initial publication of the Official Plugin Architecture decision.                                                                                                                                                                                                                                                                              |
| 1.1.0   | Accepted | Formalizes the canonical Plugin Identity Model, separates Plugin Identifier from display and package representations, defines dependency/resolution/graph identity semantics, documents Plugin Ecosystem identity debt, and establishes controlled legacy identifier migration requirements.                                                   |
| 1.2.0   | Accepted | Records implementation of canonical Plugin Identifier propagation, migration of official plugin manifests, explicit `plugin_id` contracts across ecosystem models, legacy identifier normalization, compatibility lookup behavior, elimination of internal `.name` identity dependence, and the current supported legacy-compatibility policy. |
