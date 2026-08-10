# SPEC-0009 — Plugin Manifest

**Identifier:** SPEC-0009
**Title:** Plugin Manifest
**Version:** 2.0.0
**Status:** Draft
**Owner:** FamilyOS Project
**Layer:** Specifications

---

# Abstract

This specification defines the normative requirements for the FamilyOS Plugin Manifest.

The Plugin Manifest is the authoritative machine-readable description of a plugin package.

It provides the information required by the FamilyOS Plugin Ecosystem to:

* identify plugins;
* describe plugin metadata;
* verify compatibility;
* resolve dependencies;
* declare capabilities;
* declare contributions;
* prepare installation;
* support runtime loading.

This specification defines:

* manifest existence;
* manifest location;
* manifest structure;
* plugin identity;
* plugin metadata;
* plugin version;
* compatibility requirements;
* dependency declarations;
* capability declarations;
* contribution declarations;
* manifest validation.

Plugin identity SHALL comply with the categorized identifier model defined by SPEC-0002.

Plugin naming SHALL comply with SPEC-0008.

This specification does not define plugin implementation behavior or runtime lifecycle semantics.

---

# 1. Purpose

The purpose of this specification is to establish a stable, explicit, interoperable, and machine-readable contract for FamilyOS plugin manifests.

A standardized Plugin Manifest enables:

* deterministic plugin discovery;
* stable plugin identity;
* dependency resolution;
* compatibility verification;
* ecosystem interoperability;
* automated validation;
* controlled installation;
* runtime preparation;
* long-term plugin evolution.

The manifest SHALL serve as the authoritative declaration of plugin package identity and externally relevant plugin metadata.

---

# 2. Scope

This specification applies to every plugin package intended to participate in the FamilyOS Plugin Ecosystem.

It defines requirements for:

* official FamilyOS plugins;
* third-party plugins;
* built-in plugins;
* distributable plugins;
* future ecosystem plugins.

This specification defines:

* manifest filename;
* manifest location;
* manifest structure;
* Plugin Identifier;
* plugin display name;
* plugin version;
* plugin metadata;
* compatibility requirements;
* dependency declarations;
* capability declarations;
* contribution declarations;
* validation requirements.

This specification does not define:

* plugin execution behavior;
* lifecycle transitions;
* internal plugin architecture;
* capability implementation;
* contribution implementation;
* package transport;
* repository protocol.

---

# 3. Normative References

This specification depends on:

* SPEC-0002 — Identifier;
* SPEC-0003 — Metadata;
* SPEC-0004 — Versioning;
* SPEC-0007 — File Format;
* SPEC-0008 — Naming Conventions.

Capability declarations additionally depend on:

* SPEC-0010 — Plugin Capability Contract.

Related architecture decisions:

* ADR-0007 — Official Plugin Architecture.

Reference terminology and reserved namespace rules are defined by:

* `docs/04-reference/Naming-Conventions.md`;
* `docs/04-reference/Reserved-Words.md`.

---

# 4. Terms and Definitions

## Plugin

An extension package integrating with FamilyOS through official plugin contracts.

---

## Plugin Manifest

The authoritative machine-readable document describing a plugin package.

---

## Plugin Identifier

The canonical Ecosystem Identifier assigned to exactly one plugin.

Plugin Identifier semantics are governed by SPEC-0002.

Example:

```text
familyos.security
```

---

## Plugin Display Name

A human-readable designation associated with a plugin.

Example:

```text
FamilyOS Security Plugin
```

The display name SHALL remain distinct from the Plugin Identifier.

---

## Plugin Version

A value representing the evolution of a plugin under a stable Plugin Identifier.

Example:

```text
1.0.0
```

Plugin version semantics are governed by SPEC-0004.

---

## Plugin Dependency

A declared requirement on another plugin or governed platform resource.

---

## Plugin Capability

A functional contract exposed by a plugin.

---

## Plugin Contribution

A declared resource or extension provided by a plugin through an approved contribution contract.

---

## Plugin Package

A distributable or loadable unit containing a plugin implementation and associated resources.

---

# 5. Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY and OPTIONAL are interpreted as defined by the FamilyOS Specification Writing Guide.

---

# 6. Manifest Requirements

## SPEC-0009-R1 — Manifest Existence

Every FamilyOS plugin package SHALL provide exactly one Plugin Manifest.

