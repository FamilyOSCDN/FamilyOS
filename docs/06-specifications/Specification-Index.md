# FamilyOS Specification Index

**Version:** 1.0.0
**Status:** Approved
**Owner:** FamilyOS Project
**Layer:** Specifications
**Directory:** `docs/06-specifications/`

---

# 1. Purpose

This document is the official registry of all FamilyOS Specifications (SPEC).

It provides a stable and centralized index of every published specification, their identifiers, versions, status, and scope.

The Specification Index is the authoritative reference for locating and identifying FamilyOS technical standards.

---

# 2. Scope

This index includes every official FamilyOS Specification regardless of its implementation status.

It does not replace individual specification documents.

Each specification remains the authoritative source for its own requirements.

---

# 3. Specification Lifecycle

Every specification follows the lifecycle defined by the Specifications layer.

Possible statuses are:

| Status      | Description                        |
| ----------- | ---------------------------------- |
| Draft       | Initial proposal under development |
| Review      | Under technical review             |
| Approved    | Official FamilyOS standard         |
| Implemented | Fully implemented in the platform  |
| Deprecated  | Scheduled for removal              |
| Superseded  | Replaced by a newer specification  |

---

# 4. Specification Categories

FamilyOS specifications are organized into logical groups.

## Documentation Foundation

Defines how specifications are written and maintained.

| ID        | Title                       | Status  | Version |
| --------- | --------------------------- | ------- | ------- |
| SPEC-0001 | Documentation Structure     | Planned | 1.0.0   |
| SPEC-0002 | Specification Writing Rules | Planned | 1.0.0   |

---

## Platform Core

Defines platform-wide technical contracts.

| ID        | Title            | Status  | Version |
| --------- | ---------------- | ------- | ------- |
| SPEC-0003 | Identifier       | Planned | 1.0.0   |
| SPEC-0004 | Metadata         | Planned | 1.0.0   |
| SPEC-0005 | Versioning       | Planned | 1.0.0   |
| SPEC-0006 | Document Format  | Planned | 1.0.0   |
| SPEC-0007 | Directory Layout | Planned | 1.0.0   |
| SPEC-0008 | File Format      | Planned | 1.0.0   |

---

## Plugin System

Defines the contracts governing plugins.

| ID        | Title               | Status  | Version |
| --------- | ------------------- | ------- | ------- |
| SPEC-0010 | Plugin Manifest     | Planned | 1.0.0   |
| SPEC-0011 | Plugin Lifecycle    | Planned | 1.0.0   |
| SPEC-0012 | Plugin Capability   | Planned | 1.0.0   |
| SPEC-0013 | Plugin Contribution | Planned | 1.0.0   |
| SPEC-0014 | Plugin Hooks        | Planned | 1.0.0   |
| SPEC-0015 | Plugin Dependencies | Planned | 1.0.0   |

---

## Generation Framework

Defines generation-related contracts.

| ID        | Title               | Status  | Version |
| --------- | ------------------- | ------- | ------- |
| SPEC-0020 | Generation Artifact | Planned | 1.0.0   |
| SPEC-0021 | Generation Recipe   | Planned | 1.0.0   |
| SPEC-0022 | Generation Preset   | Planned | 1.0.0   |
| SPEC-0023 | Template            | Planned | 1.0.0   |
| SPEC-0024 | Domain Generation   | Planned | 1.0.0   |

---

## Domain Model

Defines Domain-Driven Design contracts.

| ID        | Title        | Status  | Version |
| --------- | ------------ | ------- | ------- |
| SPEC-0030 | Aggregate    | Planned | 1.0.0   |
| SPEC-0031 | Entity       | Planned | 1.0.0   |
| SPEC-0032 | Value Object | Planned | 1.0.0   |
| SPEC-0033 | Command      | Planned | 1.0.0   |
| SPEC-0034 | Domain Event | Planned | 1.0.0   |
| SPEC-0035 | Query        | Planned | 1.0.0   |

---

## API Specifications

Defines interface and exchange format contracts.

| ID        | Title             | Status  | Version |
| --------- | ----------------- | ------- | ------- |
| SPEC-0040 | CLI               | Planned | 1.0.0   |
| SPEC-0041 | JSON              | Planned | 1.0.0   |
| SPEC-0042 | YAML              | Planned | 1.0.0   |
| SPEC-0043 | Schema Guidelines | Planned | 1.0.0   |

---

# 5. Identifier Policy

Every specification identifier is:

* unique;
* permanent;
* immutable;
* never reused.

A specification title may evolve.

Its identifier SHALL remain unchanged.

---

# 6. Version Policy

Each specification maintains its own version history.

Specification versions are independent of:

* FamilyOS releases;
* CLI releases;
* Plugin SDK releases.

---

# 7. Cross References

Specifications may reference:

* Foundation documents;
* Architecture documents;
* Reference documents;
* other Specifications;
* ADRs;
* RFCs.

References SHALL use permanent identifiers whenever available.

Example:

```text
SPEC-0012
ADR-0007
RFC-0010
```

---

# 8. Future Specifications

New specifications SHALL be added to this registry before publication.

Identifier ranges SHALL remain stable.

Deprecated specifications SHALL remain listed for historical traceability.

Superseded specifications SHALL reference their replacements.

---

# 9. Maintenance

The Specification Index SHALL be updated whenever:

* a new specification is created;
* a specification changes status;
* a specification is deprecated;
* a specification is superseded.

Maintaining this document is mandatory for preserving the integrity of the FamilyOS specification catalogue.

---

# 10. References

Related documents:

* `README.md`
* `Writing-Guide.md`
* `SPEC-0001-Documentation-Structure.md`

---

# 11. Revision History

| Version | Status   | Description                                              |
| ------- | -------- | -------------------------------------------------------- |
| 1.0.0   | Approved | Initial publication of the FamilyOS Specification Index. |
