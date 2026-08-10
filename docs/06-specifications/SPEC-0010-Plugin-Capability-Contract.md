# SPEC-0010 — Plugin Capability Contract

**Identifier:** SPEC-0010
**Title:** Plugin Capability Contract
**Version:** 2.0.0
**Status:** Draft
**Owner:** FamilyOS Project
**Layer:** Specifications

---

# Abstract

This specification defines the normative contract for FamilyOS Plugin Capabilities.

A Plugin Capability represents a stable functional contract exposed by a plugin and made available to the FamilyOS platform through the official capability system.

This specification defines:

* capability identity;
* capability naming;
* capability ownership;
* capability metadata;
* capability versioning;
* capability declaration;
* capability providers;
* capability registration;
* capability discovery;
* capability consumption;
* capability compatibility;
* capability validation;
* capability lifecycle expectations.

Capability identifiers SHALL comply with the categorized identifier model defined by SPEC-0002 and the naming conventions defined by SPEC-0008.

For official FamilyOS plugins, capability identifiers SHALL use the canonical hierarchical form:

```text
familyos.<plugin-name>.<capability>
```

This specification does not define capability implementation internals.

---

# 1. Purpose

The purpose of this specification is to establish a stable, discoverable, namespaced, and interoperable capability contract for the FamilyOS plugin ecosystem.

A standardized capability model enables:

* loose coupling between plugins and consumers;
* explicit functional contracts;
* runtime discovery;
* deterministic registration;
* namespace ownership;
* compatibility management;
* independent plugin evolution;
* ecosystem extensibility;
* automated validation;
* long-term capability stability.

Capabilities SHALL represent functional abilities rather than implementation classes.

---

# 2. Scope

This specification applies to every capability exposed through the FamilyOS Plugin Capability system.

It applies to:

* official plugin capabilities;
* third-party plugin capabilities;
* built-in plugin capabilities;
* runtime capability providers;
* capability registries;
* capability consumers;
* capability metadata;
* capability declarations.

This specification defines:

* capability identifiers;
* capability naming;
* capability ownership;
* metadata;
* versions;
* provider responsibilities;
* registration;
* discovery;
* consumption;
* compatibility;
* validation.

This specification does not define:

* plugin lifecycle implementation;
* plugin package transport;
* plugin contribution contracts;
* internal capability implementation;
* domain-specific business behavior.

---

# 3. Normative References

This specification depends on:

* SPEC-0002 — Identifier;
* SPEC-0003 — Metadata;
* SPEC-0004 — Versioning;
* SPEC-0008 — Naming Conventions;
* SPEC-0009 — Plugin Manifest.

Related architecture decisions:

* ADR-0007 — Official Plugin Architecture.

Reference terminology and namespace rules are defined by:

* `docs/04-reference/Naming-Conventions.md`;
* `docs/04-reference/Reserved-Words.md`.

---

# 4. Terms and Definitions

## Capability

A functional contract exposed by a plugin and consumable through the FamilyOS capability system.

---

## Capability Identifier

The canonical identifier assigned to exactly one capability contract within its defined identification scope.

Example:

```text
familyos.health.record
```

Capability Identifier semantics are governed by SPEC-0002.

---

## Capability Name

A human-readable designation associated with a capability.

Example:

```text
Health Record
```

The Capability Name SHALL remain distinct from the Capability Identifier.

---

## Capability Provider

A plugin component responsible for exposing an implementation of a Capability Contract.

---

## Capability Consumer

A FamilyOS component or plugin that consumes a capability exclusively through its declared contract.

---

## Capability Contract

The stable definition of the externally observable behavior, identity, metadata, and compatibility expectations of a capability.

---

## Capability Version

A version representing the evolution of a Capability Contract under a stable Capability Identifier.

---

## Capability Registry

The authoritative runtime registry through which capabilities become discoverable.

---

## Capability Ownership

The relationship between a capability and the plugin or platform namespace authorized to expose it.

---

# 5. Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY and OPTIONAL are interpreted as defined by the FamilyOS Specification Writing Guide.

---

# 6. Capability Identity

## SPEC-0010-R1 — Exactly One Capability Identifier

Every Plugin Capability SHALL have exactly one canonical Capability Identifier.

The identifier SHALL uniquely identify the Capability Contract within the FamilyOS ecosystem.

---

## SPEC-0010-R2 — Identifier Contract

Capability Identifiers SHALL comply with:

* SPEC-0002 — Identifier;
* SPEC-0008 — Naming Conventions;
* FamilyOS reserved namespace rules.

A Capability Identifier SHALL remain distinct from:

