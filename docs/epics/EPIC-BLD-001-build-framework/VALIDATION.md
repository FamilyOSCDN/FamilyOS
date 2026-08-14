# EPIC-BLD-001 — Build Framework Validation

## Metadata

| Field                         | Value                     |
| ----------------------------- | ------------------------- |
| Identifier                    | EPIC-BLD-001              |
| Title                         | Build Framework           |
| Framework Version             | 1.0.0                     |
| Framework Status              | Completed                 |
| Validation Type               | Post-Release Revalidation |
| Validation Status             | Validated                 |
| Historical Publication Tag    | `v4.7.0-build-framework`  |
| Historical Publication Status | Published                 |
| Historical Tag Policy         | Immutable                 |
| Repository                    | FamilyOS                  |
| Owner                         | FamilyOS Engineering      |
| Language                      | English                   |

---

# 1. Purpose

This document records the current validation state and validation evidence for:

**EPIC-BLD-001 — Build Framework**

It is the authoritative validation evidence record for the current canonical Build Framework documentation.

The validation confirms that the framework remains:

* structurally complete;
* internally consistent at the validated structural level;
* synchronized with its canonical inventory;
* represented by valid machine-readable metadata;
* free from empty required canonical files;
* free from unresolved blocking placeholders identified by the executed checks;
* free from detected accidental word-join defects covered by the executed checks;
* supported by successful repository quality gates;
* associated with an intact immutable historical publication tag.

This document distinguishes between:

1. historical publication;
2. current canonical repository state;
3. current post-release revalidation;
4. repository quality evidence;
5. final validation outcome.

Only evidence obtained from actual execution is recorded as PASS.

---

# 2. Historical Publication

EPIC-BLD-001 version `1.0.0` was historically published under:

```text
v4.7.0-build-framework
```

Historical publication state:

```text
EPIC:                EPIC-BLD-001
Framework:           Build Framework
Framework Version:   1.0.0
Historical Tag:      v4.7.0-build-framework
Publication Status:  Published
```

The historical publication tag identifies the original release state.

Post-release normalization does not recreate, move, overwrite, or otherwise mutate that historical tag.

---

# 3. Historical Tag Integrity

The historical tag was resolved successfully.

Execution evidence:

```text
Historical Tag:
v4.7.0-build-framework

Historical Tag Commit:
1b457dd86ae4c94033fa29b96b4e6db135202171
```

Result:

```text
Historical Tag Exists: PASS
Historical Tag Integrity Baseline: PASS
```

The historical tag remains the reference for the original Build Framework publication.

Any post-release correction commit SHALL remain separate from this historical tag.

---

# 4. Revalidation Context

The current validation activity is a post-release documentation normalization and revalidation.

It does not replace the historical release.

Its purpose is to ensure that the current canonical repository representation of EPIC-BLD-001 remains structurally coherent and supported by current repository evidence.

The executed revalidation covers:

* YAML parsing;
* YAML metadata contract;
* canonical filesystem inventory;
* numbered-document inventory;
* control-document inventory;
* empty-file detection;
* placeholder detection;
* local Markdown reference integrity;
* canonical document reference integrity;
* accidental join-defect detection;
* Ruff;
* MyPy;
* Pytest;
* Git diff validation;
* historical tag existence.

---

# 5. Validation Authority

The Build Framework contains separate normative and evidentiary validation artifacts.

| Document                         | Responsibility                                                    |
| -------------------------------- | ----------------------------------------------------------------- |
| `20-Validation.md`               | Defines normative framework validation requirements.              |
| `22-Release.md`                  | Defines release readiness and publication requirements.           |
| `23-Implementation-Checklist.md` | Defines implementation and adoption activities.                   |
| `EPIC.yaml`                      | Defines machine-readable framework metadata and validation state. |
| `MANIFEST.md`                    | Defines the canonical inventory and structural contract.          |
| `VALIDATION.md`                  | Records actual validation execution and evidence.                 |

Normative requirements do not become PASS merely because they are documented.

PASS requires evidence.

---

# 6. Canonical Inventory

The canonical Build Framework inventory is:

```text
24 numbered documents
+
7 control documents
=
31 canonical files
```

Canonical numbered range:

```text
00 → 23
```

Validated structure:

```yaml
structure:
  numbered_documents: 24
  canonical_document_range: "00-23"
  control_documents: 7
  canonical_files: 31
```

Result:

```text
Canonical Inventory: PASS
```

---

# 7. Numbered Document Inventory

The canonical numbered documents are:

```text
00-EPIC.md
01-Context.md
02-Vision.md
03-Build-Principles.md
04-Build-Architecture.md
05-Build-Lifecycle.md
06-Build-Input-Requirements.md
07-Build-Inputs-and-Project-Structure.md
08-Build-Toolchain.md
09-Build-Environment-Management.md
10-Dependency-Management.md
11-Build-Configuration.md
12-Build-Philosophy.md
13-Build-Execution.md
14-Artifact-Management.md
15-Build-Validation.md
16-Build-Governance.md
17-Build-Automation-and-CI.md
18-Roadmap.md
19-References.md
20-Validation.md
21-Summary.md
22-Release.md
23-Implementation-Checklist.md
```

Validated result:

```text
Numbered Documents: 24
First Document:      00-EPIC.md
Last Document:       23-Implementation-Checklist.md
```

Result:

```text
Numbering Integrity: PASS
```

---

# 8. Control Document Inventory

The canonical control documents are:

```text
EPIC-BLD-001.md
EPIC.yaml
README.md
MANIFEST.md
CHANGELOG.md
VALIDATION.md
Revision-History.md
```

Validated result:

```text
Control Documents: 7
```

Result:

```text
Control Documents: PASS
```

---

# 9. Complete Filesystem Contract

The canonical filesystem contract requires:

```text
Declared Files:   31
Filesystem Files: 31
Missing Files:    []
Unexpected Files: []
```

Actual execution evidence:

```text
id: EPIC-BLD-001
version: 1.0.0
status: completed
deliverables: 31
actual: 31
numbered: 24
missing: []
unexpected: []
```

Result:

```text
Filesystem Contract: PASS
```

---

# 10. YAML Parse Validation

`EPIC.yaml` was parsed successfully using the repository Python environment and `yaml.safe_load`.

The earlier malformed YAML state was corrected before the successful validation execution.

Validated machine-readable identity:

```text
id: EPIC-BLD-001
version: 1.0.0
status: completed
```

Result:

```text
YAML Parse: PASS
```

---

# 11. YAML Contract Validation

The validated YAML contract reports:

