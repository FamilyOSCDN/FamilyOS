# EPIC-DOC-001 — Documentation Framework

## Overview

EPIC-DOC-001 defines the canonical **FamilyOS Documentation Framework**.

The framework establishes how engineering documentation is:

* structured;
* created;
* reviewed;
* validated;
* versioned;
* governed;
* maintained;
* automated;
* organized;
* migrated;
* deprecated;
* measured;
* released;
* evolved.

FamilyOS treats documentation as a first-class engineering artifact.

Documentation is therefore part of the engineering system itself rather than a secondary activity performed after implementation.

---

# Framework Identity

| Field                   | Value                                     |
| ----------------------- | ----------------------------------------- |
| EPIC                    | EPIC-DOC-001                              |
| Title                   | Documentation Framework                   |
| Version                 | 1.0.0                                     |
| Framework Type          | Engineering Framework                     |
| Domain                  | Documentation                             |
| Current Framework State | Baseline                                  |
| Current Activity        | Structural Normalization and Revalidation |
| Repository Validation   | Validated                      |
| Final Revalidation      | Validated                      |
| Canonical Range         | `00-23`                                   |
| Numbered Documents      | 24                                        |
| Control Documents       | 7                                         |
| Canonical Files         | 31                                        |

---

# Purpose

The Documentation Framework provides the common rules required to manage engineering knowledge throughout the FamilyOS lifecycle.

Its purpose is to ensure that documentation remains:

* accurate;
* understandable;
* discoverable;
* consistent;
* traceable;
* maintainable;
* reviewable;
* version controlled;
* structurally valid;
* historically recoverable.

The framework supports engineering activities across:

* architecture;
* ADRs;
* RFCs;
* specifications;
* EPICs;
* engineering frameworks;
* plugins;
* implementation guidance;
* testing;
* quality;
* security;
* observability;
* operations;
* build;
* release;
* reference documentation.

---

# Vision

The FamilyOS Documentation Framework establishes a scalable engineering knowledge system.

The framework aims to ensure that important technical knowledge can be:

```text
Created
   ↓
Structured
   ↓
Reviewed
   ↓
Validated
   ↓
Published
   ↓
Maintained
   ↓
Versioned
   ↓
Migrated
   ↓
Deprecated
   ↓
Preserved
```

Documentation SHALL evolve together with the system it describes.

---

# Core Documentation Principles

The framework is based on the following principles.

## Documentation Is an Engineering Artifact

Documentation SHALL receive engineering discipline appropriate to its importance.

---

## Single Source of Truth

Canonical information SHOULD have one authoritative location.

Uncontrolled normative duplication SHOULD be avoided.

---

## Explicit Ownership

Important documentation SHALL have identifiable ownership or an explicit governance responsibility.

---

## Traceability

Documentation SHOULD be traceable to related engineering artifacts where applicable.

Potential relationships include:

```text
EPIC
RFC
ADR
Specification
Implementation
Test
Build
Release
Operational Evidence
```

---

## Maintainability

Documentation SHALL remain understandable and safely maintainable by contributors other than its original author.

---

## Version Control

Canonical FamilyOS documentation SHALL be managed through repository version control.

---

## Validation

Documentation SHALL be validated before it is treated as authoritative.

---

## Controlled Evolution

Documentation changes SHALL preserve appropriate historical traceability.

---

# Documentation Architecture

FamilyOS documentation is organized conceptually into four major layers.

## Strategic Documentation

Strategic documentation expresses engineering direction and intent.

Examples include:

* EPICs;
* vision documents;
* roadmaps;
* framework definitions.

---

## Governance Documentation

Governance documentation defines engineering rules and decision structures.

Examples include:

* policies;
* standards;
* ADRs;
* lifecycle rules;
* governance models.

---

## Specification Documentation

Specification documentation defines technical contracts and expected behavior.

Examples include:

* RFCs;
* technical specifications;
* interfaces;
* plugin contracts;
* architecture specifications.

---

## Implementation Documentation

Implementation documentation supports practical execution.

Examples include:

* implementation guides;
* migration guides;
* operational guides;
* reference documentation;
* templates;
* examples.

---

# Canonical Repository Structure

EPIC-DOC-001 currently uses the canonical numbered range:

```text
00-23
```

The normalized framework consists of:

```text
24 numbered documents
7 control documents
31 canonical files
```

---

# Canonical Numbered Documents

