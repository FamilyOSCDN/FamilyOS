# FamilyOS Specification Writing Guide

**Version:** 1.0.0
**Status:** Approved
**Owner:** FamilyOS Project
**Layer:** Specifications
**Directory:** `docs/06-specifications/`

---

# 1. Purpose

This document defines the official writing rules for all FamilyOS Specifications (SPEC).

Its objective is to ensure that every specification is:

* consistent;
* precise;
* implementation-independent;
* easy to review;
* easy to maintain.

All FamilyOS Specifications SHALL comply with this guide.

---

# 2. Scope

This guide applies to every document identified as a FamilyOS Specification (`SPEC-XXXX`).

It defines:

* document organization;
* writing style;
* normative language;
* requirement format;
* examples;
* references;
* versioning conventions.

It does not define the technical content of individual specifications.

---

# 3. General Principles

Every specification SHALL follow these principles.

## Clarity

Requirements MUST be understandable without ambiguity.

## Precision

Requirements SHALL describe observable behavior.

Avoid subjective wording.

## Stability

Specifications define contracts.

Contracts SHALL evolve more slowly than implementations.

## Independence

Specifications MUST NOT describe implementation details.

They define **what** must be respected, not **how** it is implemented.

## Consistency

Terminology SHALL remain consistent across all specifications.

Definitions from the Reference layer SHALL be reused whenever applicable.

---

# 4. Standard Document Structure

Every specification SHALL use the following structure.

```text id="s5jkdp"
Document Metadata

1. Purpose
2. Scope
3. Normative References
4. Terms and Definitions
5. Normative Language
6. Requirements
7. Constraints
8. Conformance
9. Security Considerations
10. Compatibility
11. Examples
12. References
13. Revision History
```

Sections MAY be omitted only if explicitly marked as not applicable.

---

# 5. Document Metadata

Every specification SHALL include:

* Identifier
* Title
* Version
* Status
* Owner
* Layer

Example:

```text id="woxyop"
Identifier: SPEC-0003
Title: Identifier
Version: 1.0.0
Status: Approved
Owner: FamilyOS Project
Layer: Specifications
```

---

# 6. Normative Language

Specifications SHALL use the following keywords with normative meaning:

* MUST
* MUST NOT
* REQUIRED
* SHALL
* SHALL NOT
* SHOULD
* SHOULD NOT
* RECOMMENDED
* MAY
* OPTIONAL

These keywords SHALL appear in uppercase.

Avoid informal wording such as:

* should probably
* maybe
* generally
* usually
* preferably

unless used outside normative statements.

---

# 7. Writing Requirements

Requirements SHALL be:

* atomic;
* testable;
* measurable whenever possible;
* implementation-independent.

Avoid combining multiple independent requirements into a single statement.

---

# 8. Requirement Identification

Every normative requirement SHOULD have a stable identifier.

Recommended format:

```text id="q7mgnx"
SPEC-0003-R1

SPEC-0003-R2

SPEC-0003-R3
```

Requirement identifiers SHALL remain stable throughout the lifetime of the specification.

---

# 9. Examples

Examples are informative.

Examples SHALL NOT introduce additional requirements.

Whenever possible, examples SHOULD be clearly distinguished from normative text.

---

# 10. References

Specifications may reference:

* Foundation
* Architecture
* Engineering
* Reference
* Specifications
* ADR
* RFC

Permanent identifiers SHOULD be used whenever available.

Example:

```text id="7m4lx6"
SPEC-0011

ADR-0007

RFC-0010
```

---

# 11. Conformance

Each specification SHALL define:

* the components concerned;
* mandatory requirements;
* optional capabilities;
* verification expectations.

Conformance requirements SHALL be objectively verifiable.

---

# 12. Security Considerations

Every specification SHALL contain a Security Considerations section.

If no specific security implications exist, the specification SHALL explicitly state that none have been identified.

---

# 13. Compatibility

Specifications SHALL indicate compatibility implications whenever requirements change.

Backward compatibility SHOULD be preserved whenever practical.

Breaking changes SHALL be clearly identified.

---

# 14. Versioning

Every specification SHALL maintain its own revision history.

Changes SHOULD be documented using semantic versioning principles:

* Major
* Minor
* Patch

---

# 15. Review Checklist

Before approval, verify that the specification:

* clearly defines its purpose;
* contains no implementation details;
* uses normative language correctly;
* follows the standard structure;
* contains complete references;
* contains a revision history;
* has no ambiguity;
* avoids duplication with existing specifications.

---

# 16. References

Related documents:

* `README.md`
* `Specification-Index.md`
* `SPEC-0001-Documentation-Structure.md`

---

# 17. Revision History

| Version | Status   | Description                                                      |
| ------- | -------- | ---------------------------------------------------------------- |
| 1.0.0   | Approved | Initial publication of the FamilyOS Specification Writing Guide. |
