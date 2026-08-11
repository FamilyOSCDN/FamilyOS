# EPIC-REL-001 — Release Framework Manifest

## Metadata

| Field      | Value                 |
| ---------- | --------------------- |
| Identifier | EPIC-REL-001          |
| Title      | Release Framework     |
| Version    | 4.8.0                 |
| Status     | Completed             |
| Type       | Engineering Framework |
| Category   | Release               |
| Domain     | Engineering Platform  |
| Owner      | FamilyOS Engineering  |
| Language   | English               |
| Repository | FamilyOS              |

---

# 1. Purpose

This manifest defines the authoritative canonical document inventory for:

```text
EPIC-REL-001 — Release Framework
```

It establishes:

* the canonical numbered document set;
* the canonical control document set;
* the expected filesystem inventory;
* the canonical numbering range;
* the structural integrity requirements;
* the relationship between the manifest and `EPIC.yaml`;
* the historical publication identity;
* the current post-release revalidation state.

The manifest is a structural contract.

It SHALL describe the files that constitute the canonical EPIC.

It SHALL remain synchronized with:

```text
EPIC.yaml
```

and with the physical repository state.

---

# 2. Canonical Structure

EPIC-REL-001 contains two document classes:

```text
Numbered Framework Documents
        +
Control Documents
```

The numbered framework documentation consists of exactly:

```text
00 → 31
```

representing:

```text
32 numbered documents
```

The EPIC additionally contains:

```text
7 control documents
```

Therefore:

```text
32 numbered documents
+
7 control documents
=
39 canonical files
```

The canonical structure is:

```text
Canonical Range:       00 → 31
Numbered Documents:    32
Control Documents:      7
Canonical Files:       39
```

---

# 3. Numbered Document Inventory

| No. | Document                             | Purpose                                                                                                                     |
| --: | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
|  00 | `00-EPIC.md`                         | Defines the EPIC identity, scope, objectives, architecture, dependencies, governance expectations, and completion model.    |
|  01 | `01-Context.md`                      | Defines the engineering context, release challenges, constraints, motivations, and need for a unified Release Framework.    |
|  02 | `02-Vision.md`                       | Defines the long-term release vision and desired controlled publication state for FamilyOS.                                 |
|  03 | `03-Release-Principles.md`           | Establishes the foundational principles governing releases across FamilyOS.                                                 |
|  04 | `04-Release-Architecture.md`         | Defines the canonical Release Framework architecture, responsibilities, boundaries, flows, and integration model.           |
|  05 | `05-Release-Lifecycle.md`            | Defines canonical release lifecycle states, transitions, controls, evidence, and lifecycle responsibilities.                |
|  06 | `06-Versioning-Strategy.md`          | Defines version identity, compatibility semantics, version progression, and version governance.                             |
|  07 | `07-Release-Types-and-Channels.md`   | Defines canonical release types, distribution channels, stability expectations, and promotion semantics.                    |
|  08 | `08-Release-Planning.md`             | Defines release planning requirements, scope control, dependencies, risks, scheduling, and preparation.                     |
|  09 | `09-Release-Readiness.md`            | Defines readiness requirements and evidence required before release progression.                                            |
|  10 | `10-Release-Candidates.md`           | Defines release candidate identity, lifecycle, validation, promotion, rejection, and replacement semantics.                 |
|  11 | `11-Artifacts-and-Provenance.md`     | Defines release artifact identity, integrity, provenance, traceability, immutability, and evidence requirements.            |
|  12 | `12-Release-Validation.md`           | Defines validation requirements used to determine whether a release may progress toward publication.                        |
|  13 | `13-Release-Automation.md`           | Defines deterministic release automation, execution boundaries, evidence, failure handling, and control requirements.       |
|  14 | `14-CI-CD-Integration.md`            | Defines integration between the Release Framework and CI/CD execution systems.                                              |
|  15 | `15-Changelog-and-Release-Notes.md`  | Defines changelog and release-note generation, structure, traceability, ownership, and publication expectations.            |
|  16 | `16-Tagging-and-Repository-State.md` | Defines canonical Git tagging, repository-state requirements, release commit identity, and publication evidence.            |
|  17 | `17-Publishing-and-Distribution.md`  | Defines controlled publication, distribution, promotion, verification, and publication-state requirements.                  |
|  18 | `18-Rollback-and-Recovery.md`        | Defines rollback, recovery, restoration, and failure-response requirements.                                                 |
|  19 | `19-Release-Security.md`             | Defines security expectations applicable to release preparation, artifacts, credentials, automation, and publication.       |
|  20 | `20-Release-Observability.md`        | Defines observability of release state, execution, failures, publication, history, and significant release signals.         |
|  21 | `21-Release-Governance.md`           | Defines authority, ownership, approval, exception, escalation, and release governance responsibilities.                     |
|  22 | `22-Release-Compliance.md`           | Defines release compliance evaluation, traceability, evidence, exceptions, and governance.                                  |
|  23 | `23-Release-Metrics.md`              | Defines release metrics, interpretation, governance, trend analysis, and responsible use.                                   |
|  24 | `24-Release-Risk-Management.md`      | Defines release risk identification, evaluation, ownership, mitigation, monitoring, and acceptance.                         |
|  25 | `25-Framework-Lifecycle.md`          | Defines adoption, operation, evolution, versioning, migration, deprecation, and retirement of the Release Framework.        |
|  26 | `26-Roadmap.md`                      | Defines progressive implementation, automation, integration, adoption, enforcement, and long-term evolution.                |
|  27 | `27-References.md`                   | Identifies authoritative FamilyOS artifacts and external references that constrain, support, or complement the framework.   |
|  28 | `28-Validation.md`                   | Defines structural, semantic, architectural, operational, and release validation of the framework itself.                   |
|  29 | `29-Summary.md`                      | Consolidates the framework's principal concepts, responsibilities, boundaries, outcomes, and engineering value.             |
|  30 | `30-Release.md`                      | Defines framework release readiness, publication, versioning, validation, governance, and historical release requirements.  |
|  31 | `31-Implementation-Checklist.md`     | Defines the implementation path from normative Release Framework documentation to executable FamilyOS release capabilities. |

