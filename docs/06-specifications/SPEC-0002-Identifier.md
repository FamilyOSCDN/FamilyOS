# SPEC-0002 — Identifier

**Identifier:** SPEC-0002
**Title:** Identifier
**Version:** 2.0.0
**Status:** Draft
**Owner:** FamilyOS Project
**Layer:** Specifications

---

# Abstract

This specification defines the normative requirements for identifiers used throughout the FamilyOS platform.

Identifiers provide stable, unique, persistent, and unambiguous references for governed documents, platform resources, plugins, capabilities, domains, artifacts, events, commands, and other technical entities.

FamilyOS recognizes that different identifier categories serve different architectural purposes.

Governance identifiers provide stable references for governed documents and decisions.

Ecosystem identifiers provide stable namespaced identities for runtime and extensibility resources.

Capability identifiers provide stable hierarchical identities for functional contracts exposed through the FamilyOS capability system.

Category-specific identifiers MAY define additional syntax where required by their governing specifications.

All FamilyOS components SHALL comply with the common identifier principles defined by this specification and with the syntax defined for their identifier category.

---

# 1. Purpose

The purpose of this specification is to establish a coherent identification model for the FamilyOS platform.

A common identification model enables:

* interoperability;
* traceability;
* stable references;
* namespace ownership;
* ecosystem extensibility;
* automated validation;
* compatibility management;
* documentation consistency;
* long-term maintainability.

This specification distinguishes identifier semantics from display names, implementation names, package names, file names, and version numbers.

An identifier represents identity.

A name represents human-readable designation.

A version represents evolution of an identified entity.

These concepts SHALL NOT be treated as interchangeable.

---

# 2. Scope

This specification applies to permanent identifiers used throughout FamilyOS, including but not limited to:

* Specifications;
* Architecture Decision Records;
* Requests for Comments;
* plugins;
* capabilities;
* domains;
* contributions;
* artifacts;
* recipes;
* presets;
* commands;
* events;
* queries;
* aggregates;
* value objects;
* extension resources;
* ecosystem resources.

This specification applies to identifiers exposed through:

* documentation;
* specifications;
* manifests;
* the Plugin SDK;
* runtime registries;
* CLI interfaces;
* generated artifacts;
* public APIs;
* extension points;
* ecosystem metadata.

This specification does not define runtime-generated instance identifiers such as UUIDs created for transient or domain-specific execution data unless another specification explicitly adopts these rules.

---

# 3. Normative References

This specification is related to:

* SPEC-0001 — Documentation Structure;
* SPEC-0003 — Metadata;
* SPEC-0004 — Versioning;
* SPEC-0008 — Naming Conventions;
* SPEC-0009 — Plugin Manifest;
* SPEC-0010 — Plugin Capability Contract;
* ADR-0007 — Official Plugin Architecture;
* FamilyOS Specification Writing Guide.

Category-specific specifications MAY impose additional identifier requirements.

Such requirements SHALL remain compatible with the common principles defined by this specification.

---

# 4. Terms and Definitions

## Identifier

A permanent textual value used to uniquely identify an entity within a defined identification scope.

---

## Entity

Any governed, documented, modeled, implemented, exposed, or registered object that requires stable identity within FamilyOS.

---

## Identifier Category

A class of identifiers sharing a common architectural purpose and syntax.

FamilyOS defines the following primary categories:

* Governance Identifier;
* Ecosystem Identifier;
* Capability Identifier;
* Category-Specific Identifier.

---

## Governance Identifier

An identifier assigned to a governed platform artifact such as a specification, architecture decision, or request for comments.

Examples:

```text
SPEC-0002
ADR-0007
RFC-0010
```

---

## Ecosystem Identifier

A namespaced identifier assigned to a persistent resource participating in the FamilyOS ecosystem.

Plugins are primary examples of ecosystem resources.

Examples:

```text
familyos.security
familyos.health
familyos.education
acme.backup
```

---

## Plugin Identifier

An Ecosystem Identifier assigned to exactly one plugin.

A Plugin Identifier is independent from:

* plugin display name;
* package name;
* import package;
* implementation class;
* version.

Example:

```text
familyos.security
```

---

## Capability Identifier

A stable hierarchical identifier assigned to a capability exposed through the FamilyOS capability system.

Examples:

```text
familyos.security.audit
familyos.health.record
familyos.education.course
```

---

## Category-Specific Identifier

An identifier whose syntax is defined by another approved specification because its architectural requirements differ from the primary identifier categories.

A category-specific syntax SHALL NOT weaken the common requirements for stability, ownership, uniqueness, and compatibility defined by this specification.

---

## Namespace

The ownership portion of an ecosystem identifier.

Example:

```text
familyos.security
```

contains the namespace:

```text
familyos
```

---

## Qualified Identifier

An identifier containing sufficient namespace information to remain unambiguous within its intended ecosystem scope.

Example:

```text
familyos.education
```

---

## Display Name

A human-readable designation for an entity.

Example:

```text
FamilyOS Education Plugin
```

A display name SHALL NOT be treated as the canonical identifier unless explicitly specified.

---

## Version

A value representing the evolution of an identified entity.

Example:

```text
1.0.0
```

A version SHALL remain separate from the canonical identifier unless a category-specific specification explicitly defines otherwise.

---

# 5. Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY and OPTIONAL are to be interpreted as described by the FamilyOS Specification Writing Guide.

---

# 6. Common Identifier Requirements

## SPEC-0002-R1 — Uniqueness

Every permanent identifier MUST uniquely identify exactly one entity within its defined identification scope.

Two distinct entities SHALL NOT share the same canonical identifier within that scope.

---

## SPEC-0002-R2 — Permanence

A permanent identifier MUST remain stable for the lifetime of the identified entity unless an explicitly governed compatibility migration is approved.

An identifier SHALL NOT be reassigned to a different entity.

---

## SPEC-0002-R3 — Human Readability

Identifiers SHOULD remain concise and readable where doing so does not compromise uniqueness, ownership, or stability.

Abbreviations SHOULD be governed and consistently applied.

---

## SPEC-0002-R4 — Explicit Category

Every permanent identifier SHALL belong to a defined identifier category.

The identifier category determines:

* syntax;
* namespace requirements;
* ownership rules;
* validation rules;
* identification scope.

A component SHALL NOT infer identifier semantics solely from an arbitrary string value.

---

## SPEC-0002-R5 — Stable Syntax

Every identifier SHALL follow the syntax defined for its identifier category.

The `<PREFIX>-<NUMBER>` syntax SHALL apply to Governance Identifiers.

It SHALL NOT be interpreted as the universal syntax for all FamilyOS identifiers.

---

## SPEC-0002-R6 — Case

Case requirements SHALL be determined by identifier category.

Governance Identifier prefixes SHALL use uppercase letters.

Ecosystem and Capability Identifiers SHALL use lowercase identifiers unless a category-specific specification explicitly defines another representation.

Canonical identifiers SHALL be treated consistently according to their category-specific case rules.

---

## SPEC-0002-R7 — References

Documentation SHOULD reference governed entities by canonical identifier whenever a stable identifier exists.

Example:

```text
See SPEC-0002.
```

Runtime and ecosystem resources SHOULD likewise be referenced by their canonical qualified identifier when ambiguity is possible.

Example:

```text
familyos.security
```

---

## SPEC-0002-R8 — Identity Immutability

Changing an entity's:

* title;
* display name;
* description;
* implementation;
* file location;
* package location;

MUST NOT by itself require changing the entity's canonical identifier.

Identity SHALL remain independent from incidental implementation structure.

---

## SPEC-0002-R9 — Traceability

Identifiers SHOULD remain usable across relevant FamilyOS surfaces, including:

* documentation;
* architecture decisions;
* specifications;
* manifests;
* tests;
* source code;
* runtime registries;
* generated artifacts;
* diagnostics.

---

## SPEC-0002-R10 — Version Independence

Canonical identifiers MUST NOT include version information unless explicitly required by a category-specific specification.

