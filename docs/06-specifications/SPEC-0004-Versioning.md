# SPEC-0004 — Versioning

**Identifier:** SPEC-0004
**Title:** Versioning
**Version:** 1.0.0
**Status:** Approved
**Owner:** FamilyOS Project
**Layer:** Specifications

---

# Abstract

This specification defines the normative versioning model used throughout the FamilyOS platform.

It establishes how versions are represented, interpreted, compared, and evolved for documentation, specifications, plugins, generated artifacts, domains, APIs, and other versioned resources.

All FamilyOS components exposing version information SHALL comply with this specification.

---

# 1. Purpose

The purpose of this specification is to establish a consistent versioning strategy across the FamilyOS platform.

A unified versioning model enables:

- compatibility management;
- lifecycle management;
- dependency resolution;
- release planning;
- predictable evolution.

---

# 2. Scope

This specification applies to versioned FamilyOS resources, including but not limited to:

- Specifications
- ADRs
- RFCs
- Plugins
- Plugin manifests
- Generation recipes
- Presets
- Templates
- Documentation
- APIs

This specification does not define source control versioning or Git workflows.

---

# 3. Normative References

- SPEC-0002 — Identifier
- SPEC-0003 — Metadata

---

# 4. Terms and Definitions

## Version

A structured identifier representing the evolution of a resource.

## Major Version

Indicates incompatible or breaking changes.

## Minor Version

Indicates backward-compatible functionality or content additions.

## Patch Version

Indicates corrections that do not modify the contract of the resource.

---

# 5. Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY and OPTIONAL are interpreted as defined by the FamilyOS Specification Writing Guide.

---

# 6. Requirements

## SPEC-0004-R1 — Version Format

Every version SHALL follow Semantic Versioning.

Required format:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
1.0.0
2.3.5
4.1.12
```

---

## SPEC-0004-R2 — Major Version

The major version MUST increase whenever a breaking change is introduced.

Breaking changes include:

- removal of mandatory requirements;
- incompatible interfaces;
- incompatible data formats;
- incompatible contracts.

---

## SPEC-0004-R3 — Minor Version

The minor version MUST increase when backward-compatible functionality or requirements are added.

Examples include:

- additional optional metadata;
- new capabilities;
- extended documentation.

---

## SPEC-0004-R4 — Patch Version

The patch version MUST increase when correcting errors that do not change the observable contract.

Examples include:

- spelling corrections;
- clarification of wording;
- editorial improvements.

---

## SPEC-0004-R5 — Version Stability

Published versions SHALL remain immutable.

A published version MUST NOT be modified.

Subsequent changes SHALL produce a new version.

---

## SPEC-0004-R6 — Independent Versioning

Each resource SHALL maintain its own version.

Versions SHALL NOT depend on the FamilyOS platform release number.

---

## SPEC-0004-R7 — Metadata Consistency

Version information SHALL be reflected in the resource metadata.

Metadata and revision history MUST remain consistent.

---

## SPEC-0004-R8 — Revision History

Every versioned resource MUST maintain a revision history documenting version evolution.

---

## SPEC-0004-R9 — Comparison

Version comparison SHALL follow the ordering:

- Major
- Minor
- Patch

Example:

```text
1.0.0 < 1.1.0 < 1.1.1 < 2.0.0
```

---

# 7. Constraints

Version numbers SHALL:

- be numeric;
- follow Semantic Versioning;
- remain stable after publication;
- accurately reflect compatibility.

Pre-release identifiers MAY be defined by future specifications.

---

# 8. Conformance

This specification applies to:

- documentation;
- specifications;
- plugins;
- manifests;
- APIs;
- generation resources.

A component conforms if its versioning strategy satisfies every mandatory requirement defined by this specification.

---

# 9. Security Considerations

Version numbers SHALL NOT be used to encode confidential or security-sensitive information.

Version identifiers are intended solely for resource evolution and compatibility management.

---

# 10. Compatibility

Backward-compatible changes SHOULD preserve the major version.

Breaking changes SHALL require a new major version.

Deprecated resources SHOULD remain available for an appropriate transition period whenever practical.

---

# 11. Examples

Specification:

```text
Version: 1.0.0
```

Plugin:

```text
Version: 2.4.1
```

API:

```text
Version: 3.0.0
```

---

# 12. References

- SPEC-0002 — Identifier
- SPEC-0003 — Metadata

---

# 13. Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0.0 | Approved | Initial publication of the Versioning specification. |

