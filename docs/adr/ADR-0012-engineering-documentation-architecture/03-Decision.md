# Decision

## Purpose

This document records the architectural decision adopted for the FamilyOS documentation architecture.

The objective is to establish a stable, scalable, and maintainable documentation structure that preserves engineering knowledge and supports the long-term evolution of the FamilyOS platform.

---

# Decision Statement

FamilyOS SHALL adopt a structured documentation architecture composed of four normative document families, supported by governance and reference documentation.

The documentation architecture becomes an integral part of the platform architecture and SHALL evolve according to the engineering principles established by the FamilyOS Foundation.

---

# Documentation Architecture

The official documentation architecture is organized as follows.

```text
Project Governance
│
├── README
├── GOVERNANCE
├── VISION
├── PRINCIPLES
├── CONTRIBUTING
│
└── docs/
    ├── 00-foundation/
    ├── 01-architecture/
    │   ├── adr/
    │   └── rfcs/
    ├── 02-specifications/
    ├── 03-engineering/
    ├── 04-reference/
    ├── 05-guides/
    ├── 06-tutorials/
    └── 07-contributing/
```

This organization SHALL remain the authoritative documentation structure unless superseded by a future Architectural Decision Record.

---

# Normative Document Families

FamilyOS defines four normative document families.

## Foundation

The Foundation defines the enduring principles of the project.

It establishes:

* vision;
* mission;
* core values;
* engineering philosophy;
* architecture principles;
* documentation principles;
* governance;
* long-term commitments.

The Foundation provides the philosophical basis for every subsequent document.

---

## Architectural Decision Records (ADR)

Architectural Decision Records capture significant architectural decisions.

Each ADR SHALL document:

* context;
* problem;
* decision;
* rationale;
* consequences.

ADRs answer the question:

> **Why was this decision made?**

---

## Request for Comments (RFC)

RFCs describe technical designs before implementation.

They define:

* architecture proposals;
* technical solutions;
* design alternatives;
* implementation direction.

RFCs answer the question:

> **How should the system be designed?**

---

## Specifications (SPEC)

Specifications define normative implementation requirements.

SPEC documents describe:

* mandatory behavior;
* functional requirements;
* non-functional requirements;
* compliance expectations.

SPEC documents answer the question:

> **What must be implemented?**

---

## Engineering Documents (ENG)

Engineering documents define engineering governance and standards.

They describe:

* engineering processes;
* documentation standards;
* testing standards;
* quality standards;
* build standards;
* release standards.

ENG documents answer the question:

> **How is FamilyOS engineered?**

---

# Supporting Documentation

In addition to the normative document families, FamilyOS maintains supporting documentation.

Supporting documentation includes:

* reference documentation;
* engineering guides;
* tutorials;
* contribution guides.

Supporting documentation provides practical assistance but SHALL NOT introduce normative requirements that conflict with ADR, RFC, SPEC, or ENG documents.

---

# Responsibility Boundaries

Every document family SHALL have a unique responsibility.

Normative content MUST NOT be duplicated across multiple document families.

Instead, documents SHALL reference the authoritative source.

The responsibilities are summarized below.

| Document Family | Primary Responsibility                      |
| --------------- | ------------------------------------------- |
| Foundation      | Vision, philosophy, and enduring principles |
| ADR             | Architectural decisions                     |
| RFC             | Technical designs                           |
| SPEC            | Normative implementation requirements       |
| ENG             | Engineering governance and standards        |
| Reference       | Shared terminology and reference material   |
| Guides          | Practical guidance                          |
| Tutorials       | Learning-oriented documentation             |

---

# Documentation Lifecycle

Documentation SHALL evolve together with the platform.

Major engineering changes SHOULD follow the documented engineering lifecycle.

```text
Need
  ↓
Foundation (if principles evolve)
  ↓
ADR (if architecture changes)
  ↓
RFC (if design is required)
  ↓
SPEC (if implementation requirements are needed)
  ↓
ENG (if engineering practices evolve)
  ↓
Implementation
  ↓
Testing
  ↓
Documentation Update
  ↓
Release
```

Not every change requires every document family.

The level of documentation SHALL remain proportional to the significance of the change.

---

# Cross-Reference Policy

All normative documents SHALL use permanent identifiers.

Examples include:

* ADR-0012
* RFC-0015
* SPEC-0006
* ENG-003

Cross-references SHOULD reference the authoritative document rather than duplicate its content.

---

# Governance

Future modifications to the documentation architecture SHALL themselves be documented through an Architectural Decision Record.

This ensures that the documentation architecture evolves in a controlled, transparent, and traceable manner.

---

# Decision Summary

The FamilyOS project formally adopts a structured documentation architecture composed of clearly defined document families with distinct responsibilities.

This decision provides:

* architectural clarity;
* engineering consistency;
* documentation scalability;
* knowledge preservation;
* long-term maintainability.

This architecture SHALL serve as the authoritative foundation for all future FamilyOS documentation.