For plugins:

```text
familyos.security
```

is an identifier.

The following representation:

```text
familyos.security@1.0.0
```

MAY be used where an identifier and version must be displayed together, but:

```text
@1.0.0
```

SHALL NOT be part of the canonical Plugin Identifier.

---

## SPEC-0002-R11 — Ownership

Every namespaced identifier SHALL have an identifiable owner.

An entity MUST NOT use a namespace it is not authorized to control.

Namespace ownership SHALL comply with FamilyOS reserved-word and governance rules.

---

## SPEC-0002-R12 — Compatibility

A stable public identifier MUST NOT be changed without compatibility analysis.

A public identifier includes identifiers exposed through:

* plugin manifests;
* Plugin SDK contracts;
* runtime registries;
* CLI interfaces;
* specifications;
* generated artifacts;
* documented extension points;
* public APIs.

---

# 7. Governance Identifiers

## SPEC-0002-R13 — Governance Identifier Syntax

Governance Identifiers SHALL use the syntax:

```text
<PREFIX>-<NUMBER>
```

The prefix SHALL identify the governed artifact category.

The number SHALL provide a stable category-local identity.

Examples:

```text
SPEC-0002
ADR-0007
RFC-0010
```

---

## SPEC-0002-R14 — Governance Prefix

Governance Identifier prefixes SHALL:

* use uppercase ASCII letters;
* have an approved meaning;
* remain stable;
* identify exactly one governance category.

Examples:

```text
SPEC
ADR
RFC
```

New governance prefixes SHALL require governance approval.

---

## SPEC-0002-R15 — Governance Number

A governance number SHALL:

* contain the number of digits defined by its governing process;
* be unique within its prefix;
* never be reassigned;
* remain stable after publication.

Where no category-specific rule exists, four digits SHOULD be used.

Example:

```text
ADR-0007
```

---

# 8. Ecosystem Identifiers

## SPEC-0002-R16 — Ecosystem Identifier Syntax

Ecosystem Identifiers SHALL use stable lowercase dot-separated segments.

General form:

```text
<namespace>.<resource>
```

Additional segments MAY be defined when required.

Examples:

```text
familyos.security
familyos.health
familyos.education
acme.backup
vendor.documents.archive
```

---

## SPEC-0002-R17 — Namespace Ownership

The first segment of an Ecosystem Identifier SHALL represent an authorized namespace.

The namespace:

```text
familyos
```

is reserved for official FamilyOS resources.

Third-party extensions MUST NOT use the `familyos` namespace without explicit authorization.

Third-party extensions SHOULD use a namespace they control.

Examples:

```text
acme.backup
example.health.import
vendor.documents.archive
```

---

## SPEC-0002-R18 — Official Plugin Identifiers

Official FamilyOS Plugin Identifiers SHALL use the `familyos` namespace.

Canonical form:

```text
familyos.<plugin-name>
```

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

The plugin name segment SHALL be:

* lowercase;
* stable;
* unambiguous;
* governed by official FamilyOS naming and reserved-word rules.

---

## SPEC-0002-R19 — Plugin Identifier Stability

A published Plugin Identifier SHALL remain stable across compatible plugin versions.

The following changes SHALL NOT automatically change a Plugin Identifier:

* implementation refactoring;
* package relocation;
* class renaming;
* display-name changes;
* internal architecture changes.

A Plugin Identifier change SHALL be treated as a compatibility-sensitive identity migration.

---

# 9. Capability Identifiers

## SPEC-0002-R20 — Capability Identifier Syntax

Capability Identifiers SHALL use lowercase dot-separated hierarchical names.

Canonical form for capabilities owned by an official plugin:

```text
familyos.<plugin-name>.<capability>
```

Examples:

```text
familyos.security.audit
familyos.health.record
familyos.health.profile
familyos.finance.account
familyos.education.learner
familyos.education.course
familyos.education.record
familyos.documents.document
familyos.documents.archive
familyos.communication.messaging
familyos.communication.archive
```

