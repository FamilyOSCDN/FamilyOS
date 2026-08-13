# FamilyOS Specification Index

**Version:** 1.1.0
**Status:** Approved
**Owner:** FamilyOS Project
**Layer:** Specifications
**Directory:** `docs/06-specifications/`

---

# 1. Purpose

This document is the official registry of all FamilyOS Specifications (SPEC).

It provides a stable and centralized index of published specifications,
reserved specification identifiers, versions, status, and scope.

The Specification Index is the authoritative catalogue for locating and
identifying FamilyOS technical standards.

Individual specification documents remain authoritative for their own
requirements, status, and version.

---

# 2. Scope

This index includes:

* every published FamilyOS Specification;
* reserved identifiers for planned specifications;
* the current status of published specifications;
* the current version of published specifications;
* planned specification categories and identifier ranges.

This index does not replace individual specification documents.

Each published specification remains the authoritative source for its own
requirements.

---

# 3. Specification Lifecycle

Published specifications follow the lifecycle defined by the Specifications
layer.

Possible statuses include:

| Status | Description |
|---|---|
| Draft | Specification under development |
| Review | Specification under technical review |
| Approved | Official FamilyOS standard |
| Implemented | Fully implemented in the platform |
| Deprecated | Scheduled for removal |
| Superseded | Replaced by a newer specification |

A reserved identifier may additionally be listed as `Planned` in this index
before the corresponding specification document is published.

`Planned` therefore represents catalogue reservation state rather than the
lifecycle state of a published specification.

---

# 4. Published Specifications

The following specification documents currently exist under the canonical
Specifications directory.

## Documentation and Platform Foundation

| ID | Title | Status | Version |
|---|---|---|---|
| SPEC-0001 | Documentation Structure | Approved | 1.0.0 |
| SPEC-0002 | Identifier | Draft | 2.0.0 |
| SPEC-0003 | Metadata | Approved | 1.0.0 |
| SPEC-0004 | Versioning | Approved | 1.0.0 |
| SPEC-0005 | Document Format | Approved | 1.0.0 |
| SPEC-0006 | Directory Layout | Approved | 1.0.0 |
| SPEC-0007 | File Format | Approved | 1.0.0 |
| SPEC-0008 | Naming Conventions | Draft | 2.0.0 |

---

## Plugin System

| ID | Title | Status | Version |
|---|---|---|---|
| SPEC-0009 | Plugin Manifest | Draft | 2.0.0 |
| SPEC-0010 | Plugin Capability Contract | Draft | 2.0.0 |
| SPEC-0011 | Plugin Contribution Contract | Draft | 1.0.0 |
| SPEC-0012 | Plugin Lifecycle Contract | Draft | 1.0.0 |
| SPEC-0013 | Security Profile Contract | Draft | 1.0.0 |

The identifiers and metadata above correspond to the canonical specification
documents currently present in `docs/06-specifications/`.

---

# 5. Reserved Specifications

The following identifiers are reserved for future specifications.

Reservation prevents identifier reuse and preserves the planned catalogue
structure.

## Plugin System

| ID | Title | Status | Version |
|---|---|---|---|
| SPEC-0014 | Plugin Hooks | Planned | 1.0.0 |
| SPEC-0015 | Plugin Dependencies | Planned | 1.0.0 |

---

## Generation Framework

| ID | Title | Status | Version |
|---|---|---|---|
| SPEC-0020 | Generation Artifact | Planned | 1.0.0 |
| SPEC-0021 | Generation Recipe | Planned | 1.0.0 |
| SPEC-0022 | Generation Preset | Planned | 1.0.0 |
| SPEC-0023 | Template | Planned | 1.0.0 |
| SPEC-0024 | Domain Generation | Planned | 1.0.0 |

---

## Domain Model

| ID | Title | Status | Version |
|---|---|---|---|
| SPEC-0030 | Aggregate | Planned | 1.0.0 |
| SPEC-0031 | Entity | Planned | 1.0.0 |
| SPEC-0032 | Value Object | Planned | 1.0.0 |
| SPEC-0033 | Command | Planned | 1.0.0 |
| SPEC-0034 | Domain Event | Planned | 1.0.0 |
| SPEC-0035 | Query | Planned | 1.0.0 |

---

## API Specifications

| ID | Title | Status | Version |
|---|---|---|---|
| SPEC-0040 | CLI | Planned | 1.0.0 |
| SPEC-0041 | JSON | Planned | 1.0.0 |
| SPEC-0042 | YAML | Planned | 1.0.0 |
| SPEC-0043 | Schema Guidelines | Planned | 1.0.0 |

---

# 6. Identifier Policy

Every specification identifier is:

* unique;
* permanent;
* immutable;
* never reused.

A specification title may evolve.

Its identifier SHALL remain unchanged after publication.

Reserved identifiers SHALL NOT be assigned to another specification unless
the reservation itself is formally revised before publication.

Examples appearing in specification documentation do not constitute
publication or allocation of an identifier unless the corresponding
specification document exists or the identifier is explicitly reserved by
this registry.

---

# 7. Version Policy

Each published specification maintains its own version history.

Specification versions are independent of:

* FamilyOS releases;
* CLI releases;
* Plugin SDK releases;
* the version of this Specification Index.

The status and version recorded for a published specification in this index
SHALL reflect the corresponding canonical specification document.

---

# 8. Cross References

Specifications may reference:

* Foundation documents;
* Architecture documents;
* Reference documents;
* other Specifications;
* ADRs;
* RFCs;
* EPICs.

References SHALL use permanent identifiers whenever available.

Example:

```text
SPEC-0012
ADR-0007
RFC-0010
```

Requirement identifiers may extend a specification identifier.

Example:

```text
SPEC-0032-R4
```

Such examples do not by themselves establish publication of the referenced
specification.

---

# 9. Future Specifications

New specifications SHALL be added to this registry before or at publication.

Identifier ranges SHALL remain stable.

Planned identifiers MAY be reserved before their specification documents
exist.

When a reserved specification is published:

1. its canonical document SHALL use the reserved identifier;
2. its actual title SHALL be reconciled with this registry;
3. its actual lifecycle status SHALL replace `Planned`;
4. its actual version SHALL replace the reserved version entry.

Deprecated specifications SHALL remain listed for historical traceability.

Superseded specifications SHALL reference their replacements.

---

# 10. Maintenance

The Specification Index SHALL be updated whenever:

* a new specification is created;
* a reserved identifier is added or changed;
* a specification changes title;
* a specification changes status;
* a specification changes version;
* a specification is deprecated;
* a specification is superseded.

Canonical metadata for an existing specification SHALL be derived from its
corresponding specification document.

Maintaining this document is mandatory for preserving the integrity of the
FamilyOS specification catalogue.

---

# 11. References

Related documents:

* `README.md`
* `Writing-Guide.md`
* `SPEC-0001-Documentation-Structure.md`

---

# 12. Revision History

| Version | Status | Description |
|---|---|---|
| 1.0.0 | Approved | Initial publication of the FamilyOS Specification Index |
| 1.1.0 | Approved | Reconciled published specification identifiers, titles, statuses, versions, and future identifier reservations with the canonical specification catalogue |