```text
id: EPIC-BLD-001
version: 1.0.0
status: completed
deliverables: 31
actual: 31
numbered: 24
```

Validated structure:

```text
numbered_documents: 24
canonical_document_range: 00-23
control_documents: 7
canonical_files: 31
```

The declared deliverables and actual filesystem inventory are identical.

Result:

```text
YAML Contract: PASS
```

---

# 12. Baseline State

At the time of structural validation, the machine-readable baseline was:

```yaml
baseline:
  framework_version: 1.0.0
  documentation_status: completed
  repository_validation_status: pending_revalidation
  final_validation_status: pending_revalidation
```

This state correctly represented the framework while current validation evidence was still being accumulated.

The successful evidence recorded by this document now supports transition to:

```yaml
baseline:
  framework_version: 1.0.0
  documentation_status: completed
  repository_validation_status: validated
  final_validation_status: validated
```

---

# 13. Release Metadata

Validated release metadata:

```yaml
release:
  historical_tag: v4.7.0-build-framework
  publication_status: published
  historical_tag_immutable: true
```

Result:

```text
Release Metadata: PASS
```

---

# 14. Empty File Validation

The executed empty-file check produced no required empty canonical files.

Result:

```text
Empty Required Files: 0
Empty File Validation: PASS
```

---

# 15. Placeholder Validation

A repository-level documentation audit was executed to distinguish actual unresolved placeholders from documentation that merely describes placeholder concepts.

The audit reported:

```text
Unresolved blocking placeholders: 0
Placeholder validation: PASS
```

Result:

```text
Placeholder Validation: PASS
```

---

# 16. Local Markdown Reference Validation

Local Markdown references were checked against existing repository paths.

Execution evidence:

```text
broken: []
Local Markdown reference validation: PASS
```

Result:

```text
Local Markdown Reference Integrity: PASS
```

---

# 17. Canonical Document Reference Validation

Canonical document references were compared against the expected Build Framework document set.

Execution evidence:

```text
missing canonical references: []
Canonical document reference validation: PASS
```

Result:

```text
Canonical Document References: PASS
```

---

# 18. Join Defect Validation

Documentation normalization included explicit detection of accidental word joins introduced by automated transformations.

An identified defect:

```text
thecanonical
```

was corrected.

The subsequent recheck returned no matching defects for the executed detection patterns.

Result:

```text
Join Defect Validation: PASS
```

---

# 19. Manifest Synchronization

The canonical structural contract is:

```text
24 numbered documents
7 control documents
31 canonical files
00 → 23
```

The validated `EPIC.yaml` and filesystem contract confirm this structure.

`MANIFEST.md` is part of the current normalization set and SHALL preserve this same canonical structure.

Structural result:

```text
Manifest Structural Synchronization: PASS
```

---

# 20. Framework Completion State

EPIC-BLD-001 remains a completed framework.

Validated state:

```text
Framework:            Build Framework
EPIC:                 EPIC-BLD-001
Framework Version:    1.0.0
Framework Status:     Completed
Historical Published: Yes
Historical Tag:       v4.7.0-build-framework
```

Post-release revalidation does not change the historical completion or publication state.

---

# 21. Historical and Current State Separation

Historical lifecycle states SHALL remain preserved where they describe actual historical events.

Terms such as:

```text
Draft
In Progress
Pending
Prepared
```

are not automatically defects.

They are defects only when presented as authoritative current state in contradiction with the current canonical state.

The current authoritative framework state is:

```text
Completed
```

The current revalidation state after the evidence recorded here is:

```text
Validated
```

---

# 22. Repository Diff Validation

The repository executed:

```text
git diff --check
```

No whitespace errors were reported.

Execution summary:

```text
DiffCheck: 0
```

Result:

```text
git diff --check: PASS
```

---

# 23. Ruff Validation

The repository executed:

```text
ruff check .
```

Actual result:

```text
All checks passed!
```

Execution status:

```text
Ruff: 0
```

Result:

```text
Ruff: PASS
```

---

# 24. MyPy Validation

The repository executed:

```text
mypy src
```

Actual result:

```text
Success: no issues found in 527 source files
```

Execution status:

```text
MyPy: 0
```

Result:

```text
MyPy: PASS — 527 source files
```

---

# 25. Pytest Validation

The repository executed:

```text
pytest -q
```

Actual result:

```text
1243 passed in 1.02s
```

Execution status:

```text
Pytest: 0
```

Result:

```text
Pytest: PASS — 1243 tests
```

---

# 26. Repository Quality Gates

The current repository quality gate execution produced:

```text
Ruff:      0
MyPy:      0
Pytest:    0
DiffCheck: 0
```

Therefore:

```text
Ruff:      PASS
MyPy:      PASS
Pytest:    PASS
DiffCheck: PASS
```

Overall automated result:

```text
AUTOMATED QUALITY GATES: PASS
```

---

# 27. Build Architecture Consistency

The canonical Build Framework architecture is distributed across:

```text
03-Build-Principles.md
04-Build-Architecture.md
05-Build-Lifecycle.md
06-Build-Input-Requirements.md
07-Build-Inputs-and-Project-Structure.md
08-Build-Toolchain.md
09-Build-Environment-Management.md
10-Dependency-Management.md
11-Build-Configuration.md
12-Build-Philosophy.md
13-Build-Execution.md
14-Artifact-Management.md
15-Build-Validation.md
16-Build-Governance.md
17-Build-Automation-and-CI.md
```

The framework maintains the canonical conceptual progression:

```text
Controlled Inputs
        ↓
Resolved Build State
        ↓
Build Execution
        ↓
Candidate Outputs
        ↓
Validation
        ↓
Trusted Artifacts
        ↓
Release Handoff
```

The normalization work does not redefine this architecture.

Result:

```text
Build Architecture Consistency: PASS
```

---

# 28. Artifact Trust Model

The Build Framework preserves the distinction between:

```text
generated output
```

and:

```text
trusted artifact
```

Artifact trust depends on controlled and validated build conditions rather than command success alone.

The canonical trust model includes:

* controlled inputs;
* controlled environment;
* known toolchain;
* dependency state;
* reproducibility where required;
* validation;
* artifact identity;
* integrity evidence;
* provenance.

Result:

```text
Artifact Trust Consistency: PASS
```

---

# 29. Framework Boundaries

EPIC-BLD-001 integrates with adjacent FamilyOS engineering frameworks without replacing their primary responsibilities.

Relevant boundaries include:

```text
Testing Framework
Quality Framework
Release Framework
Security Framework
Observability Framework
Operations Framework
```