---

# 4. Control Document Inventory

The canonical control documents are:

| Document              | Purpose                                                                                                                                              |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `EPIC-REL-001.md`     | Concise EPIC-level definition, scope, architecture, objectives, dependencies, risks, lifecycle, and final state.                                     |
| `EPIC.yaml`           | Machine-readable EPIC metadata, canonical inventory, dependencies, validation requirements, baseline state, publication identity, and closure state. |
| `README.md`           | Human-readable entry point and navigation guide for the Release Framework.                                                                           |
| `MANIFEST.md`         | Authoritative inventory and structural contract for the complete EPIC documentation set.                                                             |
| `CHANGELOG.md`        | Records significant Release Framework changes and publication history.                                                                               |
| `VALIDATION.md`       | Records actual validation execution, evidence, results, repository verification, and final revalidation state.                                       |
| `Revision-History.md` | Maintains the historical record of published Release Framework revisions and post-release normalization.                                             |

Exactly seven control documents SHALL exist.

---

# 5. Canonical File Inventory

The complete canonical inventory is:

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
EPIC.yaml
README.md
MANIFEST.md
CHANGELOG.md
VALIDATION.md
Revision-History.md
```

Inventory totals:

```text
Numbered Documents: 32
Control Documents:   7
Canonical Files:    39
```

---

# 6. Structural Requirements

The canonical numbered documentation SHALL satisfy all of the following:

```text
Exactly 32 numbered documents
Sequential numbering from 00 through 31
Exactly one document for each number
No duplicate document numbers
No missing document numbers
No unexpected numbered documents
No empty required documents
Canonical file names match document responsibilities
```

The control documentation SHALL satisfy:

```text
Exactly 7 control documents
No required control document missing
No unexpected control document
No empty required control document
Control documents synchronized with canonical state
```

A structural deviation SHALL be treated as a documentation integrity finding until resolved or explicitly governed.

---

# 7. Filesystem Contract

The physical EPIC directory SHALL contain exactly:

```text
39 canonical files
```

The declared inventory in `EPIC.yaml` SHALL match the physical filesystem exactly.

The required relationship is:

```text
declared_files == actual_files
```

Therefore:

```text
missing_files == []
unexpected_files == []
```

The manifest SHALL NOT declare a file that does not physically exist.

The filesystem SHALL NOT contain an undeclared canonical EPIC file.

---

# 8. Numbering Contract

The canonical numbered range is:

```text
00-31
```

The expected sequence is:

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
24
25
26
27
28
29
30
31
```

