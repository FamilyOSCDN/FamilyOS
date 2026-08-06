# Documentation Framework

# 18 Documentation Deprecation Policy

## Context

FamilyOS documentation evolves continuously as architecture, specifications, and engineering practices mature.

Some documentation artifacts may become obsolete because of:

* replaced architectures,
* updated standards,
* new specifications,
* improved processes,
* discontinued features.

Documentation deprecation provides a controlled method to retire outdated documents while preserving historical knowledge.

---

# Documentation Deprecation Principles

FamilyOS documentation deprecation follows these principles.

## Preservation

Deprecated documentation must remain accessible for historical reference.

---

## Transparency

Users must understand:

* why a document is deprecated,
* what replaces it,
* when the transition occurs.

---

## Controlled Transition

Deprecation must provide enough time for contributors and consumers to migrate.

---

## No Silent Removal

Official documentation must not disappear without a documented lifecycle transition.

---

# Deprecation Lifecycle

The deprecation lifecycle is:

```text id="u2n4g7"
Active

  |

  v

Deprecated

  |

  v

Archived
```

---

# Active State

An active document is:

* officially supported,
* maintained,
* referenced by current documentation.

---

# Deprecated State

A deprecated document is:

* still available,
* no longer recommended,
* scheduled for replacement or archival.

---

# Archived State

An archived document is:

* preserved permanently,
* read-only,
* maintained for historical purposes.

---

# Deprecation Triggers

A document may be deprecated when:

## Replacement Exists

Example:

* old specification replaced by a new specification,
* old architecture replaced by a new design.

---

## Information Becomes Obsolete

Example:

* removed features,
* outdated procedures,
* incompatible approaches.

---

## Duplicate Information Exists

Example:

* multiple documents describe the same concept.

---

## Standards Change

Example:

* new documentation template,
* new repository organization.

---

# Deprecation Proposal

A deprecation proposal must include:

```yaml id="z6q3fd"
deprecation:
  document: DOC-XXXX
  reason: "Replaced by new specification"
  replacement: DOC-YYYY
  owner: documentation-team
```

---

# Deprecation Review

Deprecation requires review.

Reviewers verify:

* reason is valid,
* replacement exists,
* migration path is available,
* references are updated.

---

# Deprecation Notice Requirements

Deprecated documents must contain a notice.

Example:

```markdown id="1g9d5v"
> Deprecated

This document has been replaced by:
DOC-YYYY

Reason:
New architecture model.

Migration:
See migration guide.
```

---

# Reference Management

Before archival:

* active references must be updated,
* indexes must be updated,
* replacement documents must be linked.

---

# Deprecation Timeline

Recommended process:

```text id="9t6x2p"
Deprecation Proposal

        |

Review

        |

Deprecation Announcement

        |

Migration Period

        |

Archive
```

---

# Migration Support

Deprecated documents should provide:

* replacement references,
* migration instructions,
* compatibility notes.

---

# Archived Documentation Rules

Archived documents must:

* remain immutable,
* keep their final version,
* preserve original identifiers,
* retain historical metadata.

Example:

```yaml id="j4k9zc"
document:
  status: archived
  final_version: 2.3.0
  archived_date: YYYY-MM-DD
```

---

# Deprecation and Versioning

Deprecation events must be versioned.

Examples:

```text id="m3e6x1"
Document v1.5.0

        |

        v

Document v2.0.0
Deprecated
```

---

# Automation Support

Future automation may detect:

* stale references,
* deprecated identifiers,
* missing replacements,
* archived document usage.

---

# Governance Rules

The following rules apply:

1. Deprecated documents must not be deleted immediately.
2. Replacement documentation must be identified.
3. Deprecation reasons must be documented.
4. References must be migrated when possible.
5. Archived history must remain available.

---

# Integration With Release Management

Deprecation should be communicated through:

* release notes,
* migration guides,
* changelogs.

---

# Relationship With Other Frameworks

Documentation Deprecation Policy integrates with:

* Documentation Lifecycle,
* Documentation Versioning,
* Documentation Migration Strategy,
* Documentation Governance,
* Release Framework.

---

# Final Compliance

Documentation deprecation is compliant when:

* lifecycle transitions are controlled,
* replacement paths exist,
* users are informed,
* history is preserved,
* obsolete information is managed responsibly.

The Documentation Deprecation Policy ensures that FamilyOS can evolve while protecting accumulated engineering knowledge.
