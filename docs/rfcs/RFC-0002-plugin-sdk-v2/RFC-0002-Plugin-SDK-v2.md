# RFC-0002 — Plugin SDK v2

## Status

Accepted

## Summary

RFC-0002 defines the public Plugin SDK contracts available to FamilyOS plugin developers.

Plugin SDK v2 establishes the stable boundary between plugin implementations and the FamilyOS platform. Plugins depend on public SDK contracts and documented extension points rather than internal core implementations.

The SDK covers plugin contracts, lifecycle contracts, capability contracts, contribution contracts, and identity-related contracts where required.

## Context

FamilyOS provides an extensible plugin architecture in which plugins add capabilities without becoming coupled to private platform implementation details.

The Plugin SDK is the public contract surface of that architecture.

The canonical architecture requires plugins to depend only on stable public contracts. Internal core implementations, private domain models, infrastructure implementations, and unstable internal APIs are outside the supported plugin boundary.

Plugin SDK v2 is already part of the implemented FamilyOS Plugin Architecture.

## Goals

Plugin SDK v2 SHALL:

- provide stable public contracts for plugin implementations;
- define plugin lifecycle integration contracts;
- define capability contracts;
- define contribution contracts;
- expose identity-related contracts where required;
- preserve canonical Plugin Identifier semantics;
- isolate plugins from internal FamilyOS implementation details;
- support controlled ecosystem evolution;
- preserve backward compatibility whenever practical.

## Non-Goals

RFC-0002 does not define:

- plugin discovery and distribution;
- plugin version resolution algorithms;
- dependency graph resolution;
- resolution diagnostics;
- CLI diagnostic presentation;
- plugin-generated artifact execution;
- remote plugin registries;
- marketplace behavior;
- plugin trust or sandboxing policies.

Those concerns are governed by their respective architectural contracts and RFCs.

## Architectural Boundary

The supported dependency direction is:

```text
FamilyOS Core
        |
        v
Plugin Runtime
        |
        v
Plugin Extensions
```

Plugins MAY depend on:

- public FamilyOS contracts;
- documented extension points;
- Plugin SDK capabilities.

Plugins MUST NOT depend directly on:

- internal core implementations;
- private domain models;
- infrastructure implementations;
- unstable internal APIs.

The SDK therefore acts as the stable compatibility boundary between plugin code and the FamilyOS platform.

## Public SDK Contracts

Plugin SDK v2 SHALL provide contracts for the following areas.

### Plugin Contract

The plugin contract defines the minimum public interface required for a plugin to participate in the FamilyOS ecosystem.

Plugin implementations SHALL depend on the public contract rather than runtime implementation details.

### Lifecycle Contract

Plugins participate in a lifecycle managed by the FamilyOS runtime.

Lifecycle integration SHALL remain controlled by platform contracts.

Plugins SHALL NOT bypass the managed lifecycle by depending on runtime internals.

### Capability Contract

Capabilities define functional services exposed by plugins.

A capability SHALL:

- have a unique identifier;
- declare its purpose;
- expose a stable contract.

Capability identity SHALL remain distinct from Plugin Identifier identity.

### Contribution Contract

Contributions define resources supplied by plugins through official extension points.

Supported contribution categories include:

- generation contributions;
- recipe contributions;
- template contributions;
- domain contributions.

Contribution identity SHALL remain distinct from Plugin Identifier identity.

### Identity Contracts

Public SDK contracts involving plugin identity SHALL use canonical Plugin Identifier semantics.

Known legacy Plugin Identifier aliases MAY be accepted at compatibility boundaries.

Internal storage SHALL remain canonical.

Official plugin capability identifiers SHALL follow the applicable FamilyOS specifications.

## Plugin Isolation

Plugins SHALL remain isolated from each other's internal implementation.

A plugin MAY consume another plugin capability only through declared public contracts.

Implementation modules SHALL NOT become cross-plugin integration mechanisms.

This preserves:

- platform stability;
- plugin independence;
- maintainability;
- compatibility;
- controlled extensibility.

## Compatibility

Plugin SDK changes SHALL preserve backward compatibility whenever practical.

Changes affecting plugin contracts or lifecycle behavior SHALL follow FamilyOS architectural governance.

Changes affecting canonical Plugin Identifier semantics SHALL remain aligned with the applicable specifications and reference documentation.

Historical identifiers MAY remain accepted at compatibility boundaries when required for existing CLI invocations, configuration, persisted state, generated artifacts, integrations, tests, or external consumers.

Removal of compatibility behavior requires explicit governance.

## Extension Model

Plugin SDK v2 participates in the FamilyOS extension model through documented contracts and registries.

Plugins MAY expose capabilities and contributions through official extension points.

The platform retains ownership of:

- runtime lifecycle management;
- validation;
- registration;
- canonical identity handling;
- execution frameworks owned by FamilyOS.

Plugins retain ownership of their implementation behind the public SDK boundary.

## Governance

The Plugin SDK SHALL evolve through:

- Architecture Decision Records;
- Specifications;
- Requests for Comments.

Changes affecting public SDK contracts require explicit architectural review.

Backward-incompatible changes require explicit compatibility and migration consideration.

The SDK SHALL NOT expose internal implementation details merely for convenience.

## Implementation Status

Plugin SDK v2 is part of the implemented FamilyOS Plugin Architecture.

The implemented architecture includes:

- Plugin Runtime;
- Plugin SDK v2;
- Plugin Lifecycle Management;
- Plugin Capabilities;
- Plugin Contributions;
- Plugin Discovery;
- Plugin Resolution;
- Dependency Graph Resolution;
- Plugin Diagnostics;
- Generation Integration;
- canonical Plugin Identifier propagation;
- explicit Plugin Package identity;
- explicit Plugin Dependency identity;
- legacy Plugin Identifier normalization;
- registry and manager compatibility lookup;
- canonical official Plugin Manifest identifiers.

RFC-0002 canonicalizes the previously referenced historical placeholder identifier `RFC-000Y`.

## Acceptance Criteria

RFC-0002 is accepted when the FamilyOS architecture provides:

1. public plugin contracts independent of private runtime implementation;
2. managed lifecycle contracts;
3. stable capability contracts;
4. stable contribution contracts;
5. canonical Plugin Identifier semantics at public identity boundaries;
6. controlled compatibility behavior for legacy identifiers where required;
7. documented dependency boundaries preventing plugins from relying on internal platform implementations;
8. architectural governance for future SDK evolution.

The current FamilyOS Plugin Architecture declares Plugin SDK v2 implemented; therefore this RFC is published with status **Accepted**.

## Related Documents

- ADR-0007 — Official Plugin Architecture
- Plugin Architecture foundation documentation
- Plugin SDK Specification
- RFC-0003 — Plugin Discovery & Distribution
- RFC-0004 — Plugin Versioning & Compatibility
- RFC-0005 — Plugin Dependency Graph
- RFC-0006 — Plugin Resolution Diagnostics
- RFC-0007 — Plugin Resolution User Experience
- RFC-0008 — Plugin Generated Artifacts

---

## Revision History

| Version | Date       | Description                                                               |
| ------- | ---------- | ------------------------------------------------------------------------- |
| 1.0.0   | 2026-08-12 | Canonical publication replacing the historical RFC-000Y placeholder identifier. |
