# SPEC-0006 — Directory Layout

**Identifier:** SPEC-0006
**Title:** Directory Layout
**Version:** 1.0.0
**Status:** Approved
**Owner:** FamilyOS Project
**Layer:** Specifications

---

# Abstract

This specification defines the normative directory layout for FamilyOS projects.

It establishes the required directory hierarchy, reserved directory names, and structural rules that enable consistent project organization, automated validation, tooling interoperability, and long-term maintainability.

This specification applies to every FamilyOS project unless explicitly exempted by another approved specification.

---

# 1. Purpose

The purpose of this specification is to define a consistent directory layout for the FamilyOS platform.

A standardized directory structure enables:

- predictable project organization;
- automated validation;
- tooling interoperability;
- simplified navigation;
- long-term maintainability.

---

# 2. Scope

This specification applies to the directory hierarchy of every FamilyOS project.

It defines:

- required top-level directories;
- reserved directory names;
- directory hierarchy requirements;
- structural conformance rules.

This specification does not define:

- file naming conventions;
- file formats;
- document content;
- source code organization inside individual modules.

---

# 3. Normative References

This specification depends on:

- SPEC-0001 — Documentation Structure
- SPEC-0002 — Identifier
- SPEC-0003 — Metadata
- SPEC-0004 — Versioning
- SPEC-0005 — Document Format

---

# 4. Terms and Definitions

## Directory

A filesystem container used to organize FamilyOS resources.

## Project Root

The top-level directory containing a FamilyOS project.

## Reserved Directory

A directory name reserved by the FamilyOS platform for a predefined purpose.

## Directory Hierarchy

The parent-child relationships between directories defined by this specification.

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

## SPEC-0006-R1 — Project Root

A FamilyOS project SHALL have exactly one project root directory.

---

## SPEC-0006-R2 — Required Top-Level Directories

The project root SHALL contain the following top-level directories:

- docs/
- src/
- tests/

Additional top-level directories MAY be defined by other approved specifications.

---

## SPEC-0006-R3 — Reserved Directory Names

Reserved directory names SHALL be used exclusively for the purposes defined by FamilyOS specifications.

Reserved directory names SHALL NOT be reused for unrelated content.

---

## SPEC-0006-R4 — Documentation Directory

The `docs/` directory SHALL contain the official FamilyOS documentation.

Documentation outside the `docs/` directory SHALL NOT be considered normative unless explicitly permitted by another specification.

---

## SPEC-0006-R5 — Source Directory

The `src/` directory SHALL contain the implementation source code.

---

## SPEC-0006-R6 — Test Directory

The `tests/` directory SHALL contain automated verification artifacts.

---

## SPEC-0006-R7 — Hierarchical Organization

Directories SHALL be organized hierarchically.

A child directory SHALL have exactly one parent directory.

---

## SPEC-0006-R8 — Directory Purpose

Each directory SHALL define exactly one primary responsibility.

A directory SHALL NOT mix unrelated responsibilities.

---

## SPEC-0006-R9 — Empty Directories

Directories MAY be empty during project initialization.

The presence of an empty directory SHALL NOT invalidate the project structure.

---

## SPEC-0006-R10 — Reserved Hierarchy

Directories defined by approved FamilyOS specifications SHALL preserve their specified hierarchy.

---

## SPEC-0006-R11 — Extension

Additional directories MAY be introduced provided they do not violate this specification or another approved specification.

---

## SPEC-0006-R12 — Naming Compliance

Directory names SHALL comply with the applicable FamilyOS naming specification.

---

# 7. Conformance

A project conforms to this specification if:

- all mandatory requirements defined by this specification are satisfied;
- required top-level directories are present;
- reserved directory names are respected;
- the directory hierarchy complies with this specification.

---
# 8. Security Considerations

Directory names SHALL NOT disclose:

- credentials;
- authentication secrets;
- private cryptographic material;
- confidential personal information.

Security-sensitive resources SHOULD be organized according to the applicable FamilyOS security specifications.

---

# 9. Compatibility

New FamilyOS projects MUST comply with this specification.

Existing projects SHOULD migrate to this directory layout during normal maintenance activities.

Changes introducing incompatible directory layouts SHALL require a new major version of this specification.

---

# Annex A — Informative Examples

## A.1 Typical FamilyOS Project Layout

```text
project-root/
├── docs/
├── src/
└── tests/
```

---

## A.2 Documentation Layout

```text
docs/
├── 00-foundation/
├── 01-product/
├── 02-architecture/
├── 03-engineering/
├── 04-reference/
├── 05-knowledge/
├── 06-specifications/
├── adr/
└── rfc/
```

---

## A.3 Source Layout

```text
src/
└── familyos_cli/
```

---

# 10. Normative References

- SPEC-0001 — Documentation Structure
- SPEC-0002 — Identifier
- SPEC-0003 — Metadata
- SPEC-0004 — Versioning
- SPEC-0005 — Document Format

---

# 11. Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0.0 | Approved | Initial publication of the Directory Layout specification. |

