# References

## Purpose

This document defines the normative and informative references supporting ADR-0012.

These references provide the architectural, engineering, and documentation context necessary to understand and apply the documentation architecture adopted by the FamilyOS project.

Normative references are considered authoritative for the interpretation of this Architectural Decision Record.

---

# Reference Philosophy

The FamilyOS documentation architecture is based on traceability rather than duplication.

Every document SHOULD reference the authoritative source instead of reproducing normative content.

Stable document identifiers SHALL be used whenever practical to preserve long-term maintainability.

---

# Normative References

## Foundation

The following Foundation documents establish the principles implemented by this ADR.

| Identifier | Title               | Purpose                                                                                                           |
| ---------- | ------------------- | ----------------------------------------------------------------------------------------------------------------- |
| FND-000    | FamilyOS Foundation | Establishes the vision, mission, engineering philosophy, governance, and documentation principles of the project. |

---

## Architecture

The following document families define the architectural documentation model.

| Identifier  | Title                          | Purpose                                                                          |
| ----------- | ------------------------------ | -------------------------------------------------------------------------------- |
| ADR Series  | Architectural Decision Records | Record significant architectural decisions.                                      |
| RFC Series  | Request for Comments           | Define technical designs and architecture proposals.                             |
| SPEC Series | Specifications                 | Define normative implementation requirements.                                    |
| ENG Series  | Engineering Documents          | Define engineering governance, engineering standards, and engineering processes. |

---

## Reference Documentation

The following supporting documentation complements the normative document families.

| Category     | Purpose                                                               |
| ------------ | --------------------------------------------------------------------- |
| Reference    | Shared terminology, conventions, identifiers, and reference material. |
| Guides       | Practical engineering guidance.                                       |
| Tutorials    | Learning-oriented documentation.                                      |
| Contributing | Contributor workflow and collaboration guidance.                      |

---

# External References

The engineering philosophy adopted by FamilyOS has been influenced by widely recognized software engineering practices.

The following publications provide useful background information.

## Software Architecture

* Robert C. Martin — *Clean Architecture*
* Eric Evans — *Domain-Driven Design*
* Vaughn Vernon — *Implementing Domain-Driven Design*

---

## Documentation

* RFC 2119 — *Key words for use in RFCs to Indicate Requirement Levels*
* Diátaxis Documentation Framework
* Docs as Code methodology

---

## Software Engineering

* Semantic Versioning (SemVer)
* Conventional Commits
* Twelve-Factor App methodology

These references provide context but do not override FamilyOS governance.

---

# Cross-Reference Policy

Documentation SHALL reference stable identifiers whenever available.

Examples include:

* FND-000
* ADR-0012
* RFC-0015
* SPEC-0006
* ENG-003

References SHOULD always point to the authoritative document.

Normative requirements SHALL NOT be duplicated across multiple document families.

---

# Reference Integrity

Project maintainers SHOULD periodically verify that:

* referenced documents remain available;
* identifiers remain stable;
* obsolete references are updated;
* broken cross-references are corrected.

Reference integrity is considered part of documentation quality.

---

# Documentation Hierarchy

The documentation architecture established by ADR-0012 is summarized below.

```text id="e9j5vh"
Foundation
      ↓
Architecture
   ├── ADR
   ├── RFC
   └── SPEC
      ↓
Engineering
      └── ENG
      ↓
Implementation
      ↓
Testing
      ↓
Release
```

Each layer builds upon the previous one while maintaining distinct responsibilities.

---

# Relationship to ADR-0012

The references defined in this document support the architectural decision recorded in ADR-0012.

Together with the FamilyOS Foundation and the remaining document families, they establish a coherent engineering knowledge system that preserves architectural intent, engineering standards, implementation requirements, and long-term project knowledge.
