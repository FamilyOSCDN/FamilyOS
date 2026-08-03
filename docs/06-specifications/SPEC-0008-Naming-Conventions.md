# SPEC-0008 — Naming Conventions

**Identifier:** SPEC-0008
**Title:** Naming Conventions
**Version:** 1.0.0
**Status:** Approved
**Owner:** FamilyOS Project
**Layer:** Specifications

---

# Abstract

This specification defines the normative naming conventions used throughout the FamilyOS platform.

It establishes consistent naming rules for directories, files, documents, specifications, plugins, domains, source code artifacts, and other persistent resources.

Consistent naming enables predictable project organization, interoperability, automated validation, and long-term maintainability.

---

# 1. Purpose

The purpose of this specification is to establish a uniform naming model across the FamilyOS platform.

Consistent naming enables:

- predictable resource identification;
- improved readability;
- automated validation;
- interoperability;
- long-term stability.

---

# 2. Scope

This specification applies to the names of persistent FamilyOS resources, including but not limited to:

- directories;
- files;
- documents;
- specifications;
- ADRs;
- RFCs;
- plugins;
- domains;
- templates;
- generated artifacts.

This specification does not define identifiers, metadata, or version numbers.

---

# 3. Normative References

This specification depends on:

- SPEC-0002 — Identifier
- SPEC-0005 — Document Format
- SPEC-0006 — Directory Layout
- SPEC-0007 — File Format

---

# 4. Terms and Definitions

## Name

A human-readable designation assigned to a resource.

## Filename

The complete name of a file, including its extension.

## Directory Name

The name assigned to a directory.

## Resource Name

The name assigned to any persistent FamilyOS resource.

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
# 8. Security Considerations

Resource names SHALL NOT disclose:

- credentials;
- authentication secrets;
- private cryptographic material;
- confidential personal information.

Sensitive information SHALL NOT be encoded in resource names.

---

# 9. Compatibility

New FamilyOS resources MUST comply with this specification.

Existing resources SHOULD be renamed during normal maintenance activities where practical.

Breaking changes to naming rules SHALL require a new major version of this specification.

---

# Annex A — Informative Examples

## A.1 Specification

```text
SPEC-0008-Naming-Conventions.md
```

---

## A.2 Architecture Decision Record

```text
ADR-0007-Plugin-Architecture.md
```

---

## A.3 Request for Comments

```text
RFC-0010-Official-Security-Plugin.md
```

---

## A.4 Documentation Directory

```text
docs/
├── 00-foundation/
├── 02-architecture/
├── 04-reference/
└── 06-specifications/
```

---

## A.5 Source Code

```text
src/
└── familyos_cli/
```

---

# 10. Normative References

- SPEC-0002 — Identifier
- SPEC-0005 — Document Format
- SPEC-0006 — Directory Layout
- SPEC-0007 — File Format

---

# 11. Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0.0 | Approved | Initial publication of the Naming Conventions specification. |

