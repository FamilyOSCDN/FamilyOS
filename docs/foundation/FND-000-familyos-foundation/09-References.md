# References

## Purpose

This document identifies the normative and informative references that support the FamilyOS Foundation.

Normative references define documents that SHALL be considered authoritative when applying the principles established by the Foundation.

Informative references provide additional context and background but do not introduce mandatory requirements.

---

# Reference Philosophy

The FamilyOS documentation system is organized as a coherent and traceable body of knowledge.

Each document family has a clearly defined responsibility and contributes to the overall governance of the platform.

References SHOULD always point to the authoritative source of information.

Normative requirements SHALL NOT be duplicated across multiple documents.

---

# Normative References

The following documents are normative for the FamilyOS Foundation.

## Project Governance

| Identifier   | Title              | Purpose                                                                                          |
| ------------ | ------------------ | ------------------------------------------------------------------------------------------------ |
| GOVERNANCE   | Project Governance | Defines project governance, contribution workflow, review process, and documentation governance. |
| README       | Project Overview   | Introduces the FamilyOS platform and repository.                                                 |
| CONTRIBUTING | Contribution Guide | Defines contribution expectations and development workflow.                                      |

---

## Architecture

| Identifier  | Title                          | Purpose                                                              |
| ----------- | ------------------------------ | -------------------------------------------------------------------- |
| ADR Series  | Architectural Decision Records | Record significant architectural decisions.                          |
| RFC Series  | Request for Comments           | Define technical designs and architecture proposals.                 |
| SPEC Series | Specifications                 | Define normative implementation requirements.                        |
| ENG Series  | Engineering Documents          | Define engineering standards, governance, and engineering processes. |

---

## Reference Documentation

| Identifier | Title                   | Purpose                                                                        |
| ---------- | ----------------------- | ------------------------------------------------------------------------------ |
| Reference  | Reference Documentation | Defines terminology, conventions, naming rules, and shared reference material. |
| Guides     | Engineering Guides      | Provide practical guidance for contributors.                                   |
| Tutorials  | Tutorials               | Support onboarding and learning.                                               |

---

# Engineering Standards

The Foundation assumes that all engineering documentation conforms to the official engineering standards established by the ENG document series.

These standards include, but are not limited to:

* engineering governance;
* documentation standards;
* testing standards;
* quality standards;
* build standards;
* release standards.

---

# External References

The following publications influence the engineering philosophy of FamilyOS.

## Software Architecture

* Clean Architecture — Robert C. Martin
* Domain-Driven Design — Eric Evans
* Implementing Domain-Driven Design — Vaughn Vernon

---

## Documentation

* Docs as Code
* Diátaxis Documentation Framework
* RFC 2119 — Key words for use in RFCs

---

## Software Engineering

* Twelve-Factor App
* Semantic Versioning (SemVer)
* Conventional Commits

These publications provide background information and SHOULD be interpreted in a manner consistent with the FamilyOS Foundation.

---

# Reference Hierarchy

The documentation hierarchy is organized as follows:

```text
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

Each layer refines the previous one without replacing it.

---

# Cross-Reference Policy

All permanent references SHOULD use stable document identifiers.

Examples include:

* ADR-0008
* RFC-0015
* SPEC-0006
* ENG-003

Cross-references SHALL remain valid across document revisions whenever practical.

Broken references SHOULD be corrected as part of normal documentation maintenance.

---

# Maintaining References

Reference integrity is part of documentation quality.

Project maintainers SHOULD periodically verify that:

* referenced documents still exist;
* identifiers remain stable;
* obsolete references are updated;
* normative references remain authoritative.

Reference maintenance contributes directly to long-term knowledge preservation.

---

# Relationship to the Foundation

This document concludes the reference model of the FamilyOS Foundation.

The Foundation establishes the principles that guide the project.

The referenced document families translate those principles into architectural decisions, technical designs, engineering standards, implementation requirements, and practical guidance.

Together they form the official knowledge system of the FamilyOS platform.