The Build Framework remains responsible for build-domain concerns and the production of validated artifacts suitable for downstream release processing.

Result:

```text
Framework Boundary Validation: PASS
```

---

# 30. Build / Release Boundary

The Build Framework owns build-domain responsibilities including:

```text
artifact production
artifact validation
build evidence
build provenance
build reproducibility
build trust
release handoff preparation
```

The Release Framework remains responsible for release-domain concerns including:

```text
release planning
release candidates
release approval
publication
distribution
rollback
release governance
release lifecycle
```

The Build Framework produces trusted release inputs.

It does not own the complete release lifecycle.

Result:

```text
Build / Release Boundary: PASS
```

---

# 31. Validation Evidence Principle

The revalidation follows the evidence rule:

```text
Execute
    ↓
Observe
    ↓
Evaluate
    ↓
Record
```

It does not use:

```text
Requirement exists
    ↓
Assume success
    ↓
Record PASS
```

This principle is particularly important for:

* YAML parsing;
* filesystem validation;
* reference checks;
* placeholder checks;
* Ruff;
* MyPy;
* Pytest;
* diff validation;
* historical tag verification.

---

# 32. Validation Matrix

| Validation Area                     | Current State |
| ----------------------------------- | ------------- |
| YAML Parse                          | PASS          |
| YAML Contract                       | PASS          |
| Filesystem Contract                 | PASS          |
| Canonical Inventory                 | PASS          |
| Numbering Integrity                 | PASS          |
| Control Documents                   | PASS          |
| Empty File Check                    | PASS          |
| Manifest Structural Synchronization | PASS          |
| Placeholder Validation              | PASS          |
| Join Defect Validation              | PASS          |
| Local Markdown References           | PASS          |
| Canonical Document References       | PASS          |
| Build Architecture Consistency      | PASS          |
| Artifact Trust Consistency          | PASS          |
| Framework Boundaries                | PASS          |
| Build / Release Boundary            | PASS          |
| Ruff                                | PASS          |
| MyPy                                | PASS          |
| Pytest                              | PASS          |
| Diff Check                          | PASS          |
| Historical Tag Existence            | PASS          |
| Historical Tag Integrity Baseline   | PASS          |

---

# 33. Repository Validation Evidence

Current evidence summary:

```text
YAML Parse:                    PASS
YAML Contract:                 PASS
Filesystem Contract:           PASS
Canonical Inventory:           PASS
Numbering Integrity:           PASS
Control Documents:             PASS
Empty Files:                   PASS
Placeholder Validation:        PASS
Join Defect Validation:        PASS
Local Markdown References:     PASS
Canonical Document References: PASS

Ruff:      PASS
MyPy:      PASS — 527 source files
Pytest:    PASS — 1243 tests
DiffCheck: PASS

Historical Tag:
v4.7.0-build-framework

Historical Tag Commit:
1b457dd86ae4c94033fa29b96b4e6db135202171
```

---

# 34. Validated Machine-Readable State

The evidence recorded by the current revalidation supports the following canonical state:

```yaml
baseline:
  framework_version: 1.0.0
  documentation_status: completed
  repository_validation_status: validated
  final_validation_status: validated

release:
  historical_tag: v4.7.0-build-framework
  publication_status: published
  historical_tag_immutable: true
```

`EPIC.yaml` SHALL be synchronized to this state as part of the same post-release normalization before the correction commit is finalized.

---

# 35. Post-Release Correction Policy

The current normalization occurs after historical publication.

Therefore:

* `v4.7.0-build-framework` SHALL remain unchanged;
* the historical tag SHALL NOT be moved;
* current corrections SHALL be committed separately;
* the correction commit SHALL represent the normalized canonical state;
* the historical tag SHALL continue to represent the original release state.

This preserves both:

```text
historical integrity
```

and:

```text
current canonical correctness
```

---

# 36. Commit and Publication Completion

The documentation revalidation is technically validated by the evidence recorded above.

The remaining repository workflow is operational:

```text
Synchronize final control-document states
        ↓
Stage post-release normalization
        ↓
Validate staged state
        ↓
Commit correction
        ↓
Re-run quality gates
        ↓
Push branch
        ↓
Verify remote branch
        ↓
Verify historical tag unchanged
        ↓
Confirm clean working tree
```

These repository publication steps SHALL provide the final post-commit and remote-state evidence.

---

# 37. Current Validation Decision

Based on the executed evidence:

```text
Framework Status:        Completed
Framework Version:       1.0.0
Historical Publication:  Published
Historical Tag:          v4.7.0-build-framework

YAML Validation:         PASS
Filesystem Validation:   PASS
Structural Validation:   PASS
Reference Validation:    PASS
Placeholder Validation:  PASS
Join Defect Validation:  PASS

Ruff:                     PASS
MyPy:                     PASS — 527 source files
Pytest:                   PASS — 1243 tests
DiffCheck:                PASS
Historical Tag:           PASS
```

Therefore:

```text
EPIC-BLD-001 REVALIDATION: PASS
```

---

# 38. Final Validation Principle

The Build Framework distinguishes historical publication from current validation evidence.

The historical release remains immutable.

The current canonical framework earns its validation state through reproducible evidence from the repository state being evaluated.

Therefore:

> A historical publication establishes provenance; current executable evidence establishes current validation.

---

**EPIC:** EPIC-BLD-001
**Framework:** Build Framework
**Framework Version:** 1.0.0
**Framework Status:** Completed
**Historical Publication:** `v4.7.0-build-framework`
**Publication Status:** Published
**Current Revalidation:** Validated
**Repository Validation:** Validated
**Final Validation Result:** PASS

---

# Dependency Reproducibility Baseline Validation

This section records revision-scoped implementation evidence separately from the historical Build Framework documentation revalidation above.

```text
Technical Revision: 113148e0db204ec48e140543f2b5dd9ab7273c87
Profile:            Python 3.13 development/CI
Resolver:           pip-tools 7.6.1
```

Executed evidence for this technical revision:

* focused dependency tests: PASS — 18 tests;
* dependency freshness check in the locked environment: PASS;
* fresh Python 3.13 environment bootstrap: PASS;
* editable installation using `--no-deps --no-build-isolation`: PASS;
* `pip check` in the repository environment: PASS;
* `pip check` in the fresh environment: PASS;
* Ruff: PASS;
* MyPy: PASS — 1141 source files;
* full Pytest: PASS — 1525 tests;
* `git diff --check`: PASS.

Validated conclusion:

```text
Dependency version-resolution reproducibility: VALIDATED
```