```text
00-EPIC.md
01-Introduction.md
02-Documentation-Vision.md
03-Documentation-Architecture.md
04-Documentation-Standards.md
05-Documentation-Lifecycle.md
06-Documentation-Templates.md
07-Documentation-Metadata.md
08-Documentation-Versioning.md
09-Documentation-Lifecycle.md
10-Documentation-Governance.md
11-Documentation-Templates.md
12-Documentation-Automation.md
13-Documentation-Quality-Gates.md
14-Documentation-Repository-Organization.md
15-Documentation-Review-Process.md
16-Documentation-Maintenance.md
17-Documentation-Migration-Strategy.md
18-Documentation-Deprecation-Policy.md
19-Documentation-Metrics.md
20-Documentation-Framework-Validation.md
21-Documentation-Framework-Summary.md
22-Documentation-Framework-Release.md
23-Documentation-Framework-Implementation-Checklist.md
```

---

# Control Documents

The framework uses the standard FamilyOS control-document set:

```text
EPIC-DOC-001.md
EPIC.yaml
README.md
MANIFEST.md
CHANGELOG.md
VALIDATION.md
Revision-History.md
```

These documents serve different repository-governance roles.

| Document              | Responsibility                            |
| --------------------- | ----------------------------------------- |
| `EPIC-DOC-001.md`     | Consolidated framework-level summary      |
| `EPIC.yaml`           | Machine-readable framework contract       |
| `README.md`           | Human-readable navigation and orientation |
| `MANIFEST.md`         | Canonical repository inventory            |
| `CHANGELOG.md`        | Framework and repository evolution        |
| `VALIDATION.md`       | Validation requirements and evidence      |
| `Revision-History.md` | Historical framework evolution            |

---

# Historical Structural Condition

Before the current normalization, the EPIC directory contained:

```text
33 numbered files
7 control documents
40 total files
```

The numbered range nominally covered:

```text
01-23
```

but numbers `09` through `18` each contained two competing documents.

This produced ten duplicate-number groups.

---

# Historical Duplicate Groups

The historical mixed structure contained:

```text
09:
  09-Documentation-Lifecycle.md
  09-Documentation-Validation.md

10:
  10-Documentation-Automation.md
  10-Documentation-Governance.md

11:
  11-Documentation-Generation.md
  11-Documentation-Templates.md

12:
  12-Documentation-Automation.md
  12-Documentation-Publishing.md

13:
  13-Documentation-Quality-Gates.md
  13-Documentation-Traceability.md

14:
  14-Documentation-Quality.md
  14-Documentation-Repository-Organization.md

15:
  15-Documentation-Governance.md
  15-Documentation-Review-Process.md

16:
  16-Documentation-Maintenance.md
  16-Documentation-Toolchain.md

17:
  17-Documentation-Migration-Strategy.md
  17-Roadmap.md

18:
  18-Documentation-Deprecation-Policy.md
  18-References.md
```

---

# Duplicate Skeleton Classification

Repository audit showed that ten of these files were short generic framework skeletons.

They contained approximately the same generic structure:

```text
Purpose
Objectives
Principles
Responsibilities
Validation
Summary
```

and did not provide substantive domain-specific framework definitions.

The duplicate skeleton documents identified for removal are:

```text
09-Documentation-Validation.md
10-Documentation-Automation.md
11-Documentation-Generation.md
12-Documentation-Publishing.md
13-Documentation-Traceability.md
14-Documentation-Quality.md
15-Documentation-Governance.md
16-Documentation-Toolchain.md
17-Roadmap.md
18-References.md
```

---

# Canonical Substantive Documents

The substantive documents retained from the duplicate range are:

```text
09-Documentation-Lifecycle.md
10-Documentation-Governance.md
11-Documentation-Templates.md
12-Documentation-Automation.md
13-Documentation-Quality-Gates.md
14-Documentation-Repository-Organization.md
15-Documentation-Review-Process.md
16-Documentation-Maintenance.md
17-Documentation-Migration-Strategy.md
18-Documentation-Deprecation-Policy.md
```

These documents contain dedicated context, principles, architecture, rules, responsibilities, and validation semantics appropriate to their subject.

---

# Structural Normalization

The current structural normalization performs two principal actions.

## Remove Duplicate Skeleton Documents

Ten duplicate generic skeleton files are removed from the canonical structure.

---

## Introduce `00-EPIC.md`

A canonical numbered EPIC document is introduced at:

```text
00-EPIC.md
```

This produces a deterministic numbered sequence:

```text
00
01
02
03
04
05
06
07
08
09
10
11
12
13
14
15
16
17
18
19
20
21
22
23
```

---

# Structural Target

After normalization:

```text
Duplicate Number Groups: 0
Missing Numbers:         0
Numbered Documents:     24
Control Documents:       7
Canonical Files:        31
```

---

# Documentation Lifecycle