Each identifier SHALL occur exactly once.

The first numbered document SHALL be:

```text
00-EPIC.md
```

The final numbered document SHALL be:

```text
31-Implementation-Checklist.md
```

---

# 9. EPIC.yaml Synchronization

`EPIC.yaml` is the machine-readable structural authority.

Its canonical structure SHALL identify:

```yaml
structure:
  numbered_documents: 32
  canonical_document_range: "00-31"
  control_documents: 7
  canonical_files: 39
```

The number of entries under:

```text
deliverables
```

SHALL equal:

```text
39
```

The machine-readable and human-readable inventories SHALL remain synchronized.

---

# 10. Framework Identity

The canonical framework identity is:

```text
Identifier: EPIC-REL-001
Title: Release Framework
Framework Version: 4.8.0
Status: Completed
```

Version `4.8.0` is retained because it is the historically published framework version.

Post-release documentation normalization SHALL NOT rewrite the historical framework identity merely to conform to another EPIC's versioning pattern.

---

# 11. Historical Publication

EPIC-REL-001 has already been historically published.

The authoritative historical publication identity is:

```text
Historical Tag:
v4.8.0-release-framework

Historical Publication Commit:
306338d7ca3df2c1d4d9b74247a837aa01deb637

Publication Status:
Published
```

The historical tag is an annotated Git tag.

The historical publication SHALL be treated as immutable.

Post-release documentation corrections SHALL be recorded in later commits rather than moving, replacing, recreating, or rewriting the historical tag.

---

# 12. Historical Tag Policy

The historical tag:

```text
v4.8.0-release-framework
```

SHALL remain attached to its original publication commit:

```text
306338d7ca3df2c1d4d9b74247a837aa01deb637
```

The following operations are prohibited during revalidation:

```text
moving the historical tag
deleting and recreating the historical tag
force-updating the historical tag
changing the tag target
rewriting the historical publication commit
claiming a post-release correction commit as the original publication
```

Current corrections SHALL preserve historical truth.

---

# 13. Publication Evidence

Historical publication evidence SHALL distinguish between:

```text
tag object identity
tag target commit
remote tag publication
current branch state
post-release correction commits
```

For annotated tags, the Git reference for the tag object MAY differ from the dereferenced commit identity.

The authoritative historical publication commit is the dereferenced tag target.

For EPIC-REL-001:

```text
v4.8.0-release-framework^{}
```

resolves to:

```text
306338d7ca3df2c1d4d9b74247a837aa01deb637
```

---

# 14. Current Repository Relationship

The current repository HEAD MAY be newer than the historical publication commit.

This is expected.

Post-release corrections and normalization SHALL occur through ordinary forward Git history.

The required relationship is:

```text
Historical Publication Commit
        ↓
Later Repository History
        ↓
Post-Release Corrections
```

The framework's historical publication identity SHALL remain preserved while its current documentation state becomes more accurate.

---

# 15. Post-Release Revalidation

The current activity is:

```text
Post-Release Revalidation
```

Revalidation exists to confirm that the current repository representation of EPIC-REL-001 is:

* structurally complete;
* machine-readable;
* internally consistent;
* historically accurate;
* synchronized across control documents;
* compatible with current repository quality gates;
* consistent with the published historical release.

Revalidation does not create a new historical release.

---

# 16. Revalidation State Model

During revalidation, the framework SHALL distinguish historical publication state from current validation state.

Historical publication:

```text
publication_status: published
historical_tag_immutable: true
remote_publication_verified: true
```

Current repository revalidation initially remains:

```text
repository_validation_status: pending_revalidation
final_validation_status: pending_revalidation
```

These current validation states SHALL be converted to:

```text
repository_validation_status: validated
final_validation_status: validated
```

only after corresponding validation has actually executed successfully.

---

# 17. Evidence Rule

Validation claims SHALL be evidence-based.

The following rule applies:

```text
No execution
=
No PASS claim
```