This result does not establish complete Build Framework implementation, CI validation, artifact reproducibility, artifact integrity, or software supply-chain assurance.

---

# Canonical CI Validation Baseline

This section records the second incremental technical implementation slice under the completed Build Framework documentation baseline.

```text
Implementation Revision: 504bd19
Corrective Revision:     c2ed8de
Workflow:                Canonical CI Validation
Remote Run:              31749853569
Remote Revision:         c2ed8de48822919fa69b670911ecd01a909b0732
Remote Conclusion:       SUCCESS
```

Commit `504bd19` introduced the provider-neutral canonical runner, deterministic validation result, local CLI entry point, builtin Plugin Compliance adapter, tests, and thin GitHub Actions workflow. The first real workflow execution exposed a missing Health documentation template; commit `c2ed8de` corrected that repository defect before the successful evidence run.

The successful remote workflow:

* checked out a known revision;
* provisioned Python 3.13;
* installed the committed locked dependency state;
* installed FamilyOS without dependency re-resolution;
* invoked the single canonical `familyos validation ci` entry point;
* uploaded structured `ci-validation.json` evidence;
* operated with repository permission `contents: read`;
* used official GitHub Actions dependencies pinned by commit SHA.

The downloaded canonical artifact records:

```text
Overall:                       PASSED
dependency-freshness:          PASSED
dependency-consistency:        PASSED
ruff:                          PASSED
mypy:                          PASSED
pytest:                        PASSED
builtin-plugin-compliance:     PASSED
Plugin Compliance Profile:     official
Discovered Builtin Plugins:    7
Compliant Builtin Plugins:     7
```

The workflow preserves mandatory validation failure as workflow failure while still attempting to upload structured evidence.

Validated conclusion:

```text
Canonical CI Validation Baseline: VALIDATED
Build Framework Technical Implementation: IN PROGRESS
```

This evidence does not establish a canonical build command, candidate artifacts, artifact validation, artifact integrity, full Build Evidence, release automation, or deployment capability.

---

# Local Developer Workflow Reconciliation

This documentation-only slice makes the already implemented Python 3.13
development and canonical validation workflow discoverable from the repository
root.

Repository evidence reviewed:

* `pyproject.toml` requires Python 3.13 and declares the direct dependency model;
* generated `requirements.txt` provides the controlled development/CI state;
* `scripts/check_dependency_lock.py` provides read-only freshness validation;
* `scripts/compile_dependencies.py` provides intentional regeneration;
* `familyos validation ci` provides the provider-neutral validation entry point;
* `.github/workflows/ci.yml` installs the same controlled dependency state and
  invokes that same canonical command;
* existing dependency and CI validation tests establish the behavior of these
  implementation surfaces.

The root `README.md` now records:

* Python 3.13 virtual-environment setup;
* the controlled bootstrap using `requirements.txt` followed by editable
  installation with `--no-deps --no-build-isolation`;
* `pip check` and dependency freshness behavior;
* intentional dependency regeneration;
* canonical local validation and optional deterministic JSON evidence;
* local/CI semantic alignment;
* common bootstrap and validation failures with remediation;
* safe cleanup of explicitly identified local environment and cache state;
* the explicit absence of canonical build, candidate-artifact, artifact
  validation, and build-output cleanup capabilities.

Validation conclusion:

```text
Local dependency and validation workflow: DOCUMENTED
Local/CI validation semantic alignment:   VALIDATED
Level 26 Local Developer Workflow:        PARTIAL
Build Framework Technical Implementation: IN PROGRESS
```

Level 26 remains partial because its artifact-location, artifact-related
cleanup, and CI-independent build requirements cannot be validated before
canonical artifact and CI build integration exists.

---

# Canonical Package Build — First Technical Slice

This revision establishes the first executable FamilyOS package-build path:

```text
familyos build
    -> CommandContext
    -> ApplicationContainer
    -> RunPackageBuildUseCase
    -> PackageBuilderPort
    -> PythonPackageBuilder
    -> sys.executable -m build --outdir <output-dir>
```

The implementation provides:

* a provider-neutral public command;
* an application-owned explicit output directory;
* a replaceable packaging port;
* a subprocess adapter with no shell interpretation;
* normalized success, failure, and execution-error results;
* non-zero CLI status for failed or erroneous packaging;
* sorted wheel and source-distribution paths as process-level outputs;
* no publication behavior;
* focused application, infrastructure, and CLI tests;
* one real isolated integration build using copied current packaging inputs.

Validation scope:

```text
Canonical package-build interface: IMPLEMENTED
Packaging mechanism:              IMPLEMENTED
Focused and integration tests:     PASS
Isolated wheel and sdist build:    PASS
Artifact validation/trust:         NOT IMPLEMENTED
CI build invocation:               NOT IMPLEMENTED
Build Framework implementation:    IN PROGRESS
```

The real integration test builds through the production adapter in a temporary
project containing the current `pyproject.toml`, `README.md`, `LICENSE`, and
`src/familyos_cli` tree. It produces one wheel and one source distribution and
asserts that all tracked checkout paths remain byte-identical.

The hygiene slice removes generated `*.egg-info/` from repository authority
and configures it, root `dist/`, and root `build/` as ignored generated state.
Setuptools may regenerate packaging metadata locally without dirtying
Git-tracked authority after hygiene commit `a85b5a7`.
`pyproject.toml` remains authoritative for package metadata, and generated
`requirements.txt` remains the controlled resolved dependency state.

Pre-commit repository-hygiene validation exercised these workflows while the
six egg-info deletions were still uncommitted:

* editable installation with `--no-deps --no-build-isolation`: PASS;
* dependency freshness: PASS;
* real `familyos build`: PASS — one wheel and one source distribution;
* canonical `familyos validation ci`: PASS;
* ignore-boundary verification: PASS — generated packaging paths ignored and
  authoritative `docs/build/`, application build, and integration-test paths
  visible.

These pre-commit runs did not by themselves prove checkout immutability after
the removals entered Git history. The dedicated post-commit evidence below
provides that proof. Neither evidence set establishes Artifact Discovery,
artifact validation, identity, integrity, trust, or Build Evidence.

## Post-Commit Source-Mutation Verification — 2026-08-14

After packaging repository hygiene commit `a85b5a7`, the following workflows
were executed against the real checkout:

* editable installation with `--no-deps --no-build-isolation`: PASS — only
  ignored packaging metadata was regenerated, and tracked status was clean;
* dependency freshness: PASS — `requirements.txt` was synchronized with
  `pyproject.toml`, generated state remained ignored, and tracked status was
  clean;