* Capability Name;
* provider class name;
* Python module;
* plugin package name;
* capability version.

---

## SPEC-0010-R3 — Canonical Official Capability Format

Capabilities owned by official FamilyOS plugins SHALL use:

```text
familyos.<plugin-name>.<capability>
```

Examples:

```text
familyos.health.record
familyos.health.profile
familyos.finance.account
familyos.finance.transaction
familyos.finance.asset
familyos.finance.liability
familyos.finance.budget
familyos.education.learner
familyos.education.course
familyos.education.record
familyos.documents.document
familyos.documents.archive
familyos.communication.messaging
familyos.communication.archive
```

---

## SPEC-0010-R4 — Lowercase Representation

Capability Identifier segments SHALL use lowercase representation.

Whitespace SHALL NOT appear in canonical Capability Identifiers.

---

## SPEC-0010-R5 — Dot-Separated Hierarchy

Capability Identifier segments SHALL be separated by `.`.

For plugin-owned capabilities, the canonical hierarchy SHALL be:

```text
namespace
    ↓
plugin
    ↓
capability
```

Example:

```text
familyos.education.course
```

---

# 7. Capability Ownership

## SPEC-0010-R6 — Plugin Prefix

A capability owned by a plugin SHOULD use the canonical Plugin Identifier as its prefix.

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

## SPEC-0010-R7 — Official Namespace

Capabilities owned by official FamilyOS plugins SHALL use the `familyos` namespace.

Third-party capability providers MUST NOT claim the `familyos` namespace without explicit authorization.

---

## SPEC-0010-R8 — Third-Party Capability Namespace

A third-party capability SHALL use a namespace controlled by its owner.

Examples:

```text
acme.backup.archive
vendor.documents.import
example.health.exchange
```

A third-party capability MAY integrate with an official FamilyOS domain but SHALL NOT falsely imply official ownership.

---

## SPEC-0010-R9 — Namespace Preservation

A Capability Provider SHALL NOT rewrite another provider's canonical namespace.

Capability identity SHALL preserve ownership boundaries throughout:

* manifests;
* runtime registration;
* discovery;
* dependency resolution;
* diagnostics.

---

# 8. Capability Semantic Naming

## SPEC-0010-R10 — Functional Naming

The final Capability Identifier segment SHALL describe a functional ability or stable contract.

Preferred:

```text
familyos.documents.archive
familyos.communication.messaging
familyos.finance.account
```

Avoid implementation-oriented names such as:

```text
familyos.documents.document_archive_capability
familyos.finance.finance_account_capability
```

---

## SPEC-0010-R11 — Stable Semantic Meaning

A published Capability Identifier SHALL retain the same fundamental semantic meaning across compatible versions.

A provider SHALL NOT reuse an existing Capability Identifier for an unrelated capability.

---

## SPEC-0010-R12 — No Implementation Leakage

Capability Identifiers SHALL NOT encode:

* implementation class names;
* source file names;
* repository paths;
* internal service names;
* transient technical architecture.

Capability identity SHALL remain implementation-independent.

---

# 9. Capability Metadata

## SPEC-0010-R13 — Required Metadata

Every Capability Contract SHALL define metadata.

Required metadata SHALL include:

* identifier;
* name;
* version;
* description.

Metadata SHALL comply with SPEC-0003.

---

## SPEC-0010-R14 — Capability Name

The capability `name` SHALL provide a human-readable designation.

Example:

```text
Education Course
```

The name SHALL NOT be used as the canonical registry key when a Capability Identifier exists.

---

## SPEC-0010-R15 — Description

The capability description SHALL explain the functional contract exposed to consumers.

It SHOULD describe observable responsibility rather than internal implementation.

---

# 10. Capability Versioning

## SPEC-0010-R16 — Exactly One Capability Version

Every published Capability Contract SHALL define exactly one version.

---

## SPEC-0010-R17 — Version Contract

Capability versions SHALL comply with SPEC-0004.

The Capability Identifier SHALL remain separate from version information.

Canonical identity:

```text
familyos.education.course
```

Version:

```text
1.0.0
```

---

## SPEC-0010-R18 — Stable Identifier Across Compatible Versions

Compatible capability versions SHALL retain the same Capability Identifier.

Example:

```text
familyos.finance.account
1.0.0

familyos.finance.account
1.1.0
```

represent evolution of the same capability identity.

---

## SPEC-0010-R19 — Breaking Changes

A breaking Capability Contract change SHALL require a version transition consistent with SPEC-0004.

A breaking behavior change SHALL NOT be hidden under an unchanged compatibility declaration.

---

# 11. Capability Declaration

