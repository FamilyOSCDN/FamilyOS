# SPEC-0007 — File Format

**Identifier:** SPEC-0007
**Title:** File Format
**Version:** 1.0.0
**Status:** Approved
**Owner:** FamilyOS Project
**Layer:** Specifications

---

# Abstract

This specification defines the normative requirements governing files within the FamilyOS platform.

It establishes common rules for file identity, encoding, extensions, reserved filenames, and structural properties to ensure consistency, interoperability, and long-term maintainability.

This specification applies to every persistent file managed by the FamilyOS platform unless explicitly exempted by another approved specification.

---

# 1. Purpose

The purpose of this specification is to establish a consistent file model for the FamilyOS platform.

A standardized file model enables:

- predictable project organization;
- automated validation;
- tooling interoperability;
- long-term maintainability;
- consistent generation.

---

# 2. Scope

This specification applies to all persistent files contained in a FamilyOS project.

It defines:

- file identity;
- filename requirements;
- filename extensions;
- character encoding;
- reserved filenames.

This specification does not define:

- document structure;
- directory hierarchy;
- naming conventions;
- file content.

---

# 3. Normative References

This specification depends on:

- SPEC-0002 — Identifier
- SPEC-0003 — Metadata
- SPEC-0004 — Versioning
- SPEC-0005 — Document Format
- SPEC-0006 — Directory Layout

---

# 4. Terms and Definitions

## File

A persistent filesystem object containing information.

## Filename

The complete name of a file, including its extension.

## Extension

The suffix identifying a file format.

## Reserved Filename

A filename reserved by the FamilyOS platform for a predefined purpose.

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

## SPEC-0007-R1 — File Identity

Every persistent file SHALL have exactly one filename.

---

## SPEC-0007-R2 — Filename Extension

Every filename SHALL include exactly one extension.

Hidden files defined by the operating system are exempt from this requirement.

---

## SPEC-0007-R3 — Character Encoding

Text files SHALL use UTF-8 encoding.

---

## SPEC-0007-R4 — Line Endings

Text files SHOULD use LF (`\n`) line endings.

Projects requiring another line-ending convention SHALL define it explicitly.

---

## SPEC-0007-R5 — Markdown Documents

Normative documentation SHALL use the `.md` filename extension.

---

## SPEC-0007-R6 — YAML Documents

YAML documents SHALL use one of the following filename extensions:

- `.yaml`
- `.yml`

A project SHOULD use a single YAML extension consistently.

---

## SPEC-0007-R7 — Reserved Filenames

Reserved filenames SHALL be used exclusively for the purposes defined by FamilyOS specifications.

Reserved filenames SHALL NOT be reused for unrelated resources.

---

## SPEC-0007-R8 — Filename Stability

A filename SHALL remain stable unless renamed through an approved maintenance activity.

---

## SPEC-0007-R9 — Duplicate Filenames

Two files within the same directory SHALL NOT have identical filenames.

---

## SPEC-0007-R10 — File Responsibility

Each file SHALL define exactly one primary responsibility.

A file SHALL NOT combine unrelated normative subjects.

---

## SPEC-0007-R11 — Extension Consistency

The filename extension SHALL accurately represent the file format.

---

## SPEC-0007-R12 — Future Extensions

Additional filename extensions MAY be introduced by future approved FamilyOS specifications.

---

# 7. Conformance

A project conforms to this specification if:

- all mandatory requirements defined by this specification are satisfied;
- filenames comply with the required extension rules;
- text files use the required character encoding;
- reserved filenames are used only for their defined purpose.

---
# 8. Security Considerations

Filenames SHALL NOT disclose:

- credentials;
- authentication secrets;
- private cryptographic material;
- confidential personal information.

Sensitive information SHALL be stored within file content only when explicitly permitted by the applicable FamilyOS specifications.

---

# 9. Compatibility

New FamilyOS projects MUST comply with this specification.

Existing projects SHOULD be updated during normal maintenance activities.

Breaking changes to this specification SHALL require a new major version.

---

# Annex A — Informative Examples

## A.1 Markdown Document

```text
README.md
```

---

## A.2 YAML Configuration

```text
familyos.yaml
```

---

## A.3 Python Source File

```text
plugin.py
```

---

## A.4 Reserved Filenames

```text
README.md
LICENSE
CHANGELOG.md
```

---

# 10. Normative References

- SPEC-0002 — Identifier
- SPEC-0003 — Metadata
- SPEC-0004 — Versioning
- SPEC-0005 — Document Format
- SPEC-0006 — Directory Layout

---

# 11. Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0.0 | Approved | Initial publication of the File Format specification. |

