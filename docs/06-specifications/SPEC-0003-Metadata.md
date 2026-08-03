# SPEC-0003 — Metadata

**Identifier:** SPEC-0003
**Title:** Metadata
**Version:** 1.0.0
**Status:** Approved
**Owner:** FamilyOS Project
**Layer:** Specifications

---

# Abstract

This specification defines the normative metadata model used throughout the FamilyOS platform.

Metadata provides consistent descriptive information for documents, specifications, plugins, generated artifacts, domains, templates, and other platform resources.

Every FamilyOS component exposing metadata SHALL comply with this specification.

---

# 1. Purpose

The purpose of this specification is to establish a common metadata model for the FamilyOS platform.

A unified metadata model enables:

- discoverability;
- traceability;
- interoperability;
- version management;
- lifecycle management;
- documentation consistency.

---

# 2. Scope

This specification applies to metadata associated with persistent FamilyOS resources, including but not limited to:

- Specifications
- ADRs
- RFCs
- Documentation
- Plugins
- Plugin manifests
- Domains
- Generation artifacts
- Recipes
- Presets
- Templates

This specification does not define runtime telemetry or transient execution metadata.

---

# 3. Normative References

- SPEC-0001 — Documentation Structure
- SPEC-0002 — Identifier

---

# 4. Terms and Definitions

## Metadata

Structured information describing a resource.

## Resource

Any persistent entity managed by the FamilyOS platform.

## Metadata Field

A named attribute describing a resource.

---

# 5. Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY and OPTIONAL are interpreted as defined by the FamilyOS Specification Writing Guide.

---

# 6. Requirements

## SPEC-0003-R1 — Metadata Presence

Every persistent FamilyOS resource MUST expose metadata.

---

## SPEC-0003-R2 — Mandatory Fields

Every metadata definition MUST contain the following fields:

- Identifier
- Title
- Version
- Status

---

## SPEC-0003-R3 — Identifier

The Identifier field SHALL comply with SPEC-0002.

---

## SPEC-0003-R4 — Title

The Title field MUST provide a concise human-readable name.

Titles SHOULD remain stable.

---

## SPEC-0003-R5 — Version

The Version field MUST indicate the current version of the resource.

Version format SHALL comply with SPEC-0004.

---

## SPEC-0003-R6 — Status

The Status field MUST indicate the lifecycle state of the resource.

Typical values include:

- Draft
- Review
- Approved
- Implemented
- Deprecated
- Superseded

Individual specifications MAY define additional status values.

---

## SPEC-0003-R7 — Optional Fields

Resources MAY define additional metadata fields when justified.

Examples include:

- Owner
- Layer
- Category
- Created
- Updated
- Tags
- Authors

Optional fields SHALL NOT redefine mandatory fields.

---

## SPEC-0003-R8 — Consistency

Metadata SHALL accurately describe the associated resource.

Metadata MUST be updated whenever the resource changes.

---

## SPEC-0003-R9 — Stability

Metadata field names SHOULD remain stable across platform versions.

Renaming existing metadata fields SHOULD be avoided.

---

# 7. Constraints

Metadata SHALL:

- be implementation-independent;
- avoid duplication;
- use consistent terminology;
- remain machine-readable;
- remain human-readable.

Metadata SHALL NOT include implementation-specific details unless explicitly required by another specification.

---

# 8. Conformance

The following components are subject to this specification:

- documentation;
- CLI;
- plugin SDK;
- generation framework;
- official plugins;
- future platform services.

A component conforms if every mandatory metadata field satisfies this specification.

---

# 9. Security Considerations

Metadata SHALL NOT contain:

- passwords;
- secrets;
- credentials;
- private cryptographic material;
- confidential personal information.

Sensitive information SHALL be stored separately from metadata.

---

# 10. Compatibility

New metadata fields MAY be introduced in backward-compatible revisions.

Mandatory metadata fields SHALL NOT be removed without an approved replacement specification.

---

# 11. Examples

Example document metadata:

```text
Identifier: SPEC-0003
Title: Metadata
Version: 1.0.0
Status: Approved
Owner: FamilyOS Project
Layer: Specifications
```

Example plugin metadata:

```text
Identifier: PLUGIN-0004
Title: Security Plugin
Version: 1.2.0
Status: Approved
```

---

# 12. References

- SPEC-0001 — Documentation Structure
- SPEC-0002 — Identifier
- SPEC-0004 — Versioning

---

# 13. Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0.0 | Approved | Initial publication of the Metadata specification. |