Only evidence from actual execution SHALL be used to convert pending engineering checks into PASS results.

Documentation SHALL NOT predict successful validation.

Documentation SHALL record successful validation only after the relevant command or verification has actually succeeded.

---

# 18. Required Structural Validation

Current revalidation SHALL verify at minimum:

```text
YAML parse
YAML contract
deliverable count
filesystem inventory
numbered document count
numbering sequence
control document count
empty file check
manifest synchronization
reference integrity
state consistency
historical tag integrity
```

Expected structural values are:

```text
Deliverables:         39
Numbered Documents:   32
Control Documents:     7
Canonical Files:      39
Canonical Range:      00-31
```

---

# 19. Required Semantic Validation

Revalidation SHALL verify consistency across the principal Release Framework concepts, including:

* release principles;
* release architecture;
* release lifecycle;
* versioning;
* release types;
* channels;
* planning;
* readiness;
* release candidates;
* artifact identity;
* provenance;
* validation;
* automation;
* CI/CD integration;
* tagging;
* repository state;
* publishing;
* distribution;
* rollback;
* recovery;
* security;
* observability;
* governance;
* compliance;
* metrics;
* risk management;
* framework lifecycle.

Semantic validation SHALL also confirm explicit ownership boundaries with specialized FamilyOS engineering frameworks.

---

# 20. Framework Boundaries

EPIC-REL-001 owns release engineering semantics.

It SHALL integrate with but SHALL NOT replace specialized framework responsibilities.

Important boundaries include:

```text
Engineering Foundation
        ↓
Testing Framework
        ↓
Quality Framework
        ↓
Build Framework
        ↓
Release Framework
```

Additional integration exists with:

```text
Security Framework
Operations Framework
Plugin Framework
Documentation Framework
```

Release may consume evidence and artifacts produced by these frameworks without absorbing their complete responsibilities.

---

# 21. Build / Release Boundary

The Build Framework and Release Framework SHALL remain distinct.

The Build Framework primarily owns:

```text
build execution
build inputs
dependency preparation
build environments
artifact creation
build reproducibility
build validation
```

The Release Framework primarily owns:

```text
release readiness
release candidates
release identity
versioning
promotion
tagging
publication
distribution
release rollback
release governance
release evidence
```

A build artifact does not become a released artifact merely because its build succeeded.

---

# 22. Testing / Release Boundary

The Testing Framework owns canonical testing strategy and test execution semantics.

The Release Framework consumes test evidence as release-readiness input.

Release SHALL NOT redefine the Testing Framework.

A release decision MAY require successful test evidence without owning the detailed design of the tests themselves.

---

# 23. Quality / Release Boundary

The Quality Framework owns general quality rules, evidence, metrics, assessments, risk, and quality-gate semantics.

The Release Framework applies appropriate quality evidence to release decisions.

Release-specific gates SHALL remain consistent with the canonical Quality Framework.

---

# 24. Security / Release Boundary

Release security concerns include:

* release credentials;
* publication authority;
* artifact integrity;
* provenance;
* signing where applicable;
* protected repository operations;
* secret handling;
* supply-chain assurance;
* publication authorization.

The Release Framework SHALL define release-specific security requirements while delegating general security architecture to the Security Framework.

---

# 25. Operations / Release Boundary

The Release Framework controls publication and distribution.

The Operations Framework controls operational runtime management.

Publication does not automatically imply deployment.

Deployment does not automatically imply release publication.

Where workflows connect release and operations, the boundary SHALL remain explicit and auditable.

---

# 26. Control Document Synchronization

The seven control documents SHALL converge on the same canonical facts.

At minimum they SHALL agree on:

```text
EPIC identifier
framework title
framework version
completion state
canonical range
numbered document count
control document count
canonical file count
historical tag
historical publication state
current revalidation state
```

Contradictory active states SHALL be corrected.

Historical statements MAY retain earlier lifecycle states when clearly identified as historical context.

---

# 27. State Consistency

The active canonical framework state is:

```text
Status: Completed
Framework Version: 4.8.0
Historical Publication: Published
```

Active control-document statements SHALL NOT incorrectly claim:

```text
status: in-progress
publication_status: pending
official tag pending
release commit pending
remote publication pending
epic closure pending
```