## SPEC-0010-R20 — Explicit Declaration

A plugin exposing a capability SHALL explicitly declare that capability through an official capability contract or supported manifest/runtime declaration.

Undeclared capabilities SHALL NOT be treated as official discoverable capabilities.

---

## SPEC-0010-R21 — Plugin Manifest Declaration

Where capabilities are declared in `plugin.yaml`, their identifiers SHALL use canonical Capability Identifiers.

Example:

```yaml
capabilities:
  - id: familyos.education.course
    name: Education Course
    version: 1.0.0
    description: Provides education course capabilities
```

---

## SPEC-0010-R22 — Declaration Consistency

A capability declared by a plugin SHALL correspond to a Capability Provider exposed by that plugin unless the declaration explicitly describes a deferred or externally provided contract.

Manifest declarations and runtime providers SHALL NOT disagree silently.

---

# 12. Capability Provider

## SPEC-0010-R23 — Provider Requirement

Every runtime capability SHALL be exposed through a Capability Provider recognized by the FamilyOS capability system.

---

## SPEC-0010-R24 — Provider Ownership

A Capability Provider SHALL expose only capabilities it is authorized to provide.

A provider MUST NOT register a capability under another plugin's namespace without explicit authorization.

---

## SPEC-0010-R25 — Provider Contract

A Capability Provider SHALL implement the official capability abstraction required by the active FamilyOS Plugin SDK.

Consumers SHALL depend on the capability contract rather than provider implementation details.

---

## SPEC-0010-R26 — Provider Identity Preservation

The provider SHALL expose the canonical Capability Identifier exactly.

For example:

```text
familyos.education.course
```

SHALL NOT be silently rewritten to:

```text
education.course
```

or:

```text
course
```

during registration.

---

# 13. Capability Registration

## SPEC-0010-R27 — Official Registry

Capabilities SHALL be registered through the official FamilyOS Capability Registry.

Direct publication outside governed capability registration mechanisms SHALL NOT establish an official capability contract.

---

## SPEC-0010-R28 — Registry Key

The canonical Capability Identifier SHALL serve as the identity key for capability registration and lookup unless an explicitly version-aware registry contract defines a composite key.

---

## SPEC-0010-R29 — Duplicate Capability Identity

Two incompatible Capability Contracts SHALL NOT be registered under the same canonical Capability Identifier and version.

Duplicate registration SHALL be rejected or explicitly reconciled by an approved registry policy.

---

## SPEC-0010-R30 — Registration Validation

Before registration, the runtime SHOULD validate:

* Capability Identifier syntax;
* namespace ownership;
* metadata completeness;
* version validity;
* provider availability;
* duplicate identity.

---

# 14. Capability Discovery

## SPEC-0010-R31 — Discoverability

The FamilyOS Runtime SHALL be able to discover registered capabilities through their declared contracts.

Discovery SHALL NOT require knowledge of provider implementation details.

---

## SPEC-0010-R32 — Identifier-Based Discovery

Capability discovery SHOULD support lookup by canonical Capability Identifier.

Example:

```text
familyos.documents.archive
```

---

## SPEC-0010-R33 — Metadata Discovery

Capability discovery MAY expose associated metadata including:

* name;
* version;
* description;
* owning plugin;
* compatibility information.

Canonical identity SHALL remain the primary stable reference.

---

# 15. Capability Consumption

## SPEC-0010-R34 — Contract-Only Consumption

A Capability Consumer SHALL interact with a capability through its declared contract.

A consumer SHALL NOT depend on:

* provider private classes;
* provider internal modules;
* plugin internal repositories;
* undocumented runtime state.

---

## SPEC-0010-R35 — Canonical Reference

Consumers SHOULD reference capabilities using their canonical Capability Identifier when a persisted, public, or cross-plugin reference is required.

Example:

```text
familyos.finance.account
```

---

## SPEC-0010-R36 — Cross-Plugin Consumption

A plugin MAY consume another plugin's capability only through declared capability contracts and approved dependency mechanisms.

Direct plugin-to-plugin implementation dependencies SHALL NOT establish capability compatibility.

---

# 16. Capability Compatibility

## SPEC-0010-R37 — Compatibility Requirements

Capability consumers SHALL declare compatibility requirements when behavior depends on a capability version.

---

## SPEC-0010-R38 — Version Compatibility

A consumer SHALL NOT activate against a capability version known to be incompatible with its declared requirements.

---

## SPEC-0010-R39 — Identifier Compatibility

Changing a stable Capability Identifier SHALL be treated as an identity migration.

Such migration SHALL require compatibility analysis.

---

## SPEC-0010-R40 — Provider Compatibility

