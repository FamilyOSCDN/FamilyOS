# Documentation Framework

# 08 Documentation Versioning

## Context

Documentation is a long-term asset of the FamilyOS ecosystem. As the platform evolves, documentation must remain understandable, traceable, and compatible with previous versions.

Documentation versioning defines how documentation changes are identified, tracked, reviewed, and released alongside software components, specifications, RFCs, ADRs, and official plugins.

The objective is to ensure that every documented decision, capability, and architectural element has a clear history.

---

# Documentation Versioning Principles

Documentation versioning follows these fundamental principles:

## Traceability

Every significant documentation change must be traceable to:

* a commit,
* a pull request,
* an RFC,
* an ADR,
* an EPIC,
* a SPEC,
* or another approved engineering artifact.

Documentation history must allow contributors to understand why a change happened.

---

## Stability

Documentation versions must reflect the maturity level of the documented subject.

Stable documentation should not change without:

* a clear reason,
* an identified owner,
* an appropriate review process.

---

## Compatibility

Documentation changes must consider compatibility with:

* previous documentation versions,
* existing implementations,
* external contributors,
* generated artifacts.

Breaking changes require explicit documentation.

---

# Documentation Version Format

FamilyOS documentation follows semantic versioning principles.

The format is:

```
MAJOR.MINOR.PATCH
```

Example:

```
2.4.1
```

---

# Major Documentation Version

A major version indicates a breaking documentation change.

Examples:

* complete restructuring of a framework,
* removal of previously supported concepts,
* replacement of a public specification,
* incompatible terminology changes.

Example:

```
1.0.0 → 2.0.0
```

A major version requires:

* migration notes,
* compatibility explanation,
* approval from documentation governance.

---

# Minor Documentation Version

A minor version introduces new information without breaking existing understanding.

Examples:

* new chapters,
* additional examples,
* new supported scenarios,
* expanded explanations.

Example:

```
1.2.0 → 1.3.0
```

Minor changes should preserve existing references whenever possible.

---

# Patch Documentation Version

A patch version contains corrections and improvements.

Examples:

* spelling corrections,
* formatting fixes,
* clarification of existing text,
* broken references correction.

Example:

```
1.3.2 → 1.3.3
```

Patch updates do not change the meaning of the documented concepts.

---

# Documentation Lifecycle Versioning

Documentation versions follow the lifecycle of the related artifact.

Example:

```
Draft
 |
 v
Review
 |
 v
Approved
 |
 v
Stable
 |
 v
Deprecated
 |
 v
Archived
```

Each lifecycle transition may create a new documentation version.

---

# Versioning During RFC Development

RFC documentation evolves through multiple stages.

Example:

```
RFC-0015 v0.1.0
        |
        v
RFC-0015 v0.2.0
        |
        v
RFC-0015 v1.0.0 Approved
```

Rules:

* Draft RFCs use version `0.x.y`.
* Approved RFCs start at version `1.0.0`.
* Major revisions after approval require a new major version.

---

# Versioning During SPEC Development

Specifications require stronger stability guarantees.

Rules:

* Initial approved specification starts at `1.0.0`.
* Normative changes require version updates.
* Clarifications without behavior changes may use patch versions.

Example:

```
SPEC-0005 v1.0.0
SPEC-0005 v1.0.1
SPEC-0005 v1.1.0
SPEC-0005 v2.0.0
```

---

# Documentation Change Classification

Every documentation update must be classified.

## Editorial Change

No semantic impact.

Examples:

* grammar,
* spelling,
* formatting.

Version impact:

```
PATCH
```

---

## Informative Change

Adds explanation without changing requirements.

Examples:

* additional examples,
* diagrams,
* explanations.

Version impact:

```
PATCH or MINOR
```

---

## Normative Change

Changes requirements, rules, or expected behavior.

Examples:

* updated architecture rule,
* changed API contract,
* modified specification requirement.

Version impact:

```
MINOR or MAJOR
```

---

# Documentation Changelog Requirements

Each versioned documentation artifact should maintain a changelog.

Required information:

```markdown
## Version X.Y.Z

Date:
Author:

Changes:

- Added:
- Modified:
- Removed:

Reason:

Related artifacts:
```

---

# Version References

Documentation references should always identify the version used.

Examples:

Correct:

```
Based on SPEC-0005 v1.0.0
```

Incorrect:

```
Based on SPEC-0005
```

Version references prevent ambiguity.

---

# Archived Documentation

Deprecated documentation must not be deleted immediately.

Archived documentation provides:

* historical context,
* migration information,
* architectural decisions history.

Archived documents must contain:

* final version,
* deprecation date,
* replacement document reference.

---

# Documentation Repository Integration

Documentation versions are managed through:

* Git history,
* tags,
* release notes,
* changelogs.

Example:

```
v3.6.0-documentation-framework
```

Tags should identify important documentation milestones.

---

# Governance Integration

Documentation versioning is controlled by the Documentation Framework governance rules.

Responsibilities:

| Role       | Responsibility                        |
| ---------- | ------------------------------------- |
| Author     | Creates and updates documentation     |
| Reviewer   | Validates quality and consistency     |
| Maintainer | Approves lifecycle changes            |
| Architect  | Validates architectural documentation |

---

# Relationship With Other Frameworks

Documentation versioning integrates with:

* Engineering Foundation,
* RFC Framework,
* ADR Framework,
* Specification Framework,
* Release Framework,
* Quality Framework.

Documentation versions must remain aligned with software and architecture evolution.

---

# Final Compliance

A documentation artifact complies with FamilyOS versioning standards when:

* it follows semantic versioning rules,
* changes are traceable,
* lifecycle state is identified,
* breaking changes are documented,
* historical versions remain accessible.

Documentation versioning ensures that FamilyOS knowledge remains reliable, maintainable, and evolvable over time.