The framework defines a controlled documentation lifecycle.

A representative lifecycle is:

```text
Draft
   ↓
Review
   ↓
Validation
   ↓
Approval
   ↓
Publication
   ↓
Maintenance
   ↓
Revision
   ↓
Deprecation
   ↓
Archival
```

Exact workflow mechanisms may vary by document type.

The fundamental requirements remain:

* explicit state;
* traceability;
* review;
* validation;
* controlled evolution.

---

# Documentation Metadata

Canonical documentation SHOULD expose metadata appropriate to its role.

Potential metadata includes:

```text
Identifier
Title
Version
Status
Owner
Creation Date
Update Date
Related EPIC
Related RFC
Related ADR
Supersedes
Superseded By
```

Machine-readable formats may be used where useful.

---

# Documentation Versioning

Documentation SHALL evolve through controlled versioning.

Versioning SHOULD communicate meaningful changes without unnecessary churn.

Version semantics may vary according to document category, but changes SHALL remain traceable in repository history.

---

# Documentation Governance

Governance responsibilities include:

* document ownership;
* review;
* validation;
* approval;
* lifecycle transition;
* maintenance;
* migration;
* deprecation;
* exception handling.

Governance SHOULD be proportional to document importance and engineering impact.

---

# Documentation Automation

The framework supports automation in areas such as:

* structure validation;
* filename validation;
* metadata validation;
* link validation;
* repository inventory;
* generation;
* quality gates;
* lifecycle checks;
* release validation.

Automation SHALL NOT eliminate required engineering ownership or review.

---

# Documentation Quality Gates

Documentation SHOULD pass appropriate quality gates before becoming canonical.

Potential gates include:

```text
Structure
Naming
Metadata
References
Completeness
Consistency
Traceability
Semantic Alignment
Repository Integrity
```

Quality gates SHOULD prevent defective documentation from becoming an official engineering reference.

---

# Repository Organization

Documentation SHOULD have predictable locations.

The framework recognizes repository areas such as:

```text
docs/
├── adr/
├── rfcs/
├── epics/
├── specs/
├── architecture/
├── plugins/
├── guides/
├── reference/
└── templates/
```

Actual repository organization may evolve through controlled migration.

---

# Review Process

Documentation review SHOULD evaluate:

* technical correctness;
* clarity;
* structure;
* terminology;
* architectural alignment;
* consistency;
* references;
* metadata;
* ownership;
* maintainability.

Review rigor SHOULD be proportional to engineering impact.

---

# Maintenance

Published documentation requires continued maintenance.

Maintenance may include:

* correcting outdated information;
* updating references;
* aligning terminology;
* reflecting implementation changes;
* updating ownership;
* correcting structural drift;
* reviewing deprecated material.

---

# Migration

Documentation migrations SHALL preserve important engineering knowledge.

Migration SHOULD include:

```text
Current State
   ↓
Migration Plan
   ↓
Controlled Transformation
   ↓
Validation
   ↓
Reference Update
   ↓
Historical Record
```

Migration SHALL NOT silently destroy relevant history.

---

# Deprecation

Deprecated documentation SHOULD remain clearly identifiable.

Where practical, deprecation records SHOULD identify:

* reason for deprecation;
* replacement document;
* migration path;
* effective lifecycle state.

Deprecated documentation MAY remain available for historical purposes.

---

# Metrics

Documentation metrics may help evaluate framework health.

Examples include:

* documentation coverage;
* structural compliance;
* metadata compliance;
* broken-reference count;
* review completion;
* stale-document count;
* validation success;
* maintenance activity.

Metrics SHALL support decisions rather than replace engineering judgment.

---

# Validation

EPIC-DOC-001 requires evidence-based validation.

Required validation areas include:

* YAML parsing;
* YAML/filesystem alignment;
* numbered-document integrity;
* duplicate-number detection;
* control-document integrity;
* empty-file detection;
* Markdown reference validation;
* placeholder validation;
* semantic consistency;
* framework-boundary validation;
* release evidence validation;
* repository quality gates.

The validation model is:

```text
Execute
   ↓
Observe
   ↓
Evaluate
   ↓
Record
```

A requirement being documented does not itself establish `PASS`.

---

# Current Release Evidence

The existing numbered release document declares:

```text
Documentation Framework
Version: 1.0.0
Status: released
Date: 2026-08-06
```

This is documentary evidence of an intended or completed framework release.

However, current normalization still requires repository-history verification before assigning authoritative values for:

```text
historical_tag
historical_commit
remote_publication_verified
```

No historical Git identity SHALL be invented.

---

# Historical Release Preservation

If repository history confirms an existing release tag or release commit, that identity SHALL remain immutable.