A provider SHALL NOT expose incompatible contract versions under the same identity/version combination.

---

# 17. Capability Stability

## SPEC-0010-R41 — Published Contract Stability

A published Capability Contract SHALL remain stable within its declared compatible version range.

---

## SPEC-0010-R42 — Identity Immutability

Refactoring:

* implementation classes;
* module names;
* file locations;
* provider internals;

SHALL NOT require changing the Capability Identifier.

---

## SPEC-0010-R43 — Identifier Reassignment

A retired Capability Identifier MUST NOT be reassigned to a semantically unrelated capability.

Historical identity SHALL remain traceable.

---

# 18. Capability Validation

## SPEC-0010-R44 — Mandatory Validation

Capabilities SHALL be validated before becoming available for activation or consumption.

---

## SPEC-0010-R45 — Identifier Validation

Capability Identifier validation SHALL verify:

* lowercase representation;
* dot-separated syntax;
* namespace authorization;
* ownership consistency;
* absence of version suffixes;
* absence of prohibited naming patterns.

---

## SPEC-0010-R46 — Metadata Validation

Capability metadata validation SHALL verify:

* identifier;
* name;
* version;
* description.

---

## SPEC-0010-R47 — Version Validation

Capability version validation SHALL comply with SPEC-0004.

---

## SPEC-0010-R48 — Provider Validation

Validation SHALL verify that an active Capability Provider exists for a runtime capability before exposure to consumers.

---

## SPEC-0010-R49 — Registry Validation

Capability registration SHALL detect conflicting or duplicate canonical identifiers according to registry rules.

---

# 19. Plugin and Capability Identity Relationship

## SPEC-0010-R50 — Plugin Prefix Relationship

For ordinary plugin-owned capabilities:

```text
Capability Identifier prefix
=
Plugin Identifier
```

Example:

```text
Plugin Identifier:
familyos.communication

Capability Identifiers:
familyos.communication.messaging
familyos.communication.archive
```

---

## SPEC-0010-R51 — Plugin Identifier Migration Impact

Migration of a Plugin Identifier MAY affect capability identifiers when the capability namespace is derived from the Plugin Identifier.

Example:

```text
education
→ familyos.education
```

with capabilities already using:

```text
familyos.education.course
familyos.education.record
```

SHALL require explicit compatibility analysis before plugin identity migration.

---

## SPEC-0010-R52 — Independent Capability Stability

A capability already using the canonical namespace SHALL NOT be renamed merely because its owning plugin previously used a legacy short Plugin Identifier.

Example:

```text
Plugin legacy ID:
education

Capability canonical ID:
familyos.education.course
```

The capability SHALL retain its canonical identifier during plugin migration unless another independent incompatibility requires change.

---

# 20. Legacy Capability Identifiers

## SPEC-0010-R53 — Legacy Forms

Capability identifiers created before the canonical FamilyOS namespace model MAY exist in forms such as:

```text
security.validation
generation.template
documents.storage
```

Such identifiers SHALL be classified as legacy when they represent stable existing contracts.

They SHALL NOT be used as new canonical examples for official FamilyOS plugin capabilities.

---

## SPEC-0010-R54 — No Automatic Rewrite

Existing public legacy Capability Identifiers SHALL NOT be rewritten automatically.

Migration SHALL comply with SPEC-0002 compatibility requirements.

---

## SPEC-0010-R55 — Canonical Migration Target

When an official plugin capability is migrated to the canonical namespace model, the target SHOULD use:

```text
familyos.<plugin-name>.<capability>
```

Example:

```text
security.validation
→ familyos.security.validation
```

This rule defines the canonical target and does not itself authorize migration.

---

## SPEC-0010-R56 — Alias Compatibility

A runtime MAY temporarily support a legacy Capability Identifier as an alias for a canonical Capability Identifier.

Alias mappings SHALL:

* be explicit;
* preserve one canonical identity;
* be testable;
* be documented;
* avoid duplicate capability instances;
* have a retirement strategy where practical.

---

# 21. Runtime Alignment

## SPEC-0010-R57 — Runtime Identity Preservation

Capability identifiers SHALL be preserved unchanged from declaration through:

```text
Declaration
    ↓
Provider
    ↓
Registration
    ↓
Registry
    ↓
Discovery
    ↓
Consumption
```

No runtime component SHALL silently shorten or rewrite canonical identifiers.

---

## SPEC-0010-R58 — Capability Object Identity

Where a runtime capability object exposes an identifier field or property, that value SHALL represent the canonical Capability Identifier.

---

## SPEC-0010-R59 — Registry Lookup