---

## SPEC-0009-R2 — Manifest Filename

The canonical manifest filename SHALL be:

```text
plugin.yaml
```

A plugin package SHALL NOT expose multiple authoritative manifests under different names.

---

## SPEC-0009-R3 — Manifest Format

The Plugin Manifest SHALL use YAML unless another manifest representation is explicitly approved by a future compatible specification.

The manifest SHALL comply with SPEC-0007 — File Format.

---

## SPEC-0009-R4 — Manifest Location

The Plugin Manifest SHALL be located at the root of the plugin package or at the canonical plugin root recognized by the FamilyOS Plugin Loader.

Example:

```text
plugin-package/
├── plugin.yaml
├── src/
└── resources/
```

A manifest location SHALL NOT depend on transient runtime paths.

---

# 7. Plugin Identity

## SPEC-0009-R5 — Exactly One Plugin Identifier

Every Plugin Manifest SHALL define exactly one canonical Plugin Identifier.

The Plugin Identifier SHALL uniquely identify the plugin within the FamilyOS Plugin Ecosystem.

---

## SPEC-0009-R6 — Identifier Contract

Plugin Identifiers SHALL comply with:

* SPEC-0002 — Identifier;
* SPEC-0008 — Naming Conventions;
* FamilyOS reserved namespace rules.

The Plugin Identifier SHALL be represented independently from:

* display name;
* version;
* package name;
* implementation class;
* file-system path.

---

## SPEC-0009-R7 — Official Plugin Identifier Format

Official FamilyOS plugins SHALL use:

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

The `familyos` namespace is reserved for official FamilyOS resources.

---

## SPEC-0009-R8 — Third-Party Plugin Identifier Format

Third-party plugins SHALL use a namespace they are authorized to control.

Examples:

```text
acme.backup
example.health.import
vendor.documents.archive
```

A third-party plugin MUST NOT use the `familyos` namespace without explicit authorization.

---

## SPEC-0009-R9 — Plugin Identifier Stability

A published Plugin Identifier SHALL remain stable across compatible plugin versions.

Changes to:

* implementation classes;
* package layout;
* source directories;
* display names;
* internal architecture;

SHALL NOT automatically change the Plugin Identifier.

---

## SPEC-0009-R10 — Plugin Identifier Migration

A change to a stable Plugin Identifier SHALL be treated as an identity migration.

Such migration SHALL require:

* compatibility analysis;
* affected-consumer identification;
* dependency analysis;
* migration strategy;
* alias or deprecation strategy where appropriate;
* test updates;
* documentation updates;
* release-note entry;
* architectural approval.

Existing legacy identifiers SHALL NOT be renamed automatically.

---

# 8. Manifest Structure

## SPEC-0009-R11 — Canonical Fields

A Plugin Manifest SHALL define, at minimum:

```yaml
id: familyos.security
name: FamilyOS Security Plugin
version: 1.0.0
description: Security capabilities for FamilyOS
module: familyos_cli.plugins.builtin.security.plugin
class: SecurityPlugin
```

Additional fields MAY be defined by this or future compatible specifications.

---

## SPEC-0009-R12 — Flat Manifest Compatibility

The canonical FamilyOS runtime MAY support a flat manifest representation such as:

```yaml
id: familyos.security
name: FamilyOS Security Plugin
version: 1.0.0
author: FamilyOS Project
description: Security capabilities for FamilyOS
module: familyos_cli.plugins.builtin.security.plugin
class: SecurityPlugin
enabled: true
```

when required for compatibility with the current Plugin Loader contract.

A future structured representation MAY be introduced through an explicit specification version.

A structured representation SHALL NOT silently replace the public manifest contract.

---

## SPEC-0009-R13 — Structured Representation

A future or alternate representation MAY group plugin metadata under a `plugin` object:

```yaml
plugin:
  id: familyos.security
  name: FamilyOS Security Plugin
  version: 1.0.0
  description: Security capabilities for FamilyOS
```

Such representation SHALL require loader support and explicit compatibility rules before becoming canonical.

Until then, the manifest shape consumed by the official runtime SHALL remain authoritative for implementation conformance.

---

# 9. Plugin Metadata

## SPEC-0009-R14 — Required Metadata

Every Plugin Manifest SHALL define the metadata required to identify and describe the plugin.

Required metadata SHALL include:

* identifier;
* name;
* version;
* description.

When required by the runtime contract, the manifest SHALL additionally define:

* author;
* module;
* implementation class.

Metadata SHALL comply with SPEC-0003.

---

## SPEC-0009-R15 — Display Name

The `name` field SHALL represent the plugin display name.

Example:

```yaml
name: FamilyOS Education Plugin
```

The display name SHALL NOT be interpreted as the canonical Plugin Identifier.

---

## SPEC-0009-R16 — Description

The `description` field SHALL provide a concise human-readable description of the plugin's primary responsibility.

Descriptions SHALL NOT be used as identity keys.

---

## SPEC-0009-R17 — Author

Where present, the `author` field SHALL identify the responsible author, organization, or maintainer.

For official plugins, the value SHOULD identify FamilyOS ownership consistently.

---

# 10. Plugin Version

## SPEC-0009-R18 — Exactly One Version

Every Plugin Manifest SHALL define exactly one plugin version.

---

## SPEC-0009-R19 — Version Contract

Plugin versions SHALL comply with SPEC-0004.

Version information SHALL remain separate from the Plugin Identifier.

Canonical:

```yaml
id: familyos.security
version: 1.0.0
```

The following SHALL NOT be used as the canonical identifier:

```text
familyos.security@1.0.0
```

The combined form MAY be used for presentation or resolution expressions where explicitly supported.

---

# 11. Runtime Loading Metadata

## SPEC-0009-R20 — Module

Where runtime loading requires dynamic Python import, the manifest SHALL define the importable module containing the plugin implementation.

Example:

```yaml
module: familyos_cli.plugins.builtin.security.plugin
```

The module name SHALL NOT define plugin identity.

---

## SPEC-0009-R21 — Plugin Class

Where runtime loading requires class resolution, the manifest SHALL define the plugin implementation class.

Example:

```yaml
class: SecurityPlugin
```

The implementation class SHALL comply with SPEC-0008.

The class name SHALL NOT define plugin identity.

---

## SPEC-0009-R22 — Enabled State

A manifest MAY define:

```yaml
enabled: true
```

when the runtime supports persisted default activation eligibility.

Absence of the field MAY default to:

```text
true
```

when defined by the runtime contract.

The enabled state SHALL NOT alter plugin identity.

---

# 12. Compatibility Declaration

## SPEC-0009-R23 — Platform Compatibility

A distributable Plugin Manifest SHOULD declare FamilyOS platform compatibility requirements.

Example:

```yaml
compatibility:
  familyos: ">=1.0.0"
```

Built-in plugins MAY rely on platform release coupling where an explicit packaging contract defines equivalent compatibility guarantees.

---

## SPEC-0009-R24 — Compatibility Validation

Platform compatibility SHALL be evaluated before plugin activation when compatibility metadata is present.

A plugin known to be incompatible with the active platform version SHALL NOT be activated.

---

# 13. Dependency Declaration

## SPEC-0009-R25 — Explicit Dependencies

A plugin SHALL explicitly declare required plugin dependencies when such dependencies exist.

A plugin SHALL NOT rely on undeclared plugin-to-plugin dependencies.

---

## SPEC-0009-R26 — Dependency Identifier

Dependency declarations SHALL reference dependencies using their canonical Plugin Identifier or another explicitly governed dependency identifier.

Example:

```yaml
dependencies:
  - id: familyos.security
    version: ">=1.0.0"
```

A dependency SHALL NOT be resolved solely by display name.

---

## SPEC-0009-R27 — Dependency Version Constraint

A dependency SHOULD define a version constraint when compatibility depends on dependency version.

Version constraints SHALL comply with SPEC-0004 or the approved plugin dependency contract.

---

## SPEC-0009-R28 — Dependency Namespace

Dependency identifiers SHALL preserve namespace ownership.

A plugin SHALL NOT rewrite or normalize another plugin's canonical identifier without an explicit compatibility mapping.

---

# 14. Capability Declaration

## SPEC-0009-R29 — Capability Declaration

A Plugin Manifest MAY declare capabilities provided by the plugin.

Declared capabilities SHALL comply with SPEC-0010.

---

## SPEC-0009-R30 — Capability Identifier

Capability declarations SHALL use canonical Capability Identifiers.

For official plugins, the preferred canonical form SHALL be:

```text
familyos.<plugin-name>.<capability>
```