* real `familyos build`: PASS — root `dist/` contained
  `familyos_cli-0.1.0-py3-none-any.whl` and
  `familyos_cli-0.1.0.tar.gz`, while tracked status remained clean;
* `familyos validation ci`: PASS — all six mandatory gates passed, all seven
  official builtin plugins were compliant, and final tracked status was clean.

Ignored `*.egg-info/`, root `dist/`, and root `build/` state is generated state,
not authoritative source. This post-commit evidence directly closes the Level
13 requirement that execution not unexpectedly mutate authoritative source.
It does not establish artifact validation, identity, integrity, trust, Build
Evidence, release readiness, or publication.

## Level 14 Artifact Discovery — 2026-08-14

The canonical package-build path now separates execution output observation
from application-owned artifact discovery:

```text
PythonPackageBuilder
    -> raw direct files created or replaced by this execution
DiscoverPackageArtifactsUseCase
    -> expected wheel and source-distribution contract
    -> classified candidate outputs
```

The current contract requires exactly one regular `.whl` and exactly one
regular `.tar.gz` file in the resolved output directory. The default directory
is `<project-root>/dist`; an explicit `--output-dir` becomes canonical for that
invocation. Missing, duplicate, out-of-location, and unexpected current outputs
produce a deterministic discovery failure and non-zero command result.
Unchanged stale files are excluded by the execution snapshot; changed or
replaced files are current outputs and are discovered normally.

Focused Ruff and MyPy validation passed. The targeted application,
infrastructure, integration, and CLI suite passed with 29 tests, including a
real isolated build through the production execution and discovery path.

Candidate classification proves only conformance to the expected current
output set. It does not establish artifact validation, identity, integrity,
trust, Build ID, Build Evidence, release handoff, or publication. Level 14
remains partial because temporary/intermediate output classification and Build
ID association remain open. At that revision, CI build invocation also
remained unimplemented.

## CI Package Build Integration — 2026-08-14

Status: REMOTELY VERIFIED.

The `Canonical CI Validation` workflow now runs `familyos build --output-dir
dist` immediately after successful validation, and uploads the resulting
`dist/` directory as the `familyos-package-candidates` artifact using the
same pinned `actions/upload-artifact` reference already used for validation
evidence. No new Python packaging or discovery logic was introduced in YAML;
the workflow invokes only the existing canonical `familyos build` command.

Static and local review confirmed:

* exactly one `familyos build` invocation; no `python -m build` in YAML;
* no wheel/sdist filename filtering or count logic in YAML;
* the package-build step carries no `continue-on-error`, so a non-zero
  `familyos build` exit (execution or discovery failure) fails the job
  directly;
* the candidate-upload step carries no `if: always()`; GitHub Actions'
  default per-step `success()` gating means it — and the build step before
  it — automatically skip when the preceding mandatory validation-failure
  step (`exit 1`) has run, so a failed validation cannot produce package
  candidates, without any reordering of the existing validation steps;
* `permissions: contents: read` is unchanged; no additional scope was added;
* local reproduction (`familyos validation ci` then
  `familyos build --output-dir dist`) was executed against this checkout and
  succeeded, matching the workflow's exact invocation.

Remote execution evidence:

* implementation commit: `63693e6152c4c8cd822313cde88e2019e5ca71a0`
  (`63693e6`);
* workflow run: `31792439104`, triggered by `push`;
* workflow status/conclusion: `completed` / `success`;
* `validate` job result: `success`;
* retained validation artifact:
  `familyos-ci-validation/ci-validation.json`;
* downloaded candidate artifact contents:
  `familyos_cli-0.1.0-py3-none-any.whl` and
  `familyos_cli-0.1.0.tar.gz`;
* candidate counts: wheel `1`, source distribution `1`.

This direct evidence closes the Level 27 canonical-build and explicit
candidate-collection requirements. Candidate means discovered build output
only. No Artifact Validation occurred, no integrity digest or integrity
evidence was generated, and no identity, trust, Build ID, Build Evidence,
release-readiness, handoff, or publication semantics are established. No Level
15+ item was changed.

## Python Package Structural Validation — 2026-08-14

This implementation slice extends the canonical application sequence without
changing the GitHub Actions workflow:

```text
PythonPackageBuilder
    -> DiscoverPackageArtifactsUseCase
    -> ValidatePythonPackageArtifactsUseCase
    -> CanonicalPackageBuildResult
```

Validation consumes only the exact candidates returned by successful Artifact
Discovery. It does not rescan `dist/`. Execution failure skips discovery and
validation, discovery failure skips validation, structural `INVALID` fails the
aggregate build, and structural `VALID` permits aggregate success.

The wheel contract covers:

* a regular non-symlink candidate file;
* a readable, non-corrupt ZIP with safe and unique member paths;
* exactly one top-level package `.dist-info` directory;
* required readable `METADATA`, `WHEEL`, and `RECORD` files;
* structurally readable core/WHEEL metadata and CSV `RECORD` rows;
* coherent name/version across filename, `.dist-info`, core metadata, and the
  authoritative repository `pyproject.toml`.

The source-distribution contract covers:

* a regular non-symlink candidate file;
* a readable, non-corrupt gzip-compressed tar archive;
* safe regular members under exactly one coherent package root;
* required readable `PKG-INFO` and archived `pyproject.toml`;
* presence of Python source material;
* coherent name/version across filename, root, `PKG-INFO`, archived project
  metadata, and the authoritative repository `pyproject.toml`.

Archive members are decompressed and inspected through bounded in-memory streams
without filesystem extraction; repository paths are never materialized from
archive member names. The bounded-inspection controls allow at most 10,000
members, 64 MiB of actual content per regular member, and 512 MiB of aggregate
actual decompressed content per archive. Wheel inspection accepts stored and
deflated members; compression methods whose standard-library readers cannot
honor bounded output requests are rejected before decompression. These controls
bound this validator's structural inspection; they are not a universal hostile-
archive sandbox. `RECORD` hashes and sizes are not verified. The slice does not
install either artifact, resolve dependencies, run imports or the CLI, validate
the complete expected module/resource inventory, build from the sdist, or
generate integrity data.

Executed local evidence:

```text
Changed-file Ruff:                         PASS
Changed-file MyPy:                         PASS — 11 source files
Targeted validation/build suite:           PASS — 65 tests
Full Pytest:                               PASS — 1559 tests
Canonical repository validation:           PASS — all six gates
Real `familyos build --output-dir dist`:    PASS — structural result `VALID`
```

