# SPEC-0005 — Document Format

**Identifier:** SPEC-0005
**Title:** Document Format
**Version:** 1.0.0
**Status:** Approved
**Owner:** FamilyOS Project
**Layer:** Specifications

---

# Abstract

This specification defines the normative document format for all official FamilyOS documentation.

It establishes a consistent structure, formatting rules, and presentation requirements that ensure documentation remains readable, maintainable, implementation-independent, and suitable for automated processing.

This specification applies to every normative document published by the FamilyOS platform.

---

# 1. Purpose

The purpose of this specification is to establish a uniform document format across the FamilyOS platform.

A standardized document format enables:

- consistent documentation;
- predictable document organization;
- automated validation;
- improved maintainability;
- long-term stability.

---

# 2. Scope

This specification applies to all official FamilyOS documentation, including but not limited to:

- Foundation documents;
- Product documentation;
- Architecture documentation;
- Engineering documentation;
- Reference documentation;
- Specifications;
- ADRs;
- RFCs;
- Domain documentation.

This specification does not define the content of documents.

It defines only their required format and presentation.

---

# 3. Normative References

This specification depends on:

- SPEC-0001 — Documentation Structure
- SPEC-0002 — Identifier
- SPEC-0003 — Metadata
- SPEC-0004 — Versioning

---

# 4. Terms and Definitions

## Document

A persistent written resource published as part of the FamilyOS platform.

## Heading

A structural title introducing a document section.

## Section

A logical subdivision of a document.

## Informative Content

Content intended to improve understanding without creating normative obligations.

## Normative Content

Content defining mandatory, recommended, or optional technical requirements.

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

## SPEC-0005-R1 — Markdown Format

Official FamilyOS documents MUST be written in CommonMark-compatible Markdown.

---

## SPEC-0005-R2 — Character Encoding

Documents MUST be encoded using UTF-8.

---

## SPEC-0005-R3 — Top-Level Heading

Every document SHALL contain exactly one level-1 heading.

---

## SPEC-0005-R4 — Heading Hierarchy

Heading levels SHALL follow a continuous hierarchy.

A heading level SHALL NOT be skipped.

Example:

```text
# Title

## Section

### Subsection
```

---

## SPEC-0005-R5 — Document Metadata

Every normative document MUST include metadata as defined by SPEC-0003.

---

## SPEC-0005-R6 — Section Ordering

Normative documents SHALL preserve the section ordering defined by their governing specification.

Mandatory sections SHALL NOT be omitted.

---

## SPEC-0005-R7 — Normative Language

Normative statements SHALL use the keywords defined by the FamilyOS Specification Writing Guide.

Keywords SHALL appear in uppercase.

---

## SPEC-0005-R8 — Code Blocks

Source code, configuration examples and command-line examples SHALL be enclosed within fenced code blocks.

The language identifier SHALL be specified whenever supported by Markdown.

Examples:

````text
```python
```

```yaml
```

```bash
```
## SPEC-0005-R9 — Tables

Tabular information SHALL be represented using Markdown tables.

Examples of tabular information include:

- metadata;
- revision history;
- compatibility matrices;
- requirement summaries.

---

## SPEC-0005-R10 — Cross References

References to FamilyOS normative documents SHALL use permanent document identifiers.

Examples:

```text
SPEC-0002
ADR-0007
RFC-0010
```

---

## SPEC-0005-R11 — Visual Elements

Visual elements MAY be included to supplement a document.

Normative requirements SHALL be expressed as text.

Visual elements SHALL NOT introduce additional normative requirements.

---

## SPEC-0005-R12 — Document Independence

Normative requirements SHALL be fully specified within the document.

Normative requirements SHALL NOT depend on implementation source code for interpretation.

---

## SPEC-0005-R13 — Single Subject

A document SHALL define exactly one primary subject.

---

## SPEC-0005-R14 — Implementation Independence

A document SHALL remain implementation-independent.

---

## SPEC-0005-R15 — Terminology Consistency

A document SHALL use terminology defined by the FamilyOS Reference layer.

---

## SPEC-0005-R16 — Requirement Uniqueness

A document SHALL NOT redefine or duplicate normative requirements defined by another approved FamilyOS Specification.

Instead, the document SHALL reference the authoritative specification.

---

## SPEC-0005-R17 — Normative Separation

Normative content SHALL be clearly distinguishable from informative content.

---

# 7. Conformance

A document conforms to this specification if:

- all mandatory requirements defined by this specification are satisfied;
- document metadata complies with SPEC-0003;
- document structure complies with SPEC-0001;
- document format complies with this specification.
# 8. Security Considerations

Documents conforming to this specification SHALL NOT expose:

- credentials;
- authentication secrets;
- private cryptographic keys;
- confidential personal information.

Illustrative examples containing security-sensitive information SHALL use fictitious values.

---

# 9. Compatibility

New official FamilyOS documents MUST comply with this specification.

Existing documents SHOULD be updated during normal maintenance activities.

Breaking changes to this specification SHALL follow the FamilyOS specification lifecycle.

---

# Annex A — Informative Examples

## A.1 Document Title

```text
# SPEC-0005 — Document Format
```

---

## A.2 Heading Hierarchy

```text
# Title

## Section

### Subsection
```

---

## A.3 Markdown Table

| Identifier | Status | Version |
|------------|--------|---------|
| SPEC-0005 | Approved | 1.0.0 |

---

## A.4 Code Block

````text
```yaml
version: 1.0.0
```
# 10. Normative References

- SPEC-0001 — Documentation Structure
- SPEC-0002 — Identifier
- SPEC-0003 — Metadata
- SPEC-0004 — Versioning

---

# 11. Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0.0 | Approved | Initial publication of the Document Format specification. |

