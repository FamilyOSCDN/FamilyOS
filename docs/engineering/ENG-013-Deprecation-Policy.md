# ENG-013 — Deprecation Policy

## Metadata

| Field | Value |
|---|---|
| Identifier | ENG-013 |
| Title | Deprecation Policy |
| Category | Engineering |
| Version | 1.0.0 |
| Status | Approved |
| Date | 2026-08-04 |

---

# 1. Purpose

This document defines the official deprecation policy for the FamilyOS
platform.

The objective is to provide a controlled and predictable process for
retiring features, APIs, behaviors, and components while preserving platform
stability.

---

# 2. Scope

This policy applies to:

- Core Platform;
- Runtime;
- CLI;
- SDK;
- APIs;
- Plugins;
- Configuration formats;
- Data formats;
- Documentation.

---

# 3. Deprecation Principles

FamilyOS deprecation SHALL follow these principles:

- transparency;
- predictability;
- migration support;
- backward compatibility awareness;
- controlled removal.

---

# 4. Reasons for Deprecation

A component MAY be deprecated when:

- a better replacement exists;
- maintenance cost becomes excessive;
- security risks are identified;
- architectural improvements require change;
- compatibility constraints require evolution.

---

# 5. Deprecation Lifecycle

Deprecation SHALL follow these phases:

| Phase | Description |
|---|---|
| Active | Feature is fully supported |
| Deprecated | Feature remains available but discouraged |
| Removal Planned | Removal is scheduled |
| Removed | Feature is no longer available |

---

# 6. Deprecation Announcement

Deprecated features SHALL be documented.

Documentation SHOULD include:

- reason for deprecation;
- affected versions;
- replacement solution;
- migration instructions.

---

# 7. Deprecation Period

Deprecated functionality SHOULD remain available for a reasonable transition
period.

The duration MAY depend on:

- user impact;
- ecosystem usage;
- security considerations;
- technical constraints.

---

# 8. Deprecation Warnings

Deprecated functionality SHOULD provide clear warnings.

Warnings SHOULD identify:

- deprecated component;
- recommended alternative;
- expected removal timeline.

---

# 9. API Deprecation

API deprecation SHALL consider:

- existing consumers;
- plugin integrations;
- migration complexity.

API removal SHALL NOT occur without appropriate communication.

---

# 10. Plugin Deprecation

Plugin capabilities, interfaces, or dependencies MAY be deprecated.

Plugin ecosystem impact SHALL be evaluated before removal.

---

# 11. Removal Process

Before removal, engineering SHALL verify:

- migration documentation exists;
- compatibility impact is understood;
- replacement solutions are available;
- release notes are prepared.

---

# 12. Testing Requirements

Deprecated functionality SHOULD remain covered by tests until removal.

Migration paths SHOULD be tested.

---

# 13. Compliance

All FamilyOS deprecations SHALL follow this policy.

Exceptions SHALL be documented and approved.

---

# Normative References

- ENG-011 — Versioning Strategy
- ENG-012 — Backward Compatibility
- ENG-010 — Release Engineering

---

# Revision History

| Version | Date | Description |
|---|---|---|
| 1.0.0 | 2026-08-04 | Initial publication |