Structural normalization SHALL be recorded as later repository history.

The normalization SHALL NOT:

* move a historical tag;
* recreate a historical tag on a new commit;
* rewrite historical release identity;
* claim normalized files existed in an earlier release when they did not.

---

# Framework Boundaries

EPIC-DOC-001 owns documentation-framework semantics.

Related framework authority remains separated as follows:

```text
Engineering Foundation    EPIC-ENG-001
Testing                   EPIC-TST-001
Quality                   EPIC-QLT-001
Build                     EPIC-BLD-001
Release                   EPIC-REL-001
Observability             EPIC-OBS-001
Security                  EPIC-SEC-001
Operations                EPIC-OPS-001
Documentation             EPIC-DOC-001
```

EPIC-DOC-001 defines how documentation for these domains is managed.

It does not replace their authoritative domain semantics.

---

# Current Revalidation State

Current framework state:

```text
EPIC:                    EPIC-DOC-001
Framework Version:       1.0.0
Framework Status:        Baseline

Canonical Range:         00-23
Numbered Documents:      24
Control Documents:        7
Canonical Files:         31

Current Activity:         Structural Normalization and Revalidation
Repository Validation:   Validated
Final Revalidation:      Validated
```

---

# Current Normalization Requirements

Current normalization remains incomplete until:

* `00-EPIC.md` exists;
* the ten duplicate skeleton documents are removed;
* exactly 24 numbered documents remain;
* exactly seven control documents remain;
* filesystem inventory matches `EPIC.yaml`;
* `MANIFEST.md` reflects the canonical structure;
* `README.md` reflects the canonical structure;
* `EPIC-DOC-001.md` reflects current lifecycle truth;
* `CHANGELOG.md` records structural normalization;
* `Revision-History.md` records structural history;
* `VALIDATION.md` records current evidence;
* historical release evidence is verified;
* repository quality gates pass;
* final repository state is clean.

---

# Validation Target

The target normalized repository contract is:

```text
Canonical Range:       00-23
Numbered Documents:    24
Control Documents:      7
Canonical Files:       31
Duplicate Numbers:      0
Empty Canonical Files:  0
```

---

# Quality Gates

Current repository validation SHALL include:

```text
ruff check .
mypy src
pytest -q
git diff --check
```

Actual results SHALL be recorded by `VALIDATION.md`.

---

# Navigation

For framework definition, start with:

```text
00-EPIC.md
```

For introductory context:

```text
01-Introduction.md
02-Documentation-Vision.md
```

For architecture and standards:

```text
03-Documentation-Architecture.md
04-Documentation-Standards.md
```

For lifecycle, templates, metadata, and versioning:

```text
05-Documentation-Lifecycle.md
06-Documentation-Templates.md
07-Documentation-Metadata.md
08-Documentation-Versioning.md
```

For the developed framework domains:

```text
09-Documentation-Lifecycle.md
10-Documentation-Governance.md
11-Documentation-Templates.md
12-Documentation-Automation.md
13-Documentation-Quality-Gates.md
14-Documentation-Repository-Organization.md
15-Documentation-Review-Process.md
16-Documentation-Maintenance.md
17-Documentation-Migration-Strategy.md
18-Documentation-Deprecation-Policy.md
19-Documentation-Metrics.md
```

For closure and release:

```text
20-Documentation-Framework-Validation.md
21-Documentation-Framework-Summary.md
22-Documentation-Framework-Release.md
23-Documentation-Framework-Implementation-Checklist.md
```

---

# Definition of Done

EPIC-DOC-001 reaches validated closure when:

```text
Canonical Structure             PASS
Numbering Integrity             PASS
Duplicate Removal               PASS
Control Document Alignment      PASS
YAML Contract                   PASS
Filesystem Contract             PASS
Manifest Synchronization        PASS
Reference Validation            PASS
Semantic Validation             PASS
Historical Release Validation   PASS
Repository Quality Gates        PASS
Remote Verification             PASS
Final Working Tree              CLEAN
```

Until these conditions are supported by current repository evidence:

```text
Repository Validation: Validated
Final Revalidation:    Validated
```

---

# Summary

EPIC-DOC-001 establishes the canonical FamilyOS Documentation Framework.

It governs documentation architecture, standards, lifecycle, metadata, versioning, templates, governance, automation, quality, repository organization, review, maintenance, migration, deprecation, metrics, validation, and release.

The current normalization converts the previously mixed documentation structure into a deterministic canonical structure of:

```text
24 numbered documents
7 control documents
31 canonical files
```

while preserving substantive framework content and requiring explicit verification of historical release evidence before final closure.
