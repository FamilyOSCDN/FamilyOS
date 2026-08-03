# FamilyOS reference index

**Version:** 1.0
**Status:** Stable
**Last Updated:** August 2026

---

# Purpose

This document provides the official entry point to the FamilyOS reference documentation.

Its purpose is to:

- identify the authoritative reference documents
- explain the responsibility of each reference document
- guide contributors toward the correct source of information
- reduce duplication across the documentation
- maintain a single source of truth for platform terminology and documentation standards

This document is normative.

---

# Scope

This index applies to:

- contributors
- maintainers
- architects
- plugin developers
- documentation authors
- reviewers
- platform governance

It references the official documentation maintained by the FamilyOS project.

---

# Normative language

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** express normative requirements.

Their interpretation follows:

`docs/04-reference/Language.md`

---

# How to use this index

Every official FamilyOS document belongs to a defined documentation category.

Before creating a new document, contributors SHOULD identify the appropriate category through this index.

Documentation MUST NOT duplicate responsibilities already assigned to another document.

When multiple documents appear relevant, the document with the narrowest and most specific responsibility takes precedence.

---

# Reference documents

The official reference documentation consists of the following documents.

| Document | Responsibility |
|---|---|
| README.md | Introduction to the Reference documentation |
| Language.md | Normative writing language |
| Glossary.md | Official terminology |
| Acronyms.md | Approved abbreviations and acronyms |
| Naming-Conventions.md | Naming rules for all platform artifacts |
| Reserved-Words.md | Reserved identifiers and namespaces |
| Reference-Index.md | Navigation and responsibility index |

---

# Navigation matrix

| I want to... | Read |
|---|---|
| Understand FamilyOS terminology | Glossary.md |
| Learn the documentation language | Language.md |
| Verify an acronym | Acronyms.md |
| Check naming rules | Naming-Conventions.md |
| Verify reserved identifiers | Reserved-Words.md |
| Start with the reference documentation | README.md |
| Find the correct reference document | Reference-Index.md |

---

# Foundation documents

The Foundation documentation defines the principles that govern the entire platform.

Primary location:

`docs/00-foundation/`

Typical documents include:

- Manifesto
- Architecture Principles
- Engineering Principles
- Documentation Standards
- Governance
- Git Strategy

Reference documents build upon these principles but do not redefine them.

---

# Architecture documentation

Architecture documentation describes how the platform is organized.

Primary location:

`docs/02-architecture/`

Architecture documents define:

- architectural layers
- component responsibilities
- interactions
- structural decisions

Reference documents support architecture by defining common terminology and conventions.

---

# Specifications

Specifications define normative technical contracts.

Primary location:

`docs/06-specifications/`

Specifications describe:

- required behavior
- interfaces
- formats
- schemas
- compatibility rules

Reference documentation provides the language and terminology used by specifications.

---

# Architecture Decision Records

Architecture Decision Records document significant architectural decisions.

Primary location:

`docs/adr/`

Each ADR records:

- context
- decision
- rationale
- consequences

Reference documents define terminology but do not replace ADRs.

---

# Requests for Comments

Requests for Comments describe architectural proposals before adoption.

Primary location:

`docs/rfcs/`

RFCs may introduce:

- new capabilities
- new architectural patterns
- platform evolution
- governance changes

Approved RFCs may result in new ADRs or updated reference documentation.

---

# Official domains

Business domains are documented under:

`docs/30-domains/`

Each domain defines its own:

- vision
- responsibilities
- business rules
- model
- APIs
- events
- commands

Reference documentation provides the common language shared across all domains.

---

# Official plugins

Official plugins extend the FamilyOS platform while respecting the architectural contracts established by the reference documentation.

Official plugin documentation defines:

- capabilities
- extension points
- configuration
- interoperability
- lifecycle
- security requirements

Reference documentation establishes the common terminology used by every official plugin.

---

# Engineering

Engineering documentation describes implementation practices used throughout the platform.

Primary location:

`docs/03-engineering/`

Typical engineering documentation includes:

- coding standards
- testing practices
- development workflow
- release process
- tooling
- quality assurance

Reference documentation defines vocabulary but does not replace engineering guidance.

---

# Development workflow

The recommended documentation workflow is:

1. Define architectural principles.
2. Define reference terminology.
3. Write specifications.
4. Approve architectural decisions.
5. Implement functionality.
6. Validate documentation.
7. Publish changes.

Documentation SHOULD evolve together with the platform.

---

# Documentation standards

Documentation standards are defined in:

`docs/00-foundation/standards/Documentation-Standards.md`

Reference documentation complements these standards by defining:

- terminology
- language
- naming
- reserved words
- document responsibilities

---

# Repository structure

The documentation repository is organized into dedicated sections.

Typical top-level documentation includes:

```text
docs/
├── 00-foundation
├── 01-product
├── 02-architecture
├── 03-engineering
├── 04-reference
├── 05-knowledge
├── 06-specifications
├── 07-business
├── 10-architecture
├── 20-core
├── 30-domains
├── adr
└── rfcs
```


Each directory has a clearly defined responsibility.

Reference documents MUST NOT duplicate content owned by another documentation category.

---

# Cross references

Reference documents are intentionally interconnected.

Typical relationships include:

| Document | References |
|---|---|
| README.md | All reference documents |
| Language.md | Glossary, Acronyms |
| Glossary.md | Naming-Conventions, Specifications |
| Acronyms.md | Language |
| Naming-Conventions.md | Reserved-Words, Glossary |
| Reserved-Words.md | Naming-Conventions |
| Reference-Index.md | Entire reference documentation |

Cross references SHOULD be maintained whenever responsibilities evolve.

---

# Document ownership

Each reference document has one primary responsibility.

A document MUST NOT redefine responsibilities assigned to another document.

When a new concept is introduced:

1. determine the responsible document;
2. update that document;
3. reference it from related documents when appropriate;
4. avoid duplicating the definition elsewhere.

This approach preserves the Single Source of Truth principle.

---

# Maintenance

This index evolves together with the FamilyOS documentation.

New reference documents MAY be added when a new permanent documentation responsibility is introduced.

Whenever a reference document is created, renamed, or removed, this index MUST be updated accordingly.

Changes require documentation review and architectural approval.

---

# Compliance

The FamilyOS reference documentation complies with this specification when:

- every reference document has a single responsibility;
- responsibilities do not overlap;
- cross references remain consistent;
- terminology is defined in the appropriate document;
- documentation categories remain clearly separated;
- navigation remains simple and unambiguous.

---

# Summary

The FamilyOS Reference documentation establishes the common language, terminology, naming conventions, reserved identifiers, and documentation responsibilities shared across the platform.

This index serves as the authoritative navigation entry point for contributors, reviewers, architects, and plugin developers.

By clearly identifying the responsibility of every reference document, it helps preserve consistency, maintainability, and the Single Source of Truth throughout the FamilyOS ecosystem.
