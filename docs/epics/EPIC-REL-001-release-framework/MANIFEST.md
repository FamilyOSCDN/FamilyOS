# Release Framework

# MANIFEST

## Overview

This manifest defines the canonical document inventory, normative hierarchy, ownership model, validation expectations, and completion rules for **EPIC-REL-001 — Release Framework**.

The manifest is the authoritative reference for determining which artifacts belong to the Release Framework baseline.

The governing principle is:

> The Release Framework is complete only when its canonical inventory exists, its required artifacts are substantive, and its normative relationships are internally consistent.

---

# EPIC Identity

```text
EPIC ID: EPIC-REL-001
Title: Release Framework
Domain: Engineering Platform
Type: Foundation Framework
Status: Complete
```

---

# Canonical Location

The Release Framework is maintained under:

```text
docs/epics/EPIC-REL-001-release-framework/
```

All canonical framework artifacts must exist in this directory unless explicitly governed otherwise.

---

# Manifest Authority

This file is the authoritative inventory for EPIC-REL-001.

When repository state and informal references disagree, the canonical manifest must be reviewed and corrected before the framework is considered valid.

The manifest must not reference:

* deleted files;
* obsolete filenames;
* duplicate canonical documents;
* temporary working files;
* accidental artifacts.

---

# Normative Hierarchy

The Release Framework follows the following normative hierarchy:

```text
FamilyOS Engineering Governance
        |
        v
Applicable ADRs and RFCs
        |
        v
EPIC-REL-001
        |
        v
00-EPIC.md
        |
        v
Numbered Release Framework Documents
        |
        v
Supporting Governance and Metadata Artifacts
```

Higher-level architectural decisions take precedence over conflicting lower-level documentation.

---

# Canonical Numbered Documents

The canonical numbered document set is:

```text
00-EPIC.md
01-Context.md
02-Vision.md
03-Release-Principles.md
04-Release-Architecture.md
05-Release-Lifecycle.md
06-Versioning-Strategy.md
07-Release-Types-and-Channels.md
08-Release-Planning.md
09-Release-Readiness.md
10-Release-Candidates.md
11-Artifacts-and-Provenance.md
12-Release-Validation.md
13-Release-Automation.md
14-CI-CD-Integration.md
15-Changelog-and-Release-Notes.md
16-Tagging-and-Repository-State.md
17-Publishing-and-Distribution.md
18-Rollback-and-Recovery.md
19-Release-Security.md
20-Release-Observability.md
21-Release-Governance.md
22-Release-Compliance.md
23-Release-Metrics.md
24-Release-Risk-Management.md
25-Framework-Lifecycle.md
26-Roadmap.md
27-References.md
28-Validation.md
29-Summary.md
30-Release.md
31-Implementation-Checklist.md
```

These documents define the core normative Release Framework.

---

# Supporting Canonical Artifacts

The Release Framework also includes the following supporting artifacts:

```text
EPIC-REL-001.md
README.md
EPIC.yaml
MANIFEST.md
CHANGELOG.md
VALIDATION.md
Revision-History.md
```

These files provide navigation, metadata, validation state, lifecycle history, and release evidence.

---

# Canonical Inventory

The complete expected canonical inventory is therefore:

```text
00-EPIC.md
01-Context.md
02-Vision.md
03-Release-Principles.md
04-Release-Architecture.md
05-Release-Lifecycle.md
06-Versioning-Strategy.md
07-Release-Types-and-Channels.md
08-Release-Planning.md
09-Release-Readiness.md
10-Release-Candidates.md
11-Artifacts-and-Provenance.md
12-Release-Validation.md
13-Release-Automation.md
14-CI-CD-Integration.md
15-Changelog-and-Release-Notes.md
16-Tagging-and-Repository-State.md
17-Publishing-and-Distribution.md
18-Rollback-and-Recovery.md
19-Release-Security.md
20-Release-Observability.md
21-Release-Governance.md
22-Release-Compliance.md
23-Release-Metrics.md
24-Release-Risk-Management.md
25-Framework-Lifecycle.md
26-Roadmap.md
27-References.md
28-Validation.md
29-Summary.md
30-Release.md
31-Implementation-Checklist.md
EPIC-REL-001.md
README.md
EPIC.yaml
MANIFEST.md
CHANGELOG.md
VALIDATION.md
Revision-History.md
```

---

# Inventory Count

The expected inventory contains:

```text
Numbered documents: 32
Supporting artifacts: 7
Total canonical artifacts: 39
```

Any deviation must be investigated.

A different total may be valid only if this manifest is intentionally updated as part of a governed framework change.

---

# Document Responsibilities

## 00-EPIC.md

Defines the core EPIC purpose, scope, objectives, and framework foundation.

## 01-Context.md

Defines the engineering and operational context that motivates the Release Framework.

## 02-Vision.md

Defines the target state and long-term release engineering vision.

## 03-Release-Principles.md

Defines the fundamental release principles that govern all later documents.

## 04-Release-Architecture.md

Defines the architectural position and major components of the Release Framework.

## 05-Release-Lifecycle.md

Defines the canonical end-to-end release lifecycle.

## 06-Versioning-Strategy.md

Defines the canonical versioning model, release identifiers, pre-release semantics, and immutable published version expectations.

## 07-Release-Types-and-Channels.md

Defines supported release types, release profiles, channels, and their governance expectations.

## 08-Release-Planning.md

Defines release planning responsibilities, scope definition, dependencies, sequencing, evidence expectations, and release preparation.

## 09-Release-Readiness.md

Defines the conditions and evidence required to determine whether a release is ready to progress.

## 10-Release-Candidates.md

Defines release candidate creation, identification, validation, replacement, promotion, and supersession semantics.

## 11-Artifacts-and-Provenance.md

Defines release artifact identity, integrity, provenance, traceability, and relationships with the Build Framework.

## 12-Release-Validation.md

Defines the validation model, required evidence, validation domains, blocking findings, and release validation outcomes.

## 13-Release-Automation.md

Defines release automation principles, automation boundaries, policy enforcement, and progressive automation maturity.

## 14-CI-CD-Integration.md

Defines how the Release Framework integrates with continuous integration and continuous delivery workflows without binding FamilyOS to a specific provider.

## 15-Changelog-and-Release-Notes.md

Defines changelog governance, release-note requirements, release communication records, and historical release traceability.

## 16-Tagging-and-Repository-State.md

Defines canonical Git tagging, repository-state requirements, immutable release references, and repository verification expectations.

## 17-Publishing-and-Distribution.md

Defines controlled release publication, distribution, publication verification, and partial-failure handling.

## 18-Rollback-and-Recovery.md

Defines rollback, forward recovery, restored-state validation, and recovery evidence expectations.

## 19-Release-Security.md

Defines security requirements for release authority, credentials, artifacts, provenance, publication, and release integrity.

## 20-Release-Observability.md

Defines release-aware observability, release event visibility, publication monitoring, and operational evidence.

## 21-Release-Governance.md

Defines release ownership, authority, approval, exception handling, escalation, and governance responsibilities.

## 22-Release-Compliance.md

Defines release compliance controls, evidence requirements, exceptions, and compliance governance.

## 23-Release-Metrics.md

Defines release performance, reliability, recovery, quality, and maturity metrics.

## 24-Release-Risk-Management.md

Defines release risk identification, assessment, mitigation, acceptance, escalation, and residual-risk governance.

## 25-Framework-Lifecycle.md

Defines the lifecycle, maintenance, evolution, compatibility, governance, and retirement model of the Release Framework itself.

## 26-Roadmap.md

Defines the planned evolution of the Release Framework.

## 27-References.md

Defines references to related EPICs, ADRs, RFCs, standards, and supporting architecture.

## 28-Validation.md

Defines the formal validation model for EPIC-REL-001.

## 29-Summary.md

Provides a concise summary of the complete framework.

## 30-Release.md

Defines the release procedure for the framework itself.

## 31-Implementation-Checklist.md

Provides the implementation and adoption checklist for the Release Framework.

---

# Supporting Artifact Responsibilities

## EPIC-REL-001.md

Provides the root EPIC-level summary and official foundation statement.

## README.md

Provides entry-point navigation and framework orientation.

## EPIC.yaml

Provides machine-readable EPIC metadata.

## MANIFEST.md

Defines the canonical inventory and normative structure.

## CHANGELOG.md

Tracks framework changes by version.

## VALIDATION.md

Records the current validation result and validation evidence.

## Revision-History.md

Tracks the chronological evolution of the framework documentation.

---

# Required Document State

Every canonical artifact must satisfy the following minimum conditions:

```text
exists == true
empty == false
canonical_name == true
repository_tracked == true
```

For normative numbered documents:

```text
substantive_content == true
required_structure_present == true
terminology_consistent == true
```