Additional hierarchy MAY be introduced when required by an approved capability contract.

---

## SPEC-0002-R21 — Capability Ownership

A capability identifier SHALL remain within the namespace of its owning or governing ecosystem resource unless an approved platform contract defines otherwise.

A plugin MUST NOT publish a capability under another owner's namespace without authorization.

---

## SPEC-0002-R22 — Capability Stability

A published Capability Identifier SHALL remain stable within compatible versions of the capability contract.

A breaking identity change SHALL require:

* compatibility analysis;
* migration strategy;
* deprecation where applicable;
* release documentation.

---

# 10. Domain and Category-Specific Identifiers

## SPEC-0002-R23 — Domain Identifiers

Domain identifiers MAY use a category-specific syntax defined by the FamilyOS domain architecture and naming conventions.

A normalized domain identifier SHALL NOT automatically be interpreted as a Plugin Identifier.

For example:

```text
education
```

MAY identify the normalized Education domain, while:

```text
familyos.education
```

identifies the official Education Plugin.

The two identifiers represent different identification contexts.

---

## SPEC-0002-R24 — Category-Specific Syntax

A category-specific specification MAY define identifier syntax different from:

```text
<PREFIX>-<NUMBER>
```

or:

```text
<namespace>.<resource>
```

when required by the category's architecture.

Such a specification SHALL define:

* identification scope;
* syntax;
* uniqueness rules;
* ownership rules where applicable;
* stability requirements;
* compatibility requirements.

---

## SPEC-0002-R25 — Specialization

When a category-specific specification defines additional identifier requirements, those requirements SHALL specialize this specification.

A specialized identifier contract MUST remain compliant with the common requirements defined in Section 6.

A category-specific specification SHALL NOT silently redefine identifier semantics.

---

# 11. Identifier Separation

## SPEC-0002-R26 — Identifier and Name Separation

Canonical identifiers and display names SHALL be represented separately when both concepts exist.

Example:

```text
Plugin Identifier:
familyos.education

Display Name:
FamilyOS Education Plugin
```

---

## SPEC-0002-R27 — Identifier and Version Separation

Canonical identifiers and versions SHALL be represented separately.

Example:

```text
Plugin Identifier:
familyos.education

Version:
1.0.0
```

---

## SPEC-0002-R28 — Identifier and Package Separation

A Plugin Identifier SHALL NOT be inferred from the Python distribution name, import package, or implementation class.

Example:

```text
Plugin Identifier:
familyos.security

Python distribution:
familyos-security-plugin

Python import package:
familyos_security_plugin

Plugin class:
SecurityPlugin
```

Each representation serves a different responsibility.

---

# 12. Validation

## SPEC-0002-R29 — Identifier Validation

Components accepting public or persistent identifiers SHALL validate identifiers according to their category.

Validation SHOULD occur at the earliest stable contract boundary.

Validation MAY verify:

* syntax;
* case;
* namespace authorization;
* prohibited segments;
* reserved namespaces;
* uniqueness;
* category-specific constraints.

---

## SPEC-0002-R30 — Plugin Manifest Validation

Plugin Manifest identifiers SHALL be validated before a plugin becomes eligible for installation or activation.

Plugin identifier validation SHALL be consistent with:

* this specification;
* SPEC-0009 — Plugin Manifest;
* official naming conventions;
* reserved namespace rules.

---

## SPEC-0002-R31 — Capability Validation

Capability identifiers SHALL be validated before capability registration or activation.

Validation SHALL preserve namespace ownership and identifier uniqueness.

---

# 13. Compatibility and Migration

## SPEC-0002-R32 — Existing Identifiers

Existing identifiers that predate the current identifier model SHALL NOT be renamed automatically.

They SHOULD be classified as:

* compliant;
* legacy-compatible;
* deprecated;
* scheduled for migration;
* explicitly exempted.

---

## SPEC-0002-R33 — Public Identifier Migration

Changing a stable public identifier SHALL require:

1. identification of affected consumers;
2. dependency analysis;
3. compatibility strategy;
4. aliasing or deprecation strategy where appropriate;
5. migration documentation;
6. test updates;
7. release-note entry;
8. architectural approval.

---

## SPEC-0002-R34 — Identifier Reassignment

A deprecated or retired identifier MUST NOT be reassigned to a different entity.

Historical identity SHALL remain traceable.

---

## SPEC-0002-R35 — Legacy Compatibility

A legacy identifier MAY remain temporarily supported when immediate migration would introduce disproportionate compatibility risk.

Temporary compatibility SHALL NOT redefine the canonical identifier convention.

Legacy support SHOULD have an explicit migration or retirement strategy when the identifier is externally visible.

---

# 14. Constraints

Identifiers SHALL:

* remain implementation-independent;
* avoid semantic ambiguity;
* avoid unauthorized namespace usage;
* avoid duplication within their defined scope;
* remain stable across compatible releases;
* remain separate from version information;
* preserve ownership boundaries.

Identifier meaning SHALL NOT depend solely on:

* file paths;
* implementation classes;
* package locations;
* transient runtime state.

---

# 15. Conformance

The following components are subject to this specification where they define or consume permanent identifiers:

* documentation;
* specifications;
* CLI;
* generation framework;
* Plugin SDK;
* Plugin Ecosystem;
* Plugin Runtime;
* official plugins;
* third-party plugin contracts;
* capability registries;
* plugin manifests;
* generated artifacts;
* future FamilyOS tooling.

A component conforms when:

* every permanent identifier belongs to a defined category;
* identifiers follow their category syntax;
* uniqueness requirements are respected;
* ownership rules are respected;
* stable identifiers are not reassigned;
* public identifier changes follow compatibility requirements.

---

# 16. Security Considerations

Identifiers SHALL NOT contain:

* credentials;
* authentication secrets;
* private cryptographic material;
* confidential personal information;
* security-sensitive implementation details.

Namespaced identifiers SHALL NOT falsely imply ownership, authorization, endorsement, or official FamilyOS status.

Namespace validation SHOULD be performed when accepting externally supplied plugin or capability identifiers.

---

# 17. Examples

## 17.1 Governance Identifiers

```text
SPEC-0002
ADR-0007
RFC-0010
```

---

## 17.2 Official Plugin Identifiers

```text
familyos.security
familyos.health
familyos.finance
familyos.education
familyos.documents
familyos.communication
familyos.documentation
```

---

## 17.3 Third-Party Plugin Identifiers

```text
acme.backup
example.health.import
vendor.documents.archive
```

---

## 17.4 Capability Identifiers

```text
familyos.security.audit
familyos.health.record
familyos.finance.account
familyos.education.course
familyos.documents.archive
familyos.communication.messaging
```

---

## 17.5 Separate Identity and Version

```text
Identifier:
familyos.security

Version:
1.0.0
```

Representational form:

```text
familyos.security@1.0.0
```

The version suffix is not part of the canonical identifier.

---

## 17.6 Domain and Plugin Identity

```text
Domain:
Education

Normalized domain identifier:
education

Official Plugin Identifier:
familyos.education
```

---

# 18. References

Related documents:

* SPEC-0001 — Documentation Structure;
* SPEC-0003 — Metadata;
* SPEC-0004 — Versioning;
* SPEC-0008 — Naming Conventions;
* SPEC-0009 — Plugin Manifest;
* SPEC-0010 — Plugin Capability Contract;
* ADR-0007 — Official Plugin Architecture;
* `docs/04-reference/Naming-Conventions.md`;
* `docs/04-reference/Reserved-Words.md`;
* FamilyOS Specification Writing Guide.

---

# 19. Revision History

| Version | Status   | Description                                                                                                                                                                                                                                   |
| ------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0.0   | Approved | Initial publication of the Identifier specification.                                                                                                                                                                                          |
| 2.0.0   | Draft    | Introduces explicit identifier categories, separates governance identifiers from ecosystem and capability identifiers, defines official FamilyOS namespace rules, and establishes compatibility requirements for legacy identifier migration. |