The immutable result's `VALID` state means structurally valid according to this
contract only. Candidate classification remains unchanged. Structural validity
does not establish Artifact Identity, Artifact Integrity, trust, provenance,
Build ID, Build Evidence, signing, attestation, release readiness, publication,
promotion, or deployment.

Level 16 remains partial, and the Level 27 `Run artifact validation` item remains
open until a later committed revision is executed successfully by the remote
GitHub Actions workflow. Framework version `1.0.0` and immutable historical tag
`v4.7.0-build-framework` remain unchanged.

## Remote Structural-Validation Evidence — 2026-08-14

This slice records remote evidence only. No production Python, tests, or CI
workflow definition changed.

The `Canonical CI Validation` workflow executed commit
`c49c655837f300930fa7a6b5df1714207e71e903` (short `c49c655`) on branch
`feature/bld-python-package-structural-validation`, `push` event, GitHub
Actions run `31801029251`. The run and its `validate` job both completed with
conclusion `success`.

At commit `c49c655`, the canonical `familyos build --output-dir dist`
invocation already includes the sequence:

```text
Build Execution
    -> Artifact Discovery
    -> Python Package Structural Validation
```

so this successful remote run empirically proves remote execution of the
mandatory structural-validation path, not merely build and discovery. The
`familyos-ci-validation` artifact (`ci-validation.json`) remained available,
and `familyos-package-candidates` was uploaded containing exactly
`familyos_cli-0.1.0-py3-none-any.whl` and `familyos_cli-0.1.0.tar.gz` (wheel
count `1`, source-distribution count `1`).

This directly closes the Level 27 `Run artifact validation` checklist item.
The prior sentence above, stating that this item "remains open until a later
committed revision is executed successfully by the remote GitHub Actions
workflow," is superseded by this run.

The run again emitted the previously recorded GitHub Actions Node.js 20
deprecation warning. That maintenance debt is unchanged and already recorded;
it does not affect this run's `success` conclusion or the validation evidence
above.

This evidence establishes only that the currently implemented structural
validation executed successfully in CI. It does NOT establish:

* isolated wheel installation;
* import smoke or CLI smoke validation;
* source-distribution functional build/install validation;
* Artifact Identity;
* Artifact Integrity or integrity digest generation;
* Build Evidence;
* trust, provenance, signing, release readiness, or publication.

`Generate artifact integrity data` and `Collect Build Evidence` remain open.
No Level 15 or Level 17 item changed. The remaining functional Level 16 items
remain open. Framework version `1.0.0` and immutable historical tag
`v4.7.0-build-framework` remain unchanged.

## Python Package Content and Metadata Validation — 2026-08-14

This implementation extends `ValidatePythonPackageArtifactsUseCase`; the
canonical sequence remains:

```text
Build Execution
    -> Artifact Discovery
    -> Python Package Validation
```

No archive is rediscovered, installed, imported, or executed. The same exact
discovered wheel and source-distribution candidates are inspected through the
existing bounded archive readers.

### Dependency authority

PEP 440 runtime specifiers and PEP 508 dependency requirements are parsed with
the maintained `packaging` implementation. Because this functionality executes
at application runtime, `packaging>=26.0` is now an explicit project dependency;
the prior lock entry was transitive through build/test tools only. The generated
`requirements.txt` was regenerated by `scripts/compile_dependencies.py` and
passes the canonical freshness/resolution check.

### Static metadata contract

The authoritative repository `pyproject.toml` provides package name, version,
`requires-python`, direct dependencies, and optional dependency groups. The
validator normalizes and compares that contract with:

* wheel `METADATA` `Requires-Python` and every `Requires-Dist` field;
* source-distribution `PKG-INFO` `Requires-Python` and every `Requires-Dist`
  field;
* the archived source-distribution `pyproject.toml` project metadata.

Malformed specifiers or requirements, missing/unexpected dependencies, and
metadata disagreement are deterministic `INVALID` findings. Equivalent PEP 440
version forms are compared semantically. These comparisons are package metadata
coherence only and do not create Artifact Identity.

### Content inventory contract

Content validation separates source existence, packaging intent, and actual
candidate content. The configured setuptools package discovery and regular
package source define expected Python modules. Non-code resource intent comes
independently from `tool.setuptools.package-data`: the validator supports the
repository's exact discovered package name mapped to relative `pathlib` glob
patterns, and only regular non-symlink source files matching those patterns are
expected resources. A non-code file does not become intended merely by existing
beneath `src/familyos_cli`. Generated caches and bytecode, egg-info, editor swap
files, and common system metadata remain excluded.

The wheel must contain the exact expected package inventory outside its
`.dist-info` metadata directory. The source distribution must contain that same
inventory beneath its configured source directory. Defined project files and
backend-generated root/egg-info metadata are allowed in the source distribution;
unrelated root content is rejected. Missing modules/resources and unintended
modules/resources are reported separately and in sorted order.

The initial comparison proved that 18 builtin plugin YAML manifests and Jinja
templates were absent from both candidates. `tool.setuptools.package-data` now
makes those resources and `py.typed` explicit. The real canonical wheel and
source distribution contain exactly the independently authorized module and
resource inventories. Regression coverage also places
`plugins/builtin/security/DEBUG_LEAKED_NOTES.env` in the source tree without a
matching package-data declaration and proves that injecting it into either
candidate is an unintended-resource `INVALID` finding; no secret-content
scanning is performed.

Executed local evidence:

```text
Changed-file Ruff:                         PASS — 3 Python files
Changed-file MyPy:                         PASS — 3 source files
Targeted validation/build suite:           PASS — 86 tests
Full Pytest:                               PASS — 1559 tests
Canonical repository validation:           PASS — all six gates
Real `familyos build --output-dir dist`:    PASS — static package result `VALID`
```

The targeted count is produced by this exact five-file scope (including
Artifact Discovery because validation consumes its result):

```bash
python -m pytest -q \
  tests/unit/application/build/test_validate_python_package_artifacts.py \
  tests/unit/application/build/test_discover_package_artifacts.py \
  tests/unit/application/build/test_run_package_build.py \
  tests/integration/build/test_python_package_build.py \
  tests/e2e/test_cli_package_build.py
```

This slice closes the six static Level 16 runtime/dependency metadata and
content-inventory items. Clean installation, import smoke, CLI smoke, and
functional source-distribution build/install validation remain open. It does
not add Artifact Identity, Artifact Integrity, digests, Build ID, Build
Evidence, trust, provenance, signing, release readiness, publication,
promotion, or deployment. The CI workflow is unchanged; the existing canonical
command will exercise this extension after commit, while remote evidence for
the extension remains future work. Framework version `1.0.0` and immutable
historical tag `v4.7.0-build-framework` remain unchanged.