Examples:

```text
familyos.health.record
familyos.finance.account
familyos.education.course
familyos.documents.archive
familyos.communication.messaging
```

---

## SPEC-0009-R31 — Capability Ownership

A plugin SHOULD expose capabilities under its own canonical Plugin Identifier prefix.

Example:

```text
Plugin:
familyos.education

Capabilities:
familyos.education.learner
familyos.education.course
familyos.education.record
```

Platform-level exceptions require explicit governance.

---

# 15. Contribution Declaration

## SPEC-0009-R32 — Contribution Declaration

A Plugin Manifest MAY declare contributions.

Contributions SHALL use official contribution contracts.

---

## SPEC-0009-R33 — Contribution Identity

Externally referenced contribution identifiers SHALL comply with SPEC-0002 and SPEC-0008.

A contribution identifier SHOULD preserve namespace ownership where applicable.

---

# 16. Manifest Validation

## SPEC-0009-R34 — Mandatory Validation

A Plugin Manifest SHALL be validated before the plugin becomes eligible for installation or activation.

---

## SPEC-0009-R35 — Structural Validation

Validation SHALL verify:

* manifest readability;
* supported YAML structure;
* required fields;
* field types;
* required runtime loading fields when applicable.

---

## SPEC-0009-R36 — Identifier Validation

Validation SHALL verify that the Plugin Identifier:

* follows the correct identifier category;
* uses valid lowercase dot-separated representation;
* contains an authorized namespace;
* does not contain version information;
* does not conflict with reserved namespace rules;
* is suitable for stable ecosystem identity.

---

## SPEC-0009-R37 — Metadata Validation

Validation SHALL verify required metadata completeness and conformance with SPEC-0003.

---

## SPEC-0009-R38 — Version Validation

Validation SHALL verify plugin version conformance with SPEC-0004.

---

## SPEC-0009-R39 — Dependency Validation

Validation SHALL verify:

* dependency declaration structure;
* dependency identifiers;
* version constraints;
* duplicate declarations;
* prohibited undeclared assumptions.

---

## SPEC-0009-R40 — Capability Validation

When capabilities are declared, validation SHALL verify capability identifier syntax and compatibility with SPEC-0010.

---

# 17. Runtime Contract Alignment

## SPEC-0009-R41 — Loader Identity Preservation

A Plugin Loader consuming a manifest SHALL preserve the canonical Plugin Identifier exactly.

For a manifest:

```yaml
id: familyos.security
```

the resulting runtime descriptor SHALL expose:

```text
familyos.security
```

as its canonical plugin identity.

The loader SHALL NOT silently shorten, rewrite, or re-namespace the identifier.

---

## SPEC-0009-R42 — Descriptor Mapping

Where the runtime uses `PluginDescriptor`, the manifest `id` field SHALL map to:

```text
PluginDescriptor.id
```

The descriptor identity SHALL therefore represent the canonical Plugin Identifier.

---

## SPEC-0009-R43 — Registry Key

Plugin registries SHALL use canonical Plugin Identifiers for plugin identity and lookup.

Example:

```text
familyos.security
```

rather than a display name such as:

```text
FamilyOS Security Plugin
```

---

## SPEC-0009-R44 — Duplicate Identity

Registration of two distinct plugin descriptors under the same canonical Plugin Identifier SHALL be rejected unless an explicitly version-aware registry contract defines otherwise.

---

# 18. Legacy Identifier Compatibility

## SPEC-0009-R45 — Legacy Plugin Identifiers

Existing plugin manifests that predate the canonical namespace convention MAY temporarily use legacy identifiers.

Examples may include:

```text
education
documents
communication
documentation
```

Such identifiers SHALL be classified explicitly as legacy-compatible rather than treated as new canonical examples.

---

## SPEC-0009-R46 — No Automatic Migration

Legacy Plugin Identifiers SHALL NOT be rewritten automatically merely to satisfy naming consistency.

Migration SHALL follow SPEC-0002 compatibility requirements.

---

## SPEC-0009-R47 — Canonical Target

Where a legacy official plugin identifier is migrated, the target SHALL follow:

```text
familyos.<plugin-name>
```

Examples:

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

This requirement defines the canonical target only.

It does not authorize immediate migration.

---

## SPEC-0009-R48 — Alias Strategy

A migration MAY temporarily support both:

```text
legacy identifier
canonical identifier
```

when required to preserve compatibility.

Alias behavior SHALL be explicit, testable, documented, and time-bounded where practical.

Aliases SHALL NOT create two independent plugin identities.

---

# 19. Security Considerations

Plugin Manifests SHALL NOT expose:

* credentials;
* authentication secrets;
* private cryptographic material;
* confidential personal information.

Plugin identifiers SHALL NOT falsely imply:

* FamilyOS ownership;
* official certification;
* endorsement;
* privileged platform status.

Manifest data SHALL be treated as untrusted input until validated.

Plugin manifests SHOULD be validated before:

* installation;
* dependency resolution;
* dynamic loading;
* activation.

---

# 20. Compatibility

Plugin Manifest evolution SHALL preserve compatibility where practical.

Changes to mandatory manifest fields SHALL require explicit specification versioning.

A manifest schema change SHALL define:

* compatibility expectations;
* migration requirements;
* loader behavior;
* deprecation requirements.

Stable Plugin Identifiers SHALL remain unchanged across compatible manifest revisions.

---

# 21. Conformance

A plugin package conforms to this specification when:

* exactly one authoritative `plugin.yaml` exists;
* the manifest is in the canonical location;
* required fields are present;
* the Plugin Identifier follows SPEC-0002 and SPEC-0008;
* namespace ownership is valid;
* display name and identifier are separate;
* plugin version is separate from identity;
* runtime loading metadata is valid where required;
* dependencies are explicit;
* declared capabilities are valid;
* compatibility rules are respected;
* the manifest passes required validation.

A legacy plugin MAY be classified as temporarily compatible when its identifier predates the canonical identifier convention and an approved migration policy exists.

---

# Annex A — Canonical Built-In Plugin Manifest

```yaml
id: familyos.security
name: FamilyOS Security Plugin
version: 1.0.0
author: FamilyOS Project
description: Security capabilities for FamilyOS
module: familyos_cli.plugins.builtin.security.plugin
class: SecurityPlugin
enabled: true
```

---

# Annex B — Canonical Education Plugin Target

```yaml
id: familyos.education
name: FamilyOS Education Plugin
version: 1.0.0
author: FamilyOS Project
description: Education capabilities for FamilyOS
module: familyos_cli.plugins.builtin.education.plugin
class: EducationPlugin
enabled: true
```

This annex defines the canonical identifier representation.

It does not authorize migration from an existing legacy identifier without compatibility analysis.

---

# Annex C — Documents and Documentation

The following represent distinct official plugins:

```text
Documents Plugin
→ familyos.documents
```

and:

```text
Documentation Plugin
→ familyos.documentation
```

Their names and identifiers SHALL NOT be treated as synonyms.

---

# Annex D — Capability Declaration

Example:

```yaml
capabilities:
  - id: familyos.education.course
    name: Education Course
    version: 1.0.0
    description: Provides education course capabilities
```

---

# Annex E — Dependency Declaration

Example:

```yaml
dependencies:
  - id: familyos.security
    version: ">=1.0.0"
```

---

# Annex F — Legacy Compatibility Example

Existing:

```yaml
id: education
```

Canonical target:

```yaml
id: familyos.education
```

Until a migration is approved, the existing identifier MAY remain active.

The canonical convention SHALL NOT be inferred as permission for an uncontrolled rename.

---

# 22. Normative References

* SPEC-0002 — Identifier;
* SPEC-0003 — Metadata;
* SPEC-0004 — Versioning;
* SPEC-0007 — File Format;
* SPEC-0008 — Naming Conventions;
* SPEC-0010 — Plugin Capability Contract;
* ADR-0007 — Official Plugin Architecture;
* `docs/04-reference/Naming-Conventions.md`;
* `docs/04-reference/Reserved-Words.md`;
* FamilyOS Specification Writing Guide.

---

# 23. Revision History

| Version | Status | Description                                                                                                                                                                                                                                                                                       |
| ------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0.0   | Draft  | Initial publication of the Plugin Manifest specification.                                                                                                                                                                                                                                         |
| 2.0.0   | Draft  | Aligns plugin manifests with the categorized identifier model, formalizes canonical `familyos.<plugin-name>` identifiers, maps manifest identity to `PluginDescriptor.id`, defines validation and runtime alignment requirements, and establishes explicit legacy identifier compatibility rules. |