when those operations have already occurred historically.

Historical descriptions of earlier states MAY remain when clearly contextualized as historical evidence rather than current state.

---

# 28. Validation Authority

This manifest defines structural expectations.

It does not independently prove successful validation.

Actual execution evidence belongs primarily in:

```text
VALIDATION.md
```

Therefore:

```text
MANIFEST.md
=
structural authority

VALIDATION.md
=
execution evidence authority
```

The two documents SHALL remain consistent but serve different purposes.

---

# 29. Repository Quality Gates

Final repository revalidation SHALL include actual execution of the applicable repository quality gates.

At minimum:

```text
ruff check .
mypy src
pytest -q
git diff --check
```

A successful result MAY be recorded only after actual execution.

The manifest does not predeclare those commands as PASS.

---

# 30. Repository Cleanliness

Final revalidation SHALL verify repository state.

Before the corrective commit, expected changes MAY exist for the EPIC control documents being normalized.

After the corrective commit and publication to the authoritative branch, final verification SHOULD establish:

```text
working tree clean
local branch synchronized
remote branch synchronized
historical tag unchanged
```

---

# 31. Revalidation Commit Policy

Post-release corrections SHALL use a new forward commit.

The historical publication commit SHALL remain unchanged.

A suitable correction history has the form:

```text
306338d7
Historical EPIC-REL-001 publication
        ↓
later repository development
        ↓
post-release normalization commit
```

The correction commit SHALL NOT be represented as the historical release commit.

---

# 32. Remote Verification

Remote verification SHALL distinguish:

```text
current branch publication
historical tag publication
```

Both SHOULD be verified independently.

For the historical tag, verification SHALL confirm that the remote dereferenced tag resolves to:

```text
306338d7ca3df2c1d4d9b74247a837aa01deb637
```

The current correction commit MAY have a different commit identity.

This is expected and correct.

---

# 33. Manifest Integrity Requirements

This manifest SHALL remain internally consistent.

It SHALL NOT contain:

* contradictory active lifecycle states;
* incorrect canonical counts;
* missing canonical documents;
* duplicate numbered documents;
* stale publication claims presented as current;
* invented validation evidence;
* an incorrect historical tag;
* an incorrect historical publication commit;
* claims that the historical tag should be moved.

---

# 34. Canonical Inventory Validation

The expected filesystem contract is:

```text
declared: 39
actual:   39
numbered: 32
control:   7

missing:    []
unexpected: []
```

These values SHALL be confirmed against the actual repository during revalidation.

---

# 35. Manifest Completion Conditions

Manifest synchronization is complete when:

* all 32 numbered documents are represented;
* all seven control documents are represented;
* all 39 canonical files are represented;
* numbering is `00-31`;
* `EPIC.yaml` declares the same inventory;
* the physical filesystem contains the same inventory;
* framework version is `4.8.0`;
* framework status is `completed`;
* historical publication is accurately represented;
* the historical tag is `v4.8.0-release-framework`;
* the historical publication commit is preserved;
* no active stale publication state remains in the manifest.

---

# 36. Canonical Manifest Summary

```text
EPIC:                   EPIC-REL-001
Title:                  Release Framework
Framework Version:      4.8.0
Framework Status:       Completed

Canonical Range:        00 → 31
Numbered Documents:     32
Control Documents:       7
Canonical Files:        39

Historical Publication: Published
Historical Tag:         v4.8.0-release-framework
Historical Commit:      306338d7ca3df2c1d4d9b74247a837aa01deb637
Historical Tag Policy:  Immutable

Current Activity:       Post-Release Revalidation
Repository Validation: Validated
Final Revalidation:     Validated
```

---

# 37. Final Manifest Contract

The authoritative structural contract for EPIC-REL-001 is:

```text
32 / 32 numbered documents present
7 / 7 control documents present
39 / 39 canonical files represented
Canonical range 00 → 31 complete
No missing canonical files
No unexpected canonical files
Historical publication preserved
Historical tag immutable
```

Current repository validation and final revalidation SHALL remain pending until supported by actual execution evidence.

**Manifest Structural State: COMPLETE**

**Historical Publication State: PUBLISHED**

**Current Revalidation State: VALIDATED**
