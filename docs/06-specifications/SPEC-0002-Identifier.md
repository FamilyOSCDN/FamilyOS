# SPEC-0002 — Identifier

**Identifier:** SPEC-0002
**Title:** Identifier
**Version:** 1.0.0
**Status:** Approved
**Owner:** FamilyOS Project
**Layer:** Specifications

---

# Abstract

This specification defines the normative requirements for identifiers used throughout the FamilyOS platform.

Identifiers provide stable, unique, and persistent references for platform resources, documentation, plugins, domains, artifacts, events, commands, and other technical entities.

All FamilyOS components SHALL comply with this specification when defining or consuming identifiers.

---

# 1. Purpose

The purpose of this specification is to establish a single, consistent identification model for the FamilyOS platform.

A common identifier model enables:

- interoperability;
- traceability;
- documentation consistency;
- stable references;
- long-term maintainability.

---

# 2. Scope

This specification applies to every permanent identifier used within FamilyOS, including but not limited to:

- Specifications;
- ADRs;
- RFCs;
- plugins;
- capabilities;
- domains;
- artifacts;
- recipes;
- presets;
- commands;
- events;
- queries;
- aggregates;
- value objects.

This specification does not define runtime-generated identifiers such as UUIDs created during execution.

---

# 3. Normative References

This specification is related to:

- SPEC-0001 — Documentation Structure
- FamilyOS Specification Writing Guide

---

# 4. Terms and Definitions

## Identifier

A permanent textual value uniquely identifying an entity.

## Entity

Any documented, modeled, or implemented object within the FamilyOS platform.

## Prefix

The alphabetic portion of an identifier indicating its category.

Example:

```text
SPEC
ADR
RFC
```

---

# 5. Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY and OPTIONAL are to be interpreted as described by the FamilyOS Specification Writing Guide.

---

# 6. Requirements

## SPEC-0002-R1 — Uniqueness

Every permanent identifier MUST uniquely identify exactly one entity.

Two different entities SHALL NOT share the same identifier.

---

## SPEC-0002-R2 — Permanence

A permanent identifier MUST remain unchanged for the lifetime of the entity.

Identifiers SHALL NOT be reassigned.

---

## SPEC-0002-R3 — Human Readability

Identifiers SHOULD be concise and readable.

Abbreviations SHOULD be consistent across the platform.

---

## SPEC-0002-R4 — Category Prefix

Every identifier MUST begin with a category prefix.

Examples include:

```text
SPEC
ADR
RFC
DOMAIN
PLUGIN
CAPABILITY
```

---

## SPEC-0002-R5 — Stable Format

Identifiers SHALL follow the syntax:

```text
<PREFIX>-<NUMBER>
```

Example:

```text
SPEC-0002
ADR-0007
RFC-0010
```

Category-specific specifications MAY define additional suffixes where required.

---

## SPEC-0002-R6 — Case

Category prefixes SHALL use uppercase letters.

Identifiers SHALL be treated as case-sensitive in documentation.

---

## SPEC-0002-R7 — References

Whenever possible, documentation SHALL reference entities by identifier instead of title alone.

Example:

```text
See SPEC-0002.
```

---

## SPEC-0002-R8 — Immutability

Changing the title, description or implementation of an entity MUST NOT require changing its identifier.

---

## SPEC-0002-R9 — Traceability

Identifiers SHOULD be usable across:

- documentation;
- architecture decisions;
- RFCs;
- tests;
- source code;
- generated artifacts.

---

# 7. Constraints

Identifiers SHALL:

- remain implementation-independent;
- avoid semantic ambiguity;
- avoid duplication;
- be stable across releases.

Meaning SHALL NOT depend on file paths or implementation details.

---

# 8. Conformance

The following components are subject to this specification:

- documentation;
- CLI;
- generation framework;
- plugin SDK;
- official plugins;
- future FamilyOS tooling.

A component conforms if every permanent identifier satisfies the mandatory requirements defined by this specification.

---

# 9. Security Considerations

Identifiers SHALL NOT contain confidential, personal, or security-sensitive information.

Identifiers are intended for reference, not for storing data.

---

# 10. Compatibility

Existing identifiers SHALL remain valid across compatible platform versions.

If an entity becomes obsolete, its identifier SHOULD be retained for historical traceability and marked as deprecated rather than reused.

---

# 11. Examples

Documentation identifier:

```text
SPEC-0005
```

Architecture decision:

```text
ADR-0008
```

Request for comments:

```text
RFC-0010
```

Plugin capability (illustrative):

```text
CAPABILITY-0004
```

---

# 12. References

Related documents:

- SPEC-0001 — Documentation Structure
- README.md
- Specification-Index.md
- Writing-Guide.md

---

# 13. Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0.0 | Approved | Initial publication of the Identifier specification. |

