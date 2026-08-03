# SPEC-0009 — Plugin Manifest

**Identifier:** SPEC-0009  
**Title:** Plugin Manifest  
**Version:** 1.0.0  
**Status:** Draft  
**Owner:** FamilyOS Project  
**Layer:** Specifications  

---

# Abstract

This specification defines the normative requirements for the FamilyOS Plugin Manifest.

The Plugin Manifest is the authoritative description of a plugin package and provides the information required by the FamilyOS Plugin Ecosystem to identify, verify, resolve, and manage plugins.

This specification defines:

- manifest identity;
- required metadata;
- compatibility information;
- dependency declaration;
- extension declarations.

This specification does not define plugin behavior, lifecycle implementation, capability contracts, or contribution contracts.

---

# 1. Purpose

The purpose of this specification is to define a stable and machine-readable contract for plugin manifests.

A standardized Plugin Manifest enables:

- plugin discovery;
- dependency resolution;
- compatibility verification;
- runtime preparation;
- automated validation.

---

# 2. Scope

This specification applies to every FamilyOS plugin package.

It defines:

- manifest existence;
- manifest location;
- manifest structure;
- required fields;
- metadata requirements;
- dependency declarations.

This specification does not define:

- plugin execution behavior;
- plugin lifecycle transitions;
- capability implementation;
- contribution implementation.

---

# 3. Normative References

This specification depends on:

- SPEC-0002 — Identifier
- SPEC-0003 — Metadata
- SPEC-0004 — Versioning
- SPEC-0007 — File Format
- SPEC-0008 — Naming Conventions

Related architecture decisions:

- ADR-0007 — Official Plugin Architecture

---

# 4. Terms and Definitions

## Plugin

An extension package that integrates with FamilyOS through official plugin contracts.

---

## Plugin Manifest

A machine-readable document describing a plugin package.

---

## Plugin Identifier

A unique identifier assigned to a plugin.

---

## Plugin Dependency

A declared requirement on another plugin or platform component.

---

## Plugin Package

A distributable unit containing a plugin implementation and its associated resources.

---

# 5. Normative Language

The keywords:

- MUST
- MUST NOT
- REQUIRED
- SHALL
- SHALL NOT
- SHOULD
- SHOULD NOT
- RECOMMENDED
- MAY
- OPTIONAL

are interpreted as defined by the FamilyOS Specification Writing Guide.

---
# 6. Requirements

## SPEC-0009-R1 — Manifest Existence

Every FamilyOS plugin package SHALL provide exactly one Plugin Manifest.

---

## SPEC-0009-R2 — Manifest Format

The Plugin Manifest SHALL use a machine-readable format.

The default manifest format SHALL be YAML.

The manifest filename SHALL be:

```text
plugin.yaml
```

---

## SPEC-0009-R3 — Manifest Location

The Plugin Manifest SHALL be located at the root directory of the plugin package.

Example:

```text
plugin-package/
├── plugin.yaml
├── src/
└── resources/
```

---

## SPEC-0009-R4 — Plugin Identifier

Every Plugin Manifest SHALL define exactly one plugin identifier.

The plugin identifier SHALL comply with:

- SPEC-0002 — Identifier;
- SPEC-0008 — Naming Conventions.

The plugin identifier SHALL uniquely identify the plugin within the FamilyOS ecosystem.

---

## SPEC-0009-R5 — Plugin Metadata

The Plugin Manifest SHALL define plugin metadata.

Required metadata SHALL include:

- identifier;
- name;
- version;
- description.

Metadata SHALL comply with SPEC-0003.

---

## SPEC-0009-R6 — Plugin Version

Every Plugin Manifest SHALL define exactly one plugin version.

Plugin versions SHALL comply with SPEC-0004.

---

## SPEC-0009-R7 — Compatibility Declaration

The Plugin Manifest SHALL declare FamilyOS compatibility requirements.

Compatibility declarations SHALL include the required FamilyOS platform version range.

---

## SPEC-0009-R8 — Dependency Declaration

Plugin dependencies SHALL be explicitly declared.

A plugin SHALL NOT rely on undeclared plugin dependencies.

---

## SPEC-0009-R9 — Dependency Version Constraints

Declared dependencies SHALL include version constraints when compatibility requirements exist.

---

## SPEC-0009-R10 — Capability Declaration

A Plugin Manifest MAY declare provided capabilities.

Declared capabilities SHALL comply with the Plugin Capability Contract.

---

## SPEC-0009-R11 — Contribution Declaration

A Plugin Manifest MAY declare provided contributions.

Declared contributions SHALL comply with the Plugin Contribution Contract.

---

## SPEC-0009-R12 — Manifest Validation

A Plugin Manifest SHALL be validated before plugin installation or activation.

Validation SHALL verify:

- required fields;
- identifier format;
- version format;
- dependency declarations;
- compatibility requirements.

---

# 7. Conformance

A plugin package conforms to this specification if:

- exactly one Plugin Manifest exists;
- the manifest location is correct;
- required metadata is present;
- identifiers and versions are valid;
- dependencies are explicitly declared;
- compatibility requirements are defined.

---
# 8. Security Considerations

Plugin Manifests SHALL NOT expose:

- credentials;
- authentication secrets;
- private cryptographic material;
- confidential personal information.

Plugin metadata SHOULD contain only information required for plugin identification, compatibility, and management.

Plugin manifests SHALL be validated before plugin installation.

---

# 9. Compatibility

Plugin Manifests MUST remain compatible with the FamilyOS Plugin Ecosystem.

Changes to mandatory manifest fields SHALL require a new specification version.

Plugins targeting incompatible FamilyOS versions SHALL NOT be activated.

---

# Annex A — Informative Examples

## A.1 Basic Plugin Manifest

```yaml
plugin:
  id: familyos.security
  name: FamilyOS Security Plugin
  version: 1.0.0
  description: Security capabilities for FamilyOS

compatibility:
  familyos: ">=1.0.0"

dependencies:
  - id: familyos.core
    version: ">=1.0.0"

capabilities:
  - security.policy
  - security.validation

contributions:
  - validation.rules
  - templates
```

---

## A.2 Plugin Package Layout

```text
familyos-security-plugin/

├── plugin.yaml

├── src/

│   └── security_plugin/

└── resources/
```

---

# 10. Normative References

- SPEC-0002 — Identifier
- SPEC-0003 — Metadata
- SPEC-0004 — Versioning
- SPEC-0007 — File Format
- SPEC-0008 — Naming Conventions

---

# 11. Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0.0 | Draft | Initial publication of the Plugin Manifest specification. |