## Python Package Functional Validation — 2026-08-14

### Invocation and architecture

Wheel functional validation is explicit through:

```bash
familyos build --output-dir dist --functional-validation
```

The default build remains the fast static path, and CI is unchanged. The
opt-in sequence is:

```text
Build Execution
    -> Artifact Discovery
    -> Structural / Metadata / Content Validation
    -> Wheel Functional Validation
```

The application passes the exact discovered wheel only after static validation
succeeds. `PythonWheelFunctionalValidatorPort` is the minimal inversion boundary
for external venv, pip, Python, and console execution; the temporary-environment
implementation remains in infrastructure and orchestration tests use a
recording fake.

### Clean-environment and dependency contract

The infrastructure adapter creates a fresh temporary venv without
`--system-site-packages`, never installs the checkout editably, and removes the
temporary tree deterministically. All pip and smoke commands use an external
working directory. The inherited `PYTHONPATH`, `PYTHONHOME`, user-base, active-
venv, and launcher variables are removed; `PYTHONNOUSERSITE=1` is set.

The repository has no committed runtime wheelhouse, so fully offline dependency
installation is not currently available without adding new dependency
infrastructure. The smallest controlled contract uses pip `--isolated`,
`--require-virtualenv`, and `--only-binary=:all:` to install the exact local
wheel. Its runtime dependency closure is selected from emitted wheel metadata
and constrained to the exact pins in committed `requirements.txt`. The shared
lock's development and build entries are not requested for installation. Pip
may use its cache or retrieve those constrained wheels; it cannot choose
unconstrained runtime versions.

### Functional checks and failure semantics

The import target is `familyos_cli.main`, matching the canonical
`familyos = familyos_cli.main:app` project script. It is imported by the venv
Python with `-I`; the probe returns the resolved module path, which must be
inside the temporary venv and outside repository `src/`. CLI smoke invokes the
installed venv executable exactly as `familyos --help` and requires canonical
help output. No repository command or source distribution is executed; CLI
smoke is side-effect free and not network dependent. Dependency wheel retrieval
may use pip's public index when its cache is empty.

Environment/installation, import, and CLI failures produce distinct,
deterministic functional `INVALID` findings. Requested functional failure makes
the aggregate build fail. Without the explicit option, functional validation is
not executed. Structural failure always skips functional validation.

The real negative control rewrites only the console entry point of an otherwise
structurally valid FamilyOS wheel, then exercises the production adapter. Clean
installation and `familyos_cli.main` import succeed, while the installed broken
entry point is rejected at the CLI-smoke stage.

Executed local evidence:

```text
Changed-file Ruff:                                      PASS
Changed-file MyPy:                                      PASS
Targeted functional/relevant package-build suite:       PASS — 105 tests
Full Pytest:                                            PASS — 1561 tests
Real clean-environment FamilyOS wheel validation:       PASS — functional `VALID`
Real broken-entry-point negative control:               PASS — CLI-stage `INVALID`
```

The targeted count is produced by this exact command:

```bash
python -m pytest -q \
  tests/unit/application/build/test_package_functional_validation.py \
  tests/unit/infrastructure/build/test_python_wheel_functional_validator.py \
  tests/unit/application/build/test_run_package_build.py \
  tests/unit/application/build/test_discover_package_artifacts.py \
  tests/unit/application/build/test_validate_python_package_artifacts.py \
  tests/unit/infrastructure/build/test_python_package_builder.py \
  tests/integration/build/test_python_package_build.py \
  tests/e2e/test_cli_package_build.py
```

This slice closes clean-environment wheel installation, installed import smoke,
and installed CLI smoke. Functional source-distribution build/install
validation remains open. No remote execution claim is added, and no Artifact
Identity, Build ID, Artifact Integrity, digest, Build Evidence, provenance,
trust, signing, release readiness, publication, promotion, or deployment
semantics are established. Framework version `1.0.0` and immutable historical
tag `v4.7.0-build-framework` remain unchanged.

## Python Source Distribution Rebuildability — 2026-08-14

### Canonical construction contract

FamilyOS production infrastructure directly invokes the pypa/build frontend as:

```text
python -m build --outdir <output>
```

No `--wheel` or `--sdist` distribution flag is supplied. The documented
pypa/build default first emits the source distribution, extracts that exact
archive into temporary state, and builds the wheel from it using a separate
isolated backend environment. FamilyOS does not reimplement this two-step
frontend behavior and does not rebuild a discovered source distribution again.

Because repository build infrastructure directly invokes `python -m build`,
`build>=1.5` is now an explicit `[project.optional-dependencies].dev`
declaration. Canonical dependency compilation retained the existing resolved
`build==1.5.0` version and updated only its direct-authority annotation and
dependency-input digest.

### Load-bearing negative control

The real integration negative control creates two isolated temporary copies of
the FamilyOS package. Both add a test-only `setup.py` construction guard that
requires `src/familyos_cli/__init__.py`, while `MANIFEST.in` excludes that file
from the source distribution. Explicit direct wheel construction from checkout
succeeds and the wheel contains the guarded file. Production
`PythonPackageBuilder` then emits the source distribution but fails non-zero
during pypa/build's wheel-from-sdist step because the guarded file is absent.
No wheel is emitted. This behavior proves that canonical execution depends on
the generated source distribution and does not silently substitute checkout
source.

The omitted module also remains a static `INVALID` finding when that emitted
negative-control archive is passed to the production static validator. The
functional regression does not weaken or bypass the existing package-content
contract.

### Positive and validation evidence

The real canonical FamilyOS build produced and discovered exactly one source
distribution and exactly one wheel. Both passed existing static package
validation. The behavioral negative control protects the fact that this wheel
is produced through the source-distribution path. The existing opt-in command
also installed and smoke-tested the derived wheel successfully.

Executed local evidence:

```text
Changed-file Ruff:                                      PASS — 2 Python files
Changed-file MyPy:                                      PASS — 2 Python files
Dependency lock compilation:                            PASS
Dependency freshness/consistency:                       PASS
Load-bearing sdist negative control:                    PASS — 1 test
Targeted functional/relevant package-build suite:       PASS — 106 tests
Full Pytest:                                            PASS — 1561 tests
Canonical repository validation:                       PASS — all six gates
Real `familyos build --output-dir dist`:                PASS — static `VALID`
Real build with `--functional-validation`:              PASS — functional `VALID`
```

The targeted count is produced by this exact command:

```bash
python -m pytest -q \
  tests/unit/application/build/test_package_functional_validation.py \
  tests/unit/infrastructure/build/test_python_wheel_functional_validator.py \
  tests/unit/application/build/test_run_package_build.py \
  tests/unit/application/build/test_discover_package_artifacts.py \
  tests/unit/application/build/test_validate_python_package_artifacts.py \
  tests/unit/infrastructure/build/test_python_package_builder.py \
  tests/integration/build/test_python_package_build.py \
  tests/e2e/test_cli_package_build.py
```

This closes the final Level 16 item with source-distribution rebuildability
semantics. It does not prove byte-for-byte reproducibility. pypa/build may still
resolve isolated backend dependencies through available caches or the network;
controlling that resolution more strongly remains separate toolchain-
determinism work. No remote execution claim, CI workflow change, Artifact
Identity, Build ID, Artifact Integrity, digest, Build Evidence, provenance,
trust, signing, release readiness, publication, promotion, or deployment
semantics are introduced. Framework version `1.0.0` and immutable historical
tag `v4.7.0-build-framework` remain unchanged.

## Isolated Build-Backend Dependency Version Determinism — 2026-08-14

### Canonical constraint contract

The canonical production command is now equivalent to:

```text
python -m build \
  --dependency-constraints-txt <absolute-project-root>/requirements.txt \
  --outdir <output>
```

The constraint path is resolved from the authoritative project root before the
subprocess is launched and is independent of the caller's current working
directory. No `--wheel`, `--sdist`, or `--no-isolation` option is supplied.
pypa/build therefore continues to create the source distribution in one
isolated environment and the wheel from that exact emitted archive in a second
isolated environment.

`requirements.txt` is used only with pip constraint semantics. It restricts
versions for dependencies actually requested by the backend; it neither
requests installation of every locked package nor rejects a backend dependency
solely because that package is absent from the file. Network access or a usable
cache may still be required.

### Two-environment falsification evidence

The load-bearing integration regression creates isolated temporary project
copies and adds `packaging>=24` as a test-only build-system requirement. A
test-only setuptools probe writes the installed `packaging` version into the
existing `familyos_cli/py.typed` resource during backend execution. The copied
constraint authority deliberately pins `packaging==24.2`.

An unconstrained control builds successfully but records a resolver-selected
version other than `24.2` in both artifacts. The production builder records
`24.2` in the emitted sdist resource and again in the derived wheel resource.
Reading the artifacts directly proves that both isolated backend executions
honored the constraint without depending on human-readable pypa/build logs.
The existing construction-asymmetry regression separately continues to prove
that checkout source is not substituted for the emitted sdist.

### Executed evidence

```text
Changed-file Ruff:                                      PASS — 3 Python files
Changed-file MyPy:                                      PASS — 3 Python files
Behavioral two-environment constraint regression:      PASS — 1 test
Build-through-sdist fallback regression:               PASS — 1 test
Targeted functional/relevant package-build suite:      PASS — 108 tests
Full Pytest:                                            PASS — 1561 tests
Dependency freshness/consistency:                       PASS
Canonical repository validation:                       PASS — all six gates
Real `familyos build --output-dir dist`:                PASS — static `VALID`
Real build with `--functional-validation`:              PASS — functional `VALID`
```

The targeted count is produced by this exact command:

```bash
python -m pytest -q \
  tests/unit/application/build/test_package_functional_validation.py \
  tests/unit/infrastructure/build/test_python_wheel_functional_validator.py \
  tests/unit/application/build/test_run_package_build.py \
  tests/unit/application/build/test_discover_package_artifacts.py \
  tests/unit/application/build/test_validate_python_package_artifacts.py \
  tests/unit/infrastructure/build/test_python_package_builder.py \
  tests/integration/build/test_python_package_build.py \
  tests/e2e/test_cli_package_build.py
```

This establishes version constraint enforcement for the current known isolated
backend dependency closure represented by `requirements.txt`. It does not
establish an allowlist, offline capability, network independence, full critical
toolchain identity, repeated-build equality, or byte-for-byte reproducibility.
Level 11 `Ensure CI installs from canonical definitions` and Level 40
`Establish critical toolchain version identity` remain open. Level 16 remains
complete. No remote execution claim, CI workflow change, Artifact Identity,
Build ID, Artifact Integrity, digest, Build Manifest, Build Evidence,
provenance, trust, signing, release readiness, publication, promotion, or
deployment semantics are introduced. Framework version `1.0.0` and immutable
historical tag `v4.7.0-build-framework` remain unchanged.

## Minimal Build Context — Source Revision Capture — 2026-08-15

The canonical package-build application flow now captures an immutable
pre-build `SourceState` through `SourceStateProviderPort` before package
construction. `GitSourceStateProvider` accepts Git state only when
`git rev-parse --show-toplevel` resolves exactly to the configured project
root, preventing nested projects from inheriting an ancestor repository.

Accepted repositories capture the exact `HEAD^{commit}` and derive working-tree
dirtiness from `git status --porcelain=v1 -z --untracked-files=all`. Non-Git
roots, unavailable Git, inaccessible metadata, and rejected ancestor
repositories produce unknown source state without failing the build.

`CanonicalPackageBuildResult` preserves the same pre-build observation across
successful and failure returns. Real-Git behavioral tests cover clean, unstaged,
staged, deleted, untracked, ignored, detached/tagged, shallow, non-Git,
unavailable-Git, and ancestor-root rejection cases.

A real canonical FamilyOS build captured revision
`169b0141a28ce997aca1b765014ebf12587ebfbb`, exactly matching independently
queried `HEAD`; it captured the pre-build dirty state as `true`, succeeded with
two candidate artifacts, and left tracked checkout state unchanged.

Executed local validation:

```text
Build-slice tests:                                  PASS — 123 tests
Global Ruff:                                        PASS
Global MyPy:                                        PASS — 1183 source files
Controlled full Pytest (PYTHONPATH=. pytest -q):    PASS — 1561 tests
Git checkout canonical-build probe:                 PASS
git diff --check:                                   PASS
```

Plain `pytest -q` remains independently blocked during collection by the
pre-existing top-level `scripts` import-path behavior under configured
`--import-mode=importlib`. No import-path change is included in this slice.

This closes only Level 5 source-revision capture and relevant working-tree-state
capture. The minimum Build Context model, canonical source identity, Build ID,
Artifact Identity, Artifact Integrity, Build Manifest, Build Evidence,
provenance, and release-candidate source policy remain open or out of scope.
Framework version `1.0.0` and immutable historical tag
`v4.7.0-build-framework` remain unchanged.