Capability Registry lookup SHOULD use canonical Capability Identifiers.

Example:

```text
familyos.health.record
```

rather than ambiguous short forms such as:

```text
record
```

---

# 22. Security Considerations

Plugin Capabilities SHALL NOT expose:

* credentials;
* authentication secrets;
* private cryptographic material;
* confidential personal information.

Capability identifiers SHALL NOT encode sensitive data.

Namespace identifiers SHALL NOT falsely imply:

* FamilyOS ownership;
* official certification;
* endorsement;
* privileged platform status.

Capability Providers SHALL NOT bypass FamilyOS security boundaries.

Capability access SHOULD be controlled through official runtime mechanisms.

---

# 23. Compatibility

Capability Contracts SHALL define compatibility expectations.

Changes affecting:

* identity;
* behavior;
* metadata requirements;
* version semantics;
* provider contract;

SHALL be evaluated for compatibility impact.

Stable public Capability Identifiers SHALL remain unchanged across compatible releases.

A capability identity migration SHALL require:

1. affected-consumer identification;
2. compatibility analysis;
3. alias or deprecation strategy where appropriate;
4. test updates;
5. documentation updates;
6. release-note entry;
7. architectural approval.

---

# 24. Conformance

A capability conforms to this specification when:

* exactly one canonical Capability Identifier exists;
* its identifier follows SPEC-0002 and SPEC-0008;
* namespace ownership is valid;
* the capability uses stable functional naming;
* metadata is complete;
* versioning complies with SPEC-0004;
* the provider implements the official capability contract;
* registration uses the official Capability Registry;
* discovery does not depend on provider internals;
* consumers use declared contracts;
* compatibility requirements are respected;
* required validation succeeds.

Legacy capability identifiers MAY remain temporarily compatible under an approved migration strategy.

---

# Annex A — Health Capabilities

```text
Plugin Identifier:
familyos.health

Capability Identifiers:
familyos.health.profile
familyos.health.record
```

---

# Annex B — Finance Capabilities

```text
Plugin Identifier:
familyos.finance

Capability Identifiers:
familyos.finance.account
familyos.finance.transaction
familyos.finance.asset
familyos.finance.liability
familyos.finance.budget
```

---

# Annex C — Education Capabilities

```text
Plugin Identifier:
familyos.education

Capability Identifiers:
familyos.education.learner
familyos.education.course
familyos.education.record
```

An implementation MAY temporarily retain:

```text
education
```

as a legacy Plugin Identifier while its capability identifiers already use the canonical namespace.

---

# Annex D — Documents Capabilities

```text
Plugin Identifier:
familyos.documents

Capability Identifiers:
familyos.documents.document
familyos.documents.archive
```

---

# Annex E — Communication Capabilities

```text
Plugin Identifier:
familyos.communication

Capability Identifiers:
familyos.communication.messaging
familyos.communication.archive
```

---

# Annex F — Capability Declaration

```yaml
capabilities:
  - id: familyos.education.course
    name: Education Course
    version: 1.0.0
    description: Provides education course capabilities
```

---

# Annex G — Legacy Capability Migration

Legacy:

```text
security.validation
```

Canonical target:

```text
familyos.security.validation
```

Possible compatibility mapping:

```text
security.validation
    ↓ alias
familyos.security.validation
```

The canonical identity SHALL remain:

```text
familyos.security.validation
```

---

# Annex H — Identity and Version Separation

```text
Capability Identifier:
familyos.documents.archive

Version:
1.0.0
```

A representation such as:

```text
familyos.documents.archive@1.0.0
```

MAY be supported for display or resolution purposes.

The version suffix SHALL NOT be part of the canonical Capability Identifier.

---

# 25. Normative References

* SPEC-0002 — Identifier;
* SPEC-0003 — Metadata;
* SPEC-0004 — Versioning;
* SPEC-0008 — Naming Conventions;
* SPEC-0009 — Plugin Manifest;
* ADR-0007 — Official Plugin Architecture;
* `docs/04-reference/Naming-Conventions.md`;
* `docs/04-reference/Reserved-Words.md`;
* FamilyOS Specification Writing Guide.

---

# 26. Revision History

| Version | Status | Description                                                                                                                                                                                                                                                                                                     |
| ------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0.0   | Draft  | Initial publication of the Plugin Capability Contract specification.                                                                                                                                                                                                                                            |
| 2.0.0   | Draft  | Aligns capability identity with the categorized identifier model, establishes `familyos.<plugin-name>.<capability>` as the canonical official capability format, formalizes namespace ownership and runtime identity preservation, and introduces explicit legacy capability compatibility and migration rules. |