A file that exists but contains only a placeholder does not satisfy completion requirements.

---

# Numbering Rules

Numbered documents must:

* use two-digit numeric prefixes;
* have unique numeric identifiers;
* appear once in the canonical inventory;
* preserve logical ordering;
* use stable names after framework release unless changed through governance.

Example:

```text
18-Rollback-and-Recovery.md
```

is valid.

Conflicting files such as:

```text
18-Rollback.md
18-Recovery.md
```

would violate canonical numbering unless the manifest explicitly defines both under different numbers.

---

# Duplicate Number Rule

There must be no duplicate numbered document identifiers.

The following condition must hold:

```text
count(unique numeric prefixes)
==
count(numbered documents)
```

Duplicate numbering is a blocking structural finding.

---

# Unexpected Files

Unexpected files in the EPIC directory must be reviewed.

Examples include:

* editor backup files;
* temporary shell outputs;
* accidentally created words;
* duplicate drafts;
* exported copies;
* stale renamed documents.

Unexpected files are not automatically invalid, but they must not be mistaken for canonical framework artifacts.

---

# Empty Files

Canonical files must not be empty.

Validation should detect empty files using repository tooling.

Any required empty file results in:

```text
Framework Validation = FAIL
```

until corrected.

---

# Normative Content Model

The core numbered documents collectively define the normative Release Framework.

Normative requirements should be expressed using clear language such as:

```text
must
must not
required
prohibited
shall
```

Recommendations may use:

```text
should
may
recommended
where practical
```

Ambiguous normative requirements should be corrected before release.

---

# Cross-Document Consistency

The canonical inventory must maintain a coherent model for:

* release identity;
* release lifecycle;
* release states;
* release readiness;
* release gates;
* approval;
* deployment;
* rollback;
* recovery;
* observability;
* compliance;
* metrics;
* risk management.

Contradictory definitions are blocking findings when they affect normative release behavior.

---

# Framework Relationships

EPIC-REL-001 depends on and integrates with:

```text
EPIC-ENG-001 — Engineering Foundation
EPIC-DOC-001 — Documentation Framework
EPIC-TST-001 — Testing Framework
EPIC-QLT-001 — Quality Framework
EPIC-BLD-001 — Build Framework
EPIC-PLUGIN-002 — Plugin Compliance Framework
```

Additional security, architecture, ADR, and RFC relationships are maintained through the references and EPIC metadata.

---

# Responsibility Boundaries

The Release Framework must consume rather than duplicate foundational capabilities.

## Build Framework

Owns:

* build architecture;
* reproducibility;
* artifact creation;
* provenance.

Release Framework owns:

* release use;
* promotion;
* authorization;
* production identity.

## Testing Framework

Owns testing architecture and execution semantics.

Release Framework consumes test evidence.

## Quality Framework

Owns quality principles and quality gates.

Release Framework consumes quality outcomes for release decisions.

## Plugin Compliance Framework

Owns plugin structural and compliance validation.

Release Framework owns release authorization of a specific plugin version.

---

# Validation Requirements

The manifest must be validated against repository state.

Validation includes:

```text
[ ] All canonical files exist
[ ] No canonical files are empty
[ ] Numbered document count is correct
[ ] Supporting artifact count is correct
[ ] No duplicate numeric prefixes exist
[ ] No required canonical file is missing
[ ] Filenames match this manifest
[ ] Metadata references valid files
[ ] Cross-document structure is coherent
```

---

# Recommended Structural Validation

A structural validation may include:

```bash
EPIC_DIR="docs/epics/EPIC-REL-001-release-framework"

printf '\n=== RELEASE FRAMEWORK STRUCTURE ===\n'
tree "$EPIC_DIR"

printf '\n=== FILE SIZES ===\n'
find "$EPIC_DIR" -maxdepth 1 -type f \
  -exec wc -c {} \; | sort -k2

printf '\n=== EMPTY FILES ===\n'
find "$EPIC_DIR" -maxdepth 1 -type f -empty -print | sort

printf '\n=== NUMBERED DOCUMENTS ===\n'
find "$EPIC_DIR" -maxdepth 1 -type f \
  -name '[0-9][0-9]-*.md' \
  -exec basename {} \; | sort
```

These checks provide basic structural evidence.

---

# Duplicate Number Validation

Duplicate numeric prefixes may be checked conceptually through:

```bash
find "$EPIC_DIR" -maxdepth 1 -type f \
  -name '[0-9][0-9]-*.md' \
  -exec basename {} \; \
  | cut -d- -f1 \
  | sort \
  | uniq -d
```

Expected output:

```text
<no output>
```

Any output indicates a duplicate numbered document.

---

# Manifest Validation

The manifest itself must be reviewed whenever:

* a canonical document is added;
* a canonical document is removed;
* a document is renamed;
* numbering changes;
* supporting metadata changes;
* framework structure changes.

Repository changes and manifest changes must remain synchronized.

---

# Framework Completion Requirements

EPIC-REL-001 may be considered structurally complete when:

```text
canonical_inventory_complete == true
required_files_non_empty == true
duplicate_numbers == 0
blocking_structure_findings == 0
```

It may be considered fully complete only when formal framework validation also succeeds.

---

# Completion Does Not Mean Automation Completion

The Release Framework defines both current normative rules and future platform evolution.

Therefore, framework completion does not require every roadmap capability to already exist.

Capabilities such as:

* progressive delivery;
* advanced policy-as-code;
* automated rollback;
* predictive release risk;
* release intelligence;

may remain roadmap items.

The framework must nevertheless define sufficient principles to guide their future implementation.

---

# Ownership

The Release Framework belongs to the FamilyOS Engineering Platform.

Framework governance is responsible for:

* maintaining the canonical inventory;
* reviewing normative changes;
* resolving structural conflicts;
* maintaining release metadata;
* ensuring compatibility with adjacent frameworks;
* approving framework evolution.

---

# Change Governance

Changes to the canonical inventory must be intentional.

A change that:

* adds a normative document;
* removes a normative document;
* changes numbering;
* changes responsibility boundaries;
* changes framework hierarchy;

must be reviewed as a framework-level change.

Material architectural changes may require an ADR.

---

# Versioning

The manifest is versioned together with the Release Framework.

Released versions of EPIC-REL-001 should preserve historical manifest state through Git history and immutable release tags.

A future framework version may update this inventory.

Such changes must be reflected in:

* CHANGELOG.md;
* Revision-History.md;
* EPIC metadata;
* validation evidence.

---

# Release Baseline

At framework release, this manifest becomes part of the immutable EPIC-REL-001 baseline.

The baseline must correspond to:

```text
Canonical Inventory
       |
       v
Validated Repository State
       |
       v
Release Commit
       |
       v
Release Tag
```

The tag establishes the historical authority of the manifest at that version.

---

# Validation Status

The final validation result for the current framework version is recorded in:

```text
VALIDATION.md
```

The manifest defines what must exist.

`VALIDATION.md` records whether those requirements were successfully verified.

---

# Manifest Acceptance Criteria

This manifest is considered valid when:

```text
inventory_matches_repository == true
all_required_files_present == true
all_required_files_non_empty == true
numbering_unique == true
framework_relationships_consistent == true
validation_requirements_defined == true
```

---

# Anti-Patterns

The following practices are prohibited or strongly discouraged.

## Untracked Canonical Documents

Treating documents as part of the official framework without listing them in the manifest.

## Manifest Drift

Allowing the inventory to differ from repository reality.

## Duplicate Numbering

Maintaining multiple canonical files with the same numeric identifier.

## Placeholder Completion

Counting empty or placeholder documents as completed deliverables.

## Hidden Structural Changes

Renaming or removing canonical documents without updating governance artifacts.

## Inventory by Memory

Relying on informal knowledge instead of the canonical manifest.

## Supporting Artifact Ambiguity

Treating metadata and validation artifacts as optional when they are required by the framework.

---

# Required Outcomes

This manifest must ensure that:

* the canonical Release Framework inventory is explicit;
* every canonical artifact has a defined role;
* numbered documents remain uniquely identified;
* supporting artifacts remain part of the release baseline;
* repository state can be validated mechanically;
* structural drift is detectable;
* framework ownership is clear;
* framework changes remain governed;
* validation can determine whether EPIC-REL-001 is structurally complete.

---

# Final Manifest Principle

The Release Framework must have one authoritative inventory.

Its structure must never depend on assumptions about which files are important.

The final principle is:

> EPIC-REL-001 is structurally authoritative only when its canonical documents, metadata artifacts, numbering, and governance relationships are explicitly defined in one manifest and verified against the actual repository state.

`MANIFEST.md` therefore provides the structural contract for the complete FamilyOS Release Framework.
