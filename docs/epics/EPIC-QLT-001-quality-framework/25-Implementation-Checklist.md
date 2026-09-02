# Quality Framework

# 25 Implementation Checklist

## Overview

This document defines the implementation checklist for EPIC-QLT-001 — Quality Framework.

Its purpose is to translate the architectural and governance model defined by the Quality Framework into a concrete engineering execution sequence.

The checklist is not intended to force implementation of every advanced capability immediately.

It provides a controlled progression from the current normative framework toward an executable FamilyOS quality platform.

The implementation sequence should preserve the dependency order established by the roadmap:

```text id="impl-overview-flow"
Normative Framework
      ↓
Core Domain Models
      ↓
Deterministic Verification
      ↓
Structured Findings
      ↓
Quality Evidence
      ↓
Quality Assessment
      ↓
Quality Automation
      ↓
Quality Profiles
      ↓
Quality Gates
      ↓
Quality Observability
      ↓
Risk / Debt / Compliance
      ↓
Quality Governance
      ↓
Continuous Improvement
      ↓
Quality Intelligence
```

---

# Purpose

The implementation checklist provides a practical mechanism for:

* planning implementation;
* sequencing work;
* tracking completion;
* validating dependencies;
* preventing premature complexity;
* coordinating cross-framework integration;
* defining acceptance criteria;
* preparing future implementation EPICs and RFCs.

The checklist should be treated as an engineering planning artifact, not as a substitute for detailed implementation design.

---

# Foundational Implementation Principle

The foundational implementation principle is:

> Implement the smallest coherent Quality Framework capability that creates reliable engineering value, then evolve it through evidence.

This means FamilyOS should prefer:

```text id="impl-small-steps"
Simple
Deterministic
Tested
Observable
Composable
```

capabilities before introducing advanced orchestration or intelligence.

---

# Implementation Status Model

Checklist items may conceptually use:

```text id="impl-status"
[ ] NOT_STARTED
[-] IN_PROGRESS
[x] COMPLETE
[!] BLOCKED
```

The actual repository workflow may use simpler Markdown checkboxes.

---

# Implementation Completion Principle

An item should only be considered complete when:

```text id="impl-completion"
Implementation
      +
Tests
      +
Documentation
      +
Validation
```

are complete where applicable.

Code existence alone is not sufficient.

---

# Phase 0 — Normative Framework Completion

## Objective

Complete and validate the Quality Framework documentation baseline.

### Normative Chapters

```text id="impl-phase0-chapters"
[ ] 00-EPIC.md complete
[ ] 01-Context.md complete
[ ] 02-Vision.md complete
[ ] 03-Quality-Principles.md complete
[ ] 04-Quality-Architecture.md complete
[ ] 05-Quality-Domains.md complete
[ ] 06-Quality-Requirements.md complete
[ ] 07-Quality-Metrics.md complete
[ ] 08-Quality-Evidence.md complete
[ ] 09-Quality-Risk-Management.md complete
[ ] 10-Defect-and-Quality-Debt-Management.md complete
[ ] 11-Quality-Reviews-and-Assessments.md complete
[ ] 12-Quality-Automation.md complete
[ ] 13-Quality-Observability.md complete
[ ] 14-Quality-Gates.md complete
[ ] 15-Quality-Compliance.md complete
[ ] 16-Continuous-Improvement.md complete
[ ] 17-Quality-Governance.md complete
[ ] 18-Quality-Framework-Lifecycle.md complete
[ ] 19-Roadmap.md complete
[ ] 20-References.md complete
[ ] 21-Validation.md complete
[ ] 22-Summary.md complete
[ ] 23-Release.md complete
[ ] 24-Implementation-Checklist.md complete
```

The canonical repository numbering remains authoritative if the actual file sequence differs.

---

# Control Artifacts

```text id="impl-control-artifacts"
[ ] EPIC.yaml synchronized
[ ] README.md synchronized
[ ] MANIFEST.md synchronized
[ ] CHANGELOG.md updated
[ ] VALIDATION.md updated
[ ] Revision-History.md updated
```

---

# Structural Validation

```text id="impl-structural-validation"
[ ] Canonical file inventory verified
[ ] No empty normative files
[ ] No unexpected duplicate chapters
[ ] Naming conventions validated
[ ] Numbering validated
[ ] Markdown code fences validated
[ ] Internal references validated
```

---

# Cross-Framework Validation

```text id="impl-cross-framework-validation"
[ ] Engineering Foundation alignment reviewed
[ ] Testing Framework alignment reviewed
[ ] Documentation Framework alignment reviewed
[ ] Build Framework alignment reviewed
[ ] Release Framework alignment reviewed
[ ] Plugin Compliance Framework alignment reviewed
[ ] Architecture Foundation alignment reviewed
[ ] Security Architecture relationship reviewed
```

---

# Phase 0 Exit Criteria

```text id="impl-phase0-exit"
[ ] Blocking documentation findings resolved
[ ] Normative terminology consistent
[ ] Framework responsibilities clearly separated
[ ] Validation evidence recorded
[ ] Framework documentation release ready
```

---

# Phase 1 — Quality Package Architecture

## Objective

Create the implementation structure required for the Quality Framework without prematurely implementing advanced infrastructure.

A conceptual source structure may be:

```text id="impl-package-architecture"
src/familyos_cli/quality/
├── domain/
├── application/
├── infrastructure/
└── presentation/
```

The actual location must follow FamilyOS repository architecture.

---

# Package Structure Checklist

```text id="impl-package-checklist"
[x] Confirm canonical package location
[x] Create quality package
[x] Create domain package
[x] Create application package
[x] Create infrastructure package
[ ] Create presentation / CLI integration package
[x] Add package exports where appropriate
[x] Preserve Clean Architecture dependency direction
```

---

# Architecture Constraints

```text id="impl-architecture-constraints"
[x] Domain layer has no Ruff-specific dependency
[x] Domain layer has no MyPy-specific dependency
[x] Domain layer has no Pytest-specific dependency
[x] Domain layer has no CI-provider dependency
[ ] Infrastructure depends on application/domain contracts
[ ] Presentation depends on application services
[x] Tool integrations remain adapters
```

---

# Architecture Tests

```text id="impl-architecture-tests"
[x] Add import-boundary tests
[ ] Add package dependency tests where tooling exists
[x] Add regression test preventing tool-specific domain coupling
```

---

# Phase 1 Exit Criteria

```text id="impl-phase1-exit"
[x] Package architecture established
[x] Dependency boundaries validated
[x] No unnecessary infrastructure introduced
[x] Architecture tests pass
```

---

# Phase 2 — Core Domain Models

## Objective

Implement the minimum stable Quality Framework domain vocabulary.

---

# Quality Severity

Implement a shared `QualitySeverity` concept.

Expected semantics:

```text id="impl-severity"
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

Checklist:

```text id="impl-severity-checklist"
[x] Define QualitySeverity
[x] Document semantics
[ ] Add serialization support if required
[x] Test all valid values
[ ] Test invalid values
[ ] Ensure ordering semantics are explicit if supported
```

---

# Quality Status

Implement quality execution or evaluation states.

Potential initial values:

```text id="impl-status-model"
PASS
WARNING
FAIL
ERROR
SKIPPED
UNKNOWN
```

Checklist:

```text id="impl-status-checklist"
[x] Define QualityStatus
[x] Separate execution status from severity
[x] Define ERROR semantics
[x] Define UNKNOWN semantics
[ ] Test serialization
[ ] Test invalid status rejection
```

---

# Quality Domain

Introduce a controlled domain classification where useful.

Potential values may include:

```text id="impl-domain-values"
CODE
TESTING
ARCHITECTURE
DOCUMENTATION
SECURITY
DEPENDENCIES
BUILD
RELEASE
COMPLIANCE
GOVERNANCE
```

Checklist:

```text id="impl-domain-checklist"
[x] Determine whether enum or extensible identifier is preferable
[x] Define initial domains
[x] Avoid unnecessary hard-coding of future domains
[x] Add validation tests
```

---

# Quality Target

Implement a model identifying the object being evaluated.

Potential fields:

```text id="impl-target-fields"
type
identifier
revision
path
metadata
```

Checklist:

```text id="impl-target-checklist"
[x] Define QualityTarget
[x] Support repository target
[ ] Support file / module target
[ ] Support plugin target
[ ] Support documentation target
[ ] Support release target where needed
[ ] Test target identity
[ ] Test revision binding
```

---

# Quality Finding

Implement the core `QualityFinding` model.

Suggested initial fields:

```text id="impl-finding-fields"
id
rule_id
domain
severity
status
message
target
location
evidence_ids
```

Checklist:

```text id="impl-finding-checklist"
[x] Define QualityFinding
[x] Define stable identifier semantics
[x] Define required fields
[x] Define optional location
[x] Define evidence references
[ ] Define status lifecycle if included initially
[x] Add construction tests
[ ] Add serialization tests
[ ] Add equality / fingerprint tests if applicable
```

---

# Quality Requirement

Implement `QualityRequirement`.

Suggested initial fields:

```text id="impl-requirement-fields"
id
title
description
domain
authority
mandatory
applicability
verification
```

Checklist:

```text id="impl-requirement-checklist"
[x] Define QualityRequirement
[x] Define authority field
[x] Define mandatory semantics
[x] Define applicability representation
[x] Define verification expectations
[x] Test requirement validation
```

---

# Quality Rule

Implement `QualityRule`.

Suggested initial fields:

```text id="impl-rule-fields"
id
requirement_id
domain
severity
description
executor
```

Checklist:

```text id="impl-rule-checklist"
[x] Define QualityRule
[x] Require requirement linkage where appropriate
[x] Define severity
[x] Define executor or adapter reference
[x] Avoid embedding tool-specific behavior in domain model
[x] Add validation tests
```

---

# Phase 2 Exit Criteria

```text id="impl-phase2-exit"
[x] Core domain models implemented
[x] Domain models independent of tool implementations
[x] Unit test coverage established
[x] Static analysis passes
[x] Domain terminology matches normative framework
```

---

# Phase 3 — Quality Evidence

## Objective

Implement structured Quality Evidence capable of supporting reproducible findings and assessments.

---

# Quality Evidence Model

Canonical initial runtime fields:

```text id="impl-evidence-fields"
id
type
source
target
result
created_at
revision
rule_id
requirement_id
tool
tool_version
metadata
artifact
```

Phase 3 runtime contract:

* `id` uses immutable `QualityEvidenceId` with the `QLT-EVID-*` namespace.
* `type` uses immutable validated extensible `QualityEvidenceType`.
* `target` reuses the existing `QualityTarget`.
* `result` uses the dedicated closed `QualityEvidenceResult` vocabulary and
  SHALL NOT reuse `QualityStatus`.
* `rule_id` and `requirement_id` are optional traceability references.
* `QLT-CHECK-*` runtime identity and normalized check execution remain Phase 4
  concerns.
* Evidence persistence, publication, assessment, gates, aggregation, and
  provider-specific execution remain outside this Phase 3 domain-model slice.

Checklist:

```text id="impl-evidence-checklist"
[x] Define QualityEvidence
[x] Define evidence identity
[x] Bind evidence to target
[x] Bind evidence to revision where applicable
[x] Record source
[x] Record verification status
[x] Support tool metadata
[x] Support machine-readable metadata
[x] Test evidence validation
```

---

# Evidence Type

Canonical initial types:

```text id="impl-evidence-types"
TEST
STATIC_ANALYSIS
TYPE_VERIFICATION
ARCHITECTURE
SECURITY
DOCUMENTATION
BUILD
PERFORMANCE
COMPATIBILITY
COMPLIANCE
OBSERVABILITY
MANUAL_REVIEW
METRIC
```

`QualityEvidenceType` SHALL be an immutable validated extensible value object,
not a closed enum and not an arbitrary unvalidated raw string. These values are
semantic categories rather than new `SPEC-0002` persistent identifier
namespaces. `TYPE_VERIFICATION` is the canonical spelling; `TYPE_CHECK` is not
a second runtime alias.

Checklist:

```text id="impl-evidence-type-checklist"
[x] Define initial evidence types
[x] Allow future extension
[ ] Test mapping from adapter results
```

---

# Evidence Result

Canonical initial result vocabulary:

```text id="impl-evidence-results"
PASS
WARNING
FAIL
ERROR
SKIPPED
NOT_APPLICABLE
```

`QualityEvidenceResult` is distinct from `QualityStatus`. `UNKNOWN` remains a
`QualityStatus` concept and SHALL NOT substitute for `NOT_APPLICABLE`.

Malformed or structurally invalid evidence is not represented as a `FAIL` or
`ERROR` evidence result; it is rejected as invalid evidence.

Checklist:

```text id="impl-evidence-result-checklist"
[x] Define QualityEvidenceResult
[x] Keep QualityEvidenceResult distinct from QualityStatus
[x] Define NOT_APPLICABLE semantics
[x] Distinguish invalid evidence from FAIL and ERROR
[x] Test all initial result values
```

---

# Evidence Freshness

```text id="impl-evidence-freshness"
[ ] Define revision freshness rules
[ ] Define stale evidence behavior
[ ] Ensure stale evidence cannot silently satisfy required assessment inputs
[ ] Add freshness tests
```

---

# Evidence Validation

```text id="impl-evidence-validation"
[x] Validate evidence target
[x] Validate revision binding
[x] Validate required metadata
[x] Reject malformed evidence
[x] Distinguish invalid from failed evidence
```

---

# Evidence Serialization

```text id="impl-evidence-serialization"
[ ] Define machine-readable representation
[ ] Add JSON serialization if consistent with project conventions
[ ] Add schema/version field if necessary
[ ] Add round-trip tests
```

---

# Phase 3 Exit Criteria

```text id="impl-phase3-exit"
[x] Quality Evidence model implemented
[x] Evidence can be produced independently of assessments
[ ] Evidence is revision-aware
[x] Evidence validation tests pass
```

## Phase 3 Runtime Closure Evidence

The initial executable Quality Evidence domain-model slice is implemented and
verified by commit `ccd0844`.

This reconciliation intentionally leaves later execution and policy concerns
open:

- adapter-result mapping remains open until Quality tool adapters exist;
- freshness and stale-evidence behavior remain open because revision-bearing
  evidence does not itself define assessment freshness policy;
- serialization remains open because no canonical serialized representation
  has been introduced and the JSON/schema items are conditional;
- `Evidence is revision-aware` remains open until revision freshness/staleness
  semantics are implemented rather than inferred from the presence of a
  `revision` field.

Current executable evidence includes 34 Quality Evidence tests, 81 Quality
domain tests, 6 Quality architecture tests, Ruff PASS, and MyPy PASS across 16
Quality domain source files. No Phase 4+ Quality models, Quality CLI, tool
coupling, evidence persistence, serialization, or freshness policy were
introduced.

This closes only checklist items directly demonstrated by the initial Phase 3
implementation and does not by itself authorize Phase 4 implementation.


---

# Phase 4 — Verification Adapter Contracts

## Objective

Create a common interface between FamilyOS quality semantics and external quality tools.

---

## Phase 4 Runtime Implementation Contract

The initial executable Phase 4 slice SHALL establish the normalized,
tool-independent verification-adapter contract before any concrete later-phase
tool adapter is implemented.

### Quality Check Identity

Phase 4 SHALL introduce immutable `QualityCheckId` using the governed
`QLT-CHECK-*` namespace and the existing Quality identifier validation
strategy. It SHALL validate the namespace and canonical non-empty suffix
without imposing a narrower suffix taxonomy.

Existing examples such as `QLT-CHECK-LINT`, `QLT-CHECK-TYPE`,
`QLT-CHECK-UNIT`, `QLT-CHECK-ARCH`, and `QLT-CHECK-DOC` SHALL remain valid.

### Initial Normalized Result Contract

`QualityCheckResult` SHALL be an immutable application-layer execution result
with exactly these initial semantic fields:

```text
check_id: QualityCheckId
status: QualityStatus
findings: tuple[QualityFinding, ...]
evidence: tuple[QualityEvidence, ...]
duration_seconds: float
diagnostics: tuple[str, ...]
```

`duration_seconds` SHALL be non-negative. Collection fields SHALL be immutable
tuples. Diagnostic entries SHALL be non-empty strings. A `PASS` result SHALL
support zero findings.

The initial result SHALL reuse `QualityStatus`. `FAIL` means reliable execution
that detected a Quality violation. `ERROR` means execution could not reliably
complete or produce a valid conclusion. Timeout, missing executable, tool
crash, and corrupt native result SHALL normally normalize to `ERROR`;
`ERROR` SHALL NOT silently become `PASS`.

The broader automation concept `NOT_APPLICABLE` SHALL NOT be silently added to
`QualityStatus` during this slice. It remains part of the distinct
`QualityEvidenceResult` vocabulary pending explicit future reconciliation.

### Initial Executor Port Contract

Phase 4 SHALL introduce a tool-independent Quality Executor application port
with a simple `execute(...) -> QualityCheckResult` boundary.

The conceptual `prepare() / execute() / collect() / normalize()` sequence does
not require separate public port methods.

The initial port SHALL use only already-authorized Quality runtime concepts and
SHALL NOT introduce `QualityProfile`, gate policy, CI-provider configuration,
or tool-specific configuration.

`QualityRule.executor` remains an opaque logical reference and SHALL NOT become
the runtime executor object.

### Deferred and Conditional Phase 4 Concerns

No canonical reusable FamilyOS command/process abstraction has been identified
as a prerequisite for this slice. The subprocess checklist therefore remains
conditional until a concrete adapter demonstrates the need.

The initial Phase 4 slice SHALL NOT introduce a generic subprocess framework
solely to close checklist items.

Actual stdout/stderr/exit-code capture, timeout handling,
executable-not-found handling, and tool-version collection SHALL remain open
until concrete tool adapters are implemented in their authorized phases.

`QualityEvidence.tool` and `QualityEvidence.tool_version` remain the canonical
descriptive evidence fields when later adapters provide those values.

This reconciliation authorizes only the initial Phase 4 contract slice. It
does not by itself authorize Phase 5 Ruff integration or any later Quality
implementation phase.

---




## Initial Phase 4 Runtime Closure Evidence

The initial Phase 4 Verification Adapter Contract runtime slice is closed by
commit `d2f530b` (`feat(quality): establish verification adapter contracts`).

Runtime evidence for this closure includes:

- immutable `QualityCheckId` using the governed `QLT-CHECK-*` namespace;
- immutable application-layer `QualityCheckResult` with the six reconciled
  normalized result fields;
- explicit `FAIL` versus `ERROR` contract semantics;
- support for multiple findings, zero findings on `PASS`, and attached
  `QualityEvidence`;
- a tool-independent `QualityExecutorPort` using the authorized
  `check_id` / `rule` / `target` execution boundary;
- contract coverage proving explicit check identity preservation;
- architecture protection against premature later-phase Quality models and
  tool-specific Quality-domain coupling;
- 113 targeted Quality tests passing;
- Ruff validation passing; and
- MyPy validation passing across 21 Quality source files.

For this initial closure, 14 of the 25 Phase 4 checklist items are satisfied.
The remaining 11 items intentionally stay open.

Two subprocess-framework items remain conditional because no reusable canonical
FamilyOS command/process abstraction has been established as a prerequisite.
FamilyOS SHALL NOT introduce duplicate or generic execution infrastructure
solely to close those checklist items.

The remaining concrete execution concerns — stdout, stderr, exit-code and
duration capture, timeout and executable-not-found behavior, and tool-version
collection/storage/unavailability handling — remain deferred until authorized
concrete Quality tool adapters demonstrate and implement those behaviors.

`Execution failures normalized` is closed at the stable application-contract
level: reliable Quality violations map to `FAIL`, while execution that cannot
reliably complete or conclude maps to `ERROR`. This closure does not claim
that concrete Ruff, MyPy, Pytest, or other tool failure modes have already been
executed or normalized by adapters.

This closure establishes only the initial Phase 4 verification-adapter
contract. It does not, by itself, authorize Phase 5 Ruff integration or any
later Quality implementation phase.

## Phase 4 Concrete Adapter Reconciliation

Phase 5 Ruff implementation subsequently supplied the concrete execution
evidence intentionally deferred by the initial Phase 4 contract closure.

The canonical Quality Ruff adapter now captures stdout, stderr, exit status,
and execution duration; normalizes timeout and process / OS execution failures
to `ERROR`; probes the Ruff version; stores an available version in
`QualityEvidence.tool_version`; and preserves an unavailable version as a
non-fatal diagnostic when the Ruff quality conclusion itself remains
trustworthy.

The two conditional process-abstraction checklist items are also resolved.
The reconciliation audit found no canonical reusable FamilyOS
`CommandExecutor` / `ProcessExecutor` abstraction that the Quality adapter was
required to reuse. Existing bounded contexts continue to own their
tool-specific subprocess execution. Phase 5 therefore introduced neither a
generic process framework nor duplicate canonical execution infrastructure
solely for Quality.

With this concrete-adapter evidence, all 25 Phase 4 checklist items are
reconciled as satisfied. This retrospective reconciliation does not broaden
Phase 4 authority and does not authorize Phase 6 or any later Quality phase.

---

# Quality Check Result

Define a normalized result model.

Potential fields:

```text id="impl-check-result"
check_id
status
findings
evidence
duration
diagnostics
```

Checklist:

```text id="impl-check-result-checklist"
[x] Define normalized check result
[x] Separate FAIL from ERROR
[x] Support multiple findings
[x] Support zero findings on PASS
[x] Support evidence attachment
```

---

# Quality Executor Contract

Conceptually:

```text id="impl-executor-contract"
prepare()
execute()
normalize()
```

or a simpler interface appropriate to the application architecture.

Checklist:

```text id="impl-executor-checklist"
[x] Define application port for quality executor
[x] Keep subprocess behavior in infrastructure
[x] Define normalized return model
[x] Define error behavior
[x] Add contract tests
```

---

# Subprocess Execution

If a reusable command executor is required:

```text id="impl-subprocess"
[x] Reuse existing FamilyOS process abstraction if available
[x] Avoid introducing duplicate execution infrastructure
[x] Capture stdout
[x] Capture stderr
[x] Capture exit code
[x] Capture duration
[x] Handle timeout
[x] Handle executable-not-found
```

---

# Tool Version Collection

```text id="impl-tool-version"
[x] Collect relevant tool version
[x] Store version in evidence
[x] Handle unavailable version gracefully
```

---

# Phase 4 Exit Criteria

```text id="impl-phase4-exit"
[x] Tool adapter contract stable
[x] Execution failures normalized
[x] Tool-specific details remain infrastructure concerns
[x] Contract tests pass
```

---

# Phase 5 — Ruff Integration

## Objective

Integrate existing Ruff validation into the Quality Framework.

---

## Phase 5 Runtime Implementation Contract

The initial Ruff integration SHALL implement the existing
`QualityExecutorPort` in the Quality infrastructure layer while preserving the
existing Plugin Compliance Ruff validator as a separate bounded-context
workflow.

The canonical invocation is:

```text
<python executable> -m ruff check <target path> --output-format=json
```

with the Python executable defaulting to `sys.executable` and no shell
interpretation.

Initial normalization is governed as follows:

```text
exit 0 + valid JSON     -> PASS
exit 1 + valid JSON     -> FAIL
other exit status       -> ERROR
timeout                 -> ERROR
process / OS failure    -> ERROR
invalid Ruff JSON       -> ERROR
```

For each Ruff violation:

* `QualityFinding.rule_id` comes from the supplied `QualityRule.id`;
* `QualityFinding.domain` comes from the supplied `QualityRule.domain`;
* `QualityFinding.severity` comes from the supplied `QualityRule.severity`;
* the finding status is `FAIL`;
* the Ruff code remains tool-native information and SHALL NOT be promoted to a
  `QLT-RULE-*` identifier;
* message, path, line, and column are preserved where available.

Finding and evidence identities SHALL use injected factories/callables that
return valid `QualityFindingId` and `QualityEvidenceId` values. Phase 5 SHALL
NOT embed random identity generation inside Ruff parsing or introduce a generic
Quality identity framework solely for this adapter.

One governed Ruff execution SHALL initially produce one `QualityEvidence`
record of type `STATIC_ANALYSIS`. The evidence SHALL bind to the supplied
target and rule, use an injected timezone-aware clock for `created_at`, identify
Ruff as the tool, and preserve the Ruff version when available. Produced
findings SHALL reference that evidence identifier.

Revision remains optional in this initial slice. Phase 5 SHALL NOT depend on
Build or Testing source-state contracts merely to populate Quality Evidence
revision, and it does not close the deferred evidence freshness or full
revision-awareness work.

The adapter SHALL attempt:

```text
<python executable> -m ruff --version
```

A version-probe failure alone is non-fatal: `tool_version` MAY remain `None`
and a diagnostic SHALL record the unavailable version without replacing an
otherwise trustworthy Ruff `PASS` or `FAIL` with `ERROR`.

The initial Phase 5 slice MAY introduce a Ruff-specific infrastructure adapter
and focused tests. It SHALL NOT introduce a generic process-execution
framework, depend on Plugin Compliance runtime models, rewrite the existing
Plugin Compliance Ruff validator, or introduce Phase 6+ behavior.

This contract authorizes only the initial Phase 5 Ruff implementation slice.
It does not, by itself, authorize Phase 6 MyPy integration or any later Quality
implementation phase.

## Phase 5 Runtime Closure Evidence

The canonical Ruff runtime slice is implemented by commit `dd5540f`
(`feat(quality): implement canonical ruff executor`) and its real integration
coverage is established by commit `1fd8c1a`
(`test(quality): add real ruff integration coverage`).

Closure evidence includes:

- `RuffQualityExecutor` implementing the existing `QualityExecutorPort` in the
  Quality infrastructure layer;
- canonical execution through the active Python interpreter using
  `python -m ruff check <target path> --output-format=json`;
- normalized `PASS`, `FAIL`, and `ERROR` semantics with reliable Ruff JSON
  parsing;
- governed `QualityFinding` mapping for rule authority, severity, message,
  path, line, and column while preserving native Ruff rule codes as
  tool-specific evidence metadata;
- one governed `STATIC_ANALYSIS` `QualityEvidence` record per Ruff execution
  attempt, including exit status, violation count, native Ruff codes, and
  available Ruff tool version;
- timeout, process / OS failure, invalid JSON, invalid violation payload, and
  inconsistent Ruff protocol behavior normalized to `ERROR`;
- non-fatal Ruff-version unavailability represented by `tool_version=None`
  plus a diagnostic;
- focused adapter unit coverage;
- real Ruff integration coverage for both a valid fixture and an invalid
  `F401` fixture without subprocess mocking;
- preservation of the pre-existing Plugin Compliance Ruff workflow as an
  independent bounded-context implementation;
- 20 tests passing across the canonical Ruff adapter, real integration tests,
  and Plugin Compliance Ruff regression;
- 128 targeted Quality tests passing during staged and post-commit validation;
- Ruff validation passing; and
- MyPy validation passing across the reconciled Quality source/test scope.

All 20 Phase 5 checklist items are therefore satisfied.

This closure authorizes documentary completion of Phase 5 only. Phase 6 MyPy
integration and all later Quality phases remain outside this closure and SHALL
remain open until separately audited and authorized.

---

# Ruff Adapter Checklist

```text id="impl-ruff"
[x] Confirm canonical Ruff command used by FamilyOS
[x] Implement Ruff adapter
[x] Execute Ruff through infrastructure layer
[x] Parse reliable machine-readable output if available
[x] Normalize violations into QualityFinding
[x] Produce QualityEvidence
[x] Distinguish Ruff execution ERROR from lint FAIL
[x] Capture Ruff version
[x] Add adapter unit tests
[x] Add integration tests with valid fixture
[x] Add integration tests with invalid fixture
```

---

# Ruff Finding Mapping

```text id="impl-ruff-mapping"
[x] Map Ruff rule code
[x] Map file path
[x] Map line / column where available
[x] Map message
[x] Map QualitySeverity according to governed policy
```

---

# Phase 5 Exit Criteria

```text id="impl-phase5-exit"
[x] Ruff produces normalized evidence
[x] Ruff failures produce structured findings
[x] Ruff adapter reproducible
[x] Existing Ruff workflow remains functional
```

---

# Phase 6 — MyPy Integration

## Phase 6 MyPy Runtime Contract Reconciliation

The Phase 6 implementation contract is frozen before runtime implementation.

The canonical Quality adapter SHALL implement the existing
`QualityExecutorPort` in the Quality infrastructure layer and execute MyPy as:

```text
<active Python executable> -m mypy <target path> --output=json
```

The runtime SHALL default to `sys.executable`, obtain the governed path from
`QualityTarget.path`, parse MyPy newline-delimited JSON diagnostics, normalize
exit status `0` to `PASS`, exit status `1` with reliable findings to `FAIL`,
and tool/protocol failures to `ERROR`.

### Empty Python Target Compatibility

The existing FamilyOS MyPy behavior for a target containing no `.py` or `.pyi`
source files SHALL be preserved explicitly. The Phase 6 adapter SHALL detect
that condition before the main MyPy execution and normalize it as a
compatibility `PASS` with zero findings, one canonical `TYPE_VERIFICATION`
evidence record with result `PASS`, and the diagnostic
`No Python source files found; nothing to type-check.`

The main MyPy check SHALL NOT run for that target, and a version probe is not
required because no governed MyPy execution occurs.

This narrow compatibility rule SHALL NOT redefine general Quality
applicability. `SKIPPED` is not the correct semantic, and Phase 6 SHALL NOT add
`NOT_APPLICABLE` to `QualityCheckResult` or implement generic applicability
resolution.

`QualityFinding` authority SHALL come from the supplied `QualityRule`:
`rule.id`, `rule.domain`, and `rule.severity`. Native MyPy severity SHALL NOT
be converted into FamilyOS `QualitySeverity`. Native MyPy diagnostic codes
remain tool-specific data and MAY be retained in evidence metadata.

MyPy evidence SHALL use canonical `TYPE_VERIFICATION`,
`source="quality.mypy"`, and `tool="mypy"`. `TYPE_CHECK` remains non-canonical.

The adapter SHALL probe:

```text
<active Python executable> -m mypy --version
```

Available version data SHALL be stored in `tool_version`. Version
unavailability SHALL remain non-fatal when the actual MyPy quality conclusion
is trustworthy and SHALL be surfaced through diagnostics.

The adapter SHALL use injected finding/evidence ID factories, a timezone-aware
evidence clock, a monotonic duration clock, the active Python executable, and
an infrastructure timeout, following the established Ruff adapter precedent.

No generic process framework, Build/Testing coupling, Plugin Compliance
dependency, validator relocation, or Phase 7+ implementation is authorized by
this reconciliation.

All 19 Phase 6 checklist items are satisfied by concrete implementation and
verification evidence and are now closed. Phase 7 and later phases remain open.


## Objective

Integrate FamilyOS static typing verification.

---

# MyPy Adapter Checklist

```text id="impl-mypy"
[x] Confirm canonical MyPy command
[x] Implement MyPy adapter
[x] Parse structured output where practical
[x] Normalize type errors into findings
[x] Produce QualityEvidence
[x] Capture MyPy version
[x] Distinguish execution ERROR from type FAIL
[x] Add passing fixture
[x] Add failing fixture
[x] Add adapter tests
```

---

# MyPy Finding Mapping

```text id="impl-mypy-mapping"
[x] File path
[x] Line
[x] Column where available
[x] MyPy code where available
[x] Message
[x] Severity mapping
```

---

# Phase 6 Exit Criteria

```text id="impl-phase6-exit"
[x] MyPy integrated into common quality model
[x] Type evidence available
[x] Existing MyPy behavior preserved
```

---

# Phase 7 — Pytest Integration

## Objective

Integrate FamilyOS testing results as structured quality evidence while preserving
the Testing Framework as the canonical authority for Pytest execution semantics.

Phase 7 SHALL introduce a Quality-owned Pytest verification adapter without
creating a runtime dependency from Quality on Testing infrastructure. Existing
Testing Framework behavior is semantic authority and SHALL be preserved, but
`PytestRunner` SHALL NOT be reused, moved, or imported into Quality.

---

# Canonical Pytest Runtime Contract

The canonical Quality adapter SHALL be:

```text id="impl-pytest-executor-contract"
PytestQualityExecutor(QualityExecutorPort)
```

The canonical invocation SHALL be:

```text id="impl-pytest-command-contract"
<python executable> -m pytest <target path> --junitxml=<temporary XML report>
```

Pytest native JUnit XML is the structured transport. The temporary report SHALL
be adapter-owned and SHALL NOT leave generated artifacts in the repository.

Phase 7 SHALL NOT add `pytest-json-report` merely for structured output, parse
human terminal output as the authoritative protocol, introduce a generic process
abstraction, create a Quality dependency on `infrastructure.testing`, move/reuse
`PytestRunner`, or authorize Phase 8+ runtime work.

---

# Testing Framework Semantic Authority

The existing Testing Framework remains authoritative for aggregate Pytest status
semantics. Quality SHALL preserve:

```text id="impl-pytest-status-contract"
Pytest exit 0  -> QualityStatus.PASS
Pytest exit 1  -> QualityStatus.FAIL
Pytest exit 2+ -> QualityStatus.ERROR
```

Established Pytest exit codes are:

```text id="impl-pytest-exit-codes"
0 = OK
1 = TESTS_FAILED
2 = INTERRUPTED
3 = INTERNAL_ERROR
4 = USAGE_ERROR
5 = NO_TESTS_COLLECTED
6 = MAX_WARNINGS_ERROR
```

Thus assertion failures and setup/fixture/teardown errors producing exit `1` are
`FAIL`. Collection errors producing exit `2`, interruption, internal/usage
errors, no tests collected (`5`), maximum-warning errors (`6`), timeout,
process-launch failure, and missing/malformed/inconsistent structured output are
`ERROR`.

A JUnit `<error>` element SHALL NOT override the aggregate exit-code mapping.

---

# Pytest Adapter Checklist

```text id="impl-pytest"
[x] Confirm canonical Pytest invocation
[x] Decide structured report format
[x] Implement Pytest adapter
[x] Normalize execution state
[x] Produce test evidence
[x] Capture test counts
[x] Capture failure information
[x] Capture duration
[x] Capture Pytest version
[x] Distinguish infrastructure ERROR from test FAIL
[x] Add adapter tests
```

---

# Test Evidence

Canonical evidence SHALL use:

```text id="impl-pytest-evidence-contract"
type:          TEST
source:        quality.pytest
tool:          pytest
revision:      None
result:        PASS | FAIL | ERROR
```

Evidence metadata SHALL preserve passed, failed, skipped, errors, duration, and
native exit code. Skipped tests SHALL be represented in evidence counts and do
not independently cause `FAIL` when the aggregate result passes.

Checklist:

```text id="impl-test-evidence-checklist"
[x] Represent passing suite
[x] Represent failing suite
[x] Represent collection error
[x] Represent skipped tests
[x] Preserve Testing Framework semantics
```

---

# Failed Test Findings

Initial granularity SHALL be one `QualityFinding` per failed or test-error
testcase when the aggregate result is `FAIL`.

Each finding SHALL preserve governed Quality authority:

```text id="impl-test-finding-authority"
rule_id  = rule.id
domain   = rule.domain
severity = rule.severity
status   = QualityStatus.FAIL
```

Canonical `ERROR` results SHALL NOT require synthetic failed-test findings.
Detailed diagnostics SHALL remain available through result diagnostics and
Quality evidence.

Checklist:

```text id="impl-test-findings-checklist"
[x] Define initial granularity
[x] Avoid excessive finding noise
[x] Preserve detailed diagnostics in evidence
```

---

# Phase 7 Exit Criteria

```text id="impl-phase7-exit"
[x] Pytest evidence integrated
[x] Test failures visible in common quality model
[x] Testing Framework remains authoritative
```

All 22 Phase 7 checklist items are satisfied by concrete implementation and
verification evidence. Phase 8 and later phases remain open.

---

# Phase 8 — Documentation Validation Integration

## Objective

Integrate existing or newly established documentation checks.

---

# Initial Documentation Checks

Potential checks include:

```text id="impl-doc-checks"
Required Files
File Naming
Empty Files
Markdown Structure
Broken Relative References
EPIC Metadata
```

Checklist:

```text id="impl-doc-checklist"
[x] Identify existing documentation validators
[x] Reuse existing validators where available
[x] Implement adapter
[x] Normalize findings
[x] Produce documentation evidence
[x] Add fixtures
[x] Add integration tests
```

---

# EPIC Structure Validation

```text id="impl-epic-structure"
[x] Validate required EPIC files
[x] Validate duplicate chapter detection
[x] Validate empty required file detection
[x] Validate expected control artifacts
```

---

# Markdown Validation

```text id="impl-markdown-validation"
[x] Validate code fence closure
[x] Validate heading rules where deterministic
[x] Validate links where practical
[x] Preserve Documentation Framework authority
```

---

# Phase 8 Exit Criteria

```text id="impl-phase8-exit"
[x] Documentation quality can produce common findings
[x] Validation works on Quality Framework itself
[x] Documentation-specific semantics remain externalized
```

---

## Phase 8 Closure Evidence

Phase 8 is closed against runtime commit `1944a31`
(`feat(quality): implement documentation validation runtime`).

Closure evidence:

- Documentation executor unit validation: **19 / 19 PASS**.
- Real Documentation integration validation: **2 / 2 PASS**.
- Combined Documentation validation slice: **21 / 21 PASS**.
- Quality regression at the runtime gate: **186 / 186 PASS**.
- Ruff validation: **PASS**.
- MyPy validation: **PASS**.
- Real canonical EPIC validation on `EPIC-COM-001`: **PASS**, zero violations.
- Quality Framework self-validation on `EPIC-QLT-001`: execution **PASS**;
  the validator deterministically reports **32** existing `markdown_heading`
  documentation violations and normalizes them through the common Quality model.
- Documentation-specific semantic authority remains with `EPIC-DOC-001`; Quality
  owns execution orchestration and common finding/evidence normalization only.
- Documentation semantics are implemented outside the Quality infrastructure package
  under `familyos_cli.infrastructure.documentation`; the Documents Plugin validator is
  not used as the Documentation Framework validation engine.

The Phase 8 exit criterion that validation works on the Quality Framework itself is a
capability/execution criterion; it does **not** assert that the existing
`EPIC-QLT-001` documentation is conformant. The 32 existing heading violations remain
a separate documentation-conformance/migration concern. Any later gate that explicitly
requires Documentation Validation to **PASS** remains open until its own evidence is
satisfied.

## Canonical Runtime Contract

Phase 8 SHALL integrate documentation validation through a Quality-owned
`DocumentationQualityExecutor` implementing `QualityExecutorPort`.

EPIC-DOC-001 remains authoritative for documentation-specific semantics.
The Quality Framework owns execution orchestration and normalization into the
common Quality model; it SHALL NOT redefine Documentation Framework ownership.

The Documents Plugin `DocumentValidator` is not the Phase 8 validation engine
and SHALL NOT be used as the Documentation Framework validator.

### Execution Boundary

The executor SHALL validate the local filesystem target identified by
`QualityTarget.path`.

The initial Phase 8 implementation SHALL be deterministic and local:

- no subprocess-based documentation validator is required;
- no external Markdown linter dependency is required;
- PyYAML MAY be used for YAML parsing;
- external HTTP link verification is outside the initial runtime slice.

A missing `target.path`, an inaccessible validation target, or an unexpected
validator/infrastructure failure SHALL produce `QualityStatus.ERROR`.

Ordinary documentation violations discovered by a successfully executed
validator SHALL produce `QualityStatus.FAIL`, not `ERROR`.

### Initial Validation Scope

The initial runtime slice SHALL cover:

- canonical EPIC structure and required control artifacts;
- required numbered chapter presence and naming consistency;
- duplicate numbered chapter detection;
- non-empty required files;
- `EPIC.yaml` presence and YAML parse validity;
- basic Markdown structural integrity, including fenced-code-block balance and
  heading structure;
- local relative Markdown reference integrity.

Malformed `EPIC.yaml`, a missing required document, an empty required document,
an invalid canonical name, an unbalanced Markdown fence, or a broken local
relative reference are documentation violations and therefore SHALL normalize
to `FAIL` with actionable findings.

### Quality Normalization

The canonical evidence type SHALL be `DOCUMENTATION`.
The canonical evidence source SHALL be `quality.documentation`.
The canonical tool identity SHALL be `familyos-documentation-validator`.
The Quality domain for governed documentation rules SHALL be `QLT-DOM-DOC`.

Each execution SHALL produce one aggregate `DOCUMENTATION` evidence record.

A successful validation with no violations SHALL produce `QualityStatus.PASS`,
`QualityEvidenceResult.PASS`, and no findings.

A successful validation with one or more documentation violations SHALL produce
`QualityStatus.FAIL`, `QualityEvidenceResult.FAIL`, and one actionable
`QualityFinding` per reported violation.

An execution that cannot reliably complete SHALL produce
`QualityStatus.ERROR`, `QualityEvidenceResult.ERROR` when execution evidence
can be produced, no synthetic documentation-violation findings, and diagnostic
information describing the execution failure.

Findings SHALL preserve the governed rule identifier, domain, severity, target,
location when available, and aggregate evidence identifier.

The evidence revision SHALL preserve `QualityTarget.revision`.

### Ownership and Deferred Scope

EPIC-DOC-001 remains the semantic authority for documentation standards,
structure, lifecycle, governance, naming, metadata, and reference expectations.

Phase 8 SHALL NOT introduce a generic subprocess abstraction or transfer
Documentation Framework semantic ownership into Quality.

Full Markdown linting, remote/external URL availability checks, generalized
schema-validation infrastructure, and broader documentation-policy engines are
deferred unless separately authorized.

These contract decisions freeze the implementation boundary only. They do not,
by themselves, satisfy or close any Phase 8 checklist item.

# Phase 9 — Plugin Compliance Integration

## Objective

Integrate EPIC-PLUGIN-002 without duplicating its compliance engine.

---

# Plugin Compliance Adapter

```text id="impl-plugin-compliance"
[x] Identify authoritative plugin compliance API / service / CLI
[x] Define integration boundary
[x] Consume plugin compliance result
[x] Map compliance evidence
[x] Map compliance findings
[x] Preserve plugin rule identities
[x] Preserve severity semantics
[x] Add integration tests
```

---

# Official Plugin Target

```text id="impl-official-plugin"
[x] Support official plugin QualityTarget
[x] Resolve plugin compliance profile
[x] Bind compliance result to plugin revision
```

---

# No Duplication Check

```text id="impl-no-duplication"
[x] Quality Framework does not recreate plugin compliance rules
[x] Quality Framework does not redefine plugin compliance profiles
[x] Quality Framework consumes authoritative plugin compliance output
```

---

# Phase 9 Exit Criteria

```text id="impl-phase9-exit"
[x] Plugin compliance participates in quality evidence
[x] Official plugin assessments can consume compliance state
```

---


## Phase 9 Closure Evidence

Phase 9 is closed against runtime commit `e9a034b`
(`feat(quality): integrate plugin compliance execution`) and real integration
commit `2dd4b1d`
(`test(quality): integrate authoritative plugin compliance`).

The governing Phase 9 runtime contract was frozen by commit `82ca5df`
(`docs(quality): freeze phase 9 plugin compliance contract`).

Closure evidence:

- Focused Plugin Compliance Quality executor unit validation: **21 / 21 PASS**.
- Real Plugin Compliance Quality integration validation: **2 / 2 PASS**.
- Quality regression at the integration gate: **211 / 211 PASS**.
- Ruff validation: **PASS**.
- MyPy validation: **PASS**.
- Quality consumes the authoritative
  `ComplianceEngine.evaluate(ComplianceRequest) -> ComplianceResult` boundary.
- The governed `official` Plugin Compliance profile is resolved through the
  existing Plugin Compliance infrastructure; Quality does not recreate or
  redefine that profile.
- Real official-plugin integration is demonstrated with `familyos.security`.
- Real non-compliant integration is demonstrated with the canonical
  `acme.broken` scenario.
- Plugin Compliance status is normalized into the common Quality status model
  without recomputing the authoritative compliance decision.
- Plugin Compliance findings and evidence participate in the common Quality
  finding/evidence model while preserving source Plugin rule identity,
  severity, evidence identity, plugin identity/version, and other governed
  provenance.
- `QualityTarget.revision` is bound to normalized Quality evidence without
  mutating or extending the authoritative `ComplianceResult`.
- The no-duplication gate confirms that Quality introduces no duplicate Plugin
  Compliance rule catalog, official profile, validator registry, compliance
  decision evaluator, or second compliance engine.
- Official plugin Quality assessments can therefore consume authoritative
  Plugin Compliance state through the Phase 9 Quality executor boundary.

Phase 9 closes the Plugin Compliance integration slice only. EPIC-PLUGIN-002
remains authoritative for plugin-specific compliance rules, profiles,
validators, findings, evidence semantics, severity semantics, and compliance
decisions. Phase 10 and later Quality Framework behavior remain outside this
closure and are not authorized or satisfied by Phase 9 completion.

## Phase 9 Runtime Contract Freeze

The Phase 9 runtime integration SHALL consume the existing
EPIC-PLUGIN-002 Plugin Compliance Framework as an authoritative bounded
context. Quality SHALL normalize Plugin Compliance output into Quality
models without recreating Plugin Compliance rules, profiles, validators,
or compliance-decision semantics.

### Authority and execution boundary

- EPIC-PLUGIN-002 remains authoritative for plugin compliance rules,
  profiles, validator execution, rule outcomes, finding semantics,
  evidence semantics, severity semantics, and the overall compliance
  decision.
- The authoritative execution API is
  `ComplianceEngine.evaluate(ComplianceRequest) -> ComplianceResult`.
- Quality SHALL consume the structured `ComplianceResult`; it SHALL NOT
  invoke Plugin Compliance validators individually or reproduce the
  compliance evaluation algorithm.
- The Plugin Compliance application/CLI surfaces remain consumers of the
  same engine and are not reimplemented inside Quality.

### Official plugin target and profile

Phase 9 freezes the canonical Quality-side plugin target shape as:

```text
QualityTarget(
    target_type="plugin",
    identifier=<canonical PluginDescriptor.id>,
    version=<PluginDescriptor.version>,
    path=<PluginDescriptor.path>,
    revision=<Quality execution revision, optional>,
)
```

- `target_type="plugin"` is the canonical Quality target type for this
  integration.
- `identifier` is the canonical plugin identity and SHALL equal the
  resolved `PluginDescriptor.id`.
- `version` SHALL represent the resolved `PluginDescriptor.version`.
- `path` SHALL identify the resolved plugin path used for discovery and
  execution; path does not replace plugin identity.
- `revision` belongs to the Quality execution context and is optional.
- The governed Plugin Compliance profile is identified by `official`.
- Plugin descriptor discovery and profile resolution remain owned by the
  existing Plugin Compliance/plugin infrastructure. Quality SHALL NOT
  recreate `OFFICIAL_PROFILE`, its included rules, mandatory rules,
  exclusions, or blocking severity threshold.
- Plugin identity and plugin version returned by `ComplianceResult` SHALL
  remain traceable in the normalized Quality output.

### Compliance decision normalization

`ComplianceResult.status` is authoritative. Quality SHALL NOT recompute
compliance from rule evaluations, findings, mandatory flags, or severity
thresholds.

The Phase 9 status normalization contract is:

```text
ComplianceStatus.COMPLIANT     -> QualityStatus.PASS
ComplianceStatus.NON_COMPLIANT -> QualityStatus.FAIL
ComplianceStatus.INCOMPLETE    -> QualityStatus.WARNING
ComplianceStatus.ERROR         -> QualityStatus.ERROR
```

An integration/runtime failure that prevents a reliable Plugin Compliance
assessment SHALL produce `QualityStatus.ERROR`; it SHALL NOT be
misrepresented as ordinary plugin non-compliance.

### Finding normalization and rule identity

- Plugin Compliance findings SHALL be normalized into `QualityFinding`
  values.
- `QualityFinding.rule_id` SHALL remain the `QualityRule.id` supplied to
  the Quality executor and therefore remains in the canonical
  `QLT-RULE-*` namespace.
- `ComplianceFinding.rule_id` remains the authoritative source Plugin
  Compliance rule identity and SHALL be preserved explicitly as
  provenance in normalized output.
- Quality SHALL NOT rewrite a `PLUGIN-*` rule id into a fabricated
  `QLT-RULE-*` id, nor create replacement Plugin Compliance rules.
- Finding message, location, source evidence references, category, source
  status, source domain, and source Plugin rule id SHALL be preserved
  directly where the Quality model supports them and otherwise through
  deterministic metadata or diagnostics.
- Quality finding identifiers and Quality evidence identifiers remain in
  their canonical `QLT-*` namespaces; source Plugin identifiers SHALL be
  preserved as provenance rather than silently rewritten.

### Severity preservation

Plugin Compliance severity and Quality severity are distinct governed
vocabularies:

```text
Plugin Compliance: INFO, WARNING, ERROR, CRITICAL
Quality:           INFO, LOW, MEDIUM, HIGH, CRITICAL
```

Phase 9 SHALL NOT invent a cross-vocabulary conversion such as
`WARNING -> MEDIUM` or `ERROR -> HIGH`.

For every normalized `QualityFinding`:

```text
QualityFinding.severity = QualityRule.severity
```

The Quality rule supplied to the executor remains authoritative for
FamilyOS `QualitySeverity`. The original `ComplianceFinding.severity`
remains authoritative Plugin Compliance provenance and SHALL be preserved
explicitly in normalized output. Source Plugin severity SHALL NOT alter,
replace, or feed back into the authoritative Plugin Compliance decision
or the governed Quality rule severity.

Tests SHALL cover all Plugin Compliance source severity values and prove
that source severity provenance is preserved independently from
`QualityRule.severity`.

### Evidence normalization

- `ComplianceEvidence` SHALL be consumed as authoritative source evidence
  and normalized into `QualityEvidence`.
- Source evidence identity and provenance SHALL remain traceable,
  including the Plugin Compliance evidence id, evidence type, source,
  producer, producer version, plugin id, plugin version, scope, trust
  level, and collection time where representable.
- Quality SHALL use its own canonical `QualityEvidenceId` namespace for
  normalized evidence and SHALL retain source Plugin evidence identifiers
  as provenance.
- Plugin Compliance payload content SHALL not be reinterpreted as new
  compliance policy by Quality.
- Phase 9 SHALL NOT invent a parallel evidence framework.

### Revision binding

`ComplianceResult` carries plugin identity and plugin version but does not
define a plugin revision field. Revision binding therefore belongs to the
Quality execution context:

```text
authoritative ComplianceResult
          +
QualityTarget.revision
          |
          v
normalized QualityEvidence.revision
```

Quality SHALL bind normalized compliance evidence to
`QualityTarget.revision` when a revision is supplied. It SHALL NOT mutate
`ComplianceResult` or imply that Plugin Compliance produced a revision it
does not own.

### No-duplication invariant

Phase 9 SHALL NOT introduce:

- a duplicate Plugin Compliance rule catalog;
- a duplicate official compliance profile;
- a duplicate Plugin Compliance validator registry;
- a duplicate compliance decision evaluator;
- a second compliance engine;
- a generic replacement abstraction that changes EPIC-PLUGIN-002
  ownership.

The Quality-side implementation is an adapter/normalizer around the
authoritative Plugin Compliance output.

### Verification contract

Phase 9 implementation evidence SHALL include focused unit tests and real
integration tests covering at least:

- official profile resolution through Plugin Compliance;
- compliant official-plugin normalization;
- non-compliant plugin normalization;
- incomplete and error status normalization;
- Plugin rule identity preservation;
- all Plugin severity normalization cases while preserving source
  severity provenance;
- Plugin finding normalization;
- Plugin evidence normalization and provenance;
- plugin id/version traceability;
- `QualityTarget.revision` binding;
- failure behavior that produces Quality `ERROR`;
- proof that Quality consumes the authoritative Plugin Compliance engine
  rather than recreating its rules or profiles.

This contract freezes the intended Phase 9 integration boundary only. It
does not constitute runtime implementation evidence and does not close
any Phase 9 checklist item.

---

# Phase 10 — Quality Assessment Model

## Objective

Implement a reproducible assessment that combines evidence and findings into a target-level quality state.

---

# Quality Assessment

Suggested initial fields:

```text id="impl-assessment-fields"
id
target
revision
profile
status
quality_state
evidence_ids
finding_ids
created_at
```

Checklist:

```text id="impl-assessment-checklist"
[ ] Define QualityAssessment
[ ] Define assessment identity
[ ] Define revision binding
[ ] Define profile reference
[ ] Define assessment status
[ ] Define quality state
[ ] Add serialization tests
```

---

# Initial Quality States

Potential states:

```text id="impl-quality-states"
PASS
PASS_WITH_WARNINGS
FAIL
UNKNOWN
```

Add `CONDITIONAL` only when exception/risk semantics are implemented.

Checklist:

```text id="impl-quality-state-checklist"
[ ] Define state semantics
[ ] Ensure UNKNOWN cannot become PASS
[ ] Add aggregation tests
```

---

# Assessment Aggregation

Initial deterministic rules may be:

```text id="impl-assessment-rules"
Any blocking finding
      → FAIL

No blocking findings + warnings
      → PASS_WITH_WARNINGS

All required checks PASS
      → PASS

Missing required evidence
      → UNKNOWN
```

Checklist:

```text id="impl-assessment-aggregation"
[ ] Implement deterministic aggregation
[ ] Test all state transitions
[ ] Test missing evidence
[ ] Test adapter ERROR
[ ] Test warning-only case
```

---

# Assessment Service

```text id="impl-assessment-service"
[ ] Define application service
[ ] Accept target and profile
[ ] Execute or consume required checks
[ ] Collect evidence
[ ] Collect findings
[ ] Produce assessment
```

---

# Phase 10 Exit Criteria

```text id="impl-phase10-exit"
[ ] Reproducible QualityAssessment available
[ ] Assessment requires complete required evidence
[ ] Assessment tests pass
```

---

# Phase 11 — Quality Profiles

## Objective

Define reusable quality expectations for target categories.

---

# Profile Model

Suggested fields:

```text id="impl-profile-fields"
id
version
target_types
required_checks
required_domains
severity_policy
```

Checklist:

```text id="impl-profile-checklist"
[ ] Define QualityProfile
[ ] Define profile identity
[ ] Define profile version
[ ] Define required checks
[ ] Define applicability
[ ] Add profile validation
```

---

# Initial Profiles

Recommended initial profiles:

```text id="impl-initial-profiles"
familyos-repository
familyos-official-plugin
familyos-documentation
```

Later:

```text id="impl-later-profiles"
familyos-release
familyos-critical-release
```

---

# Repository Profile

Potential requirements:

```text id="impl-repository-profile"
Ruff
MyPy
Pytest
Documentation Structure
```

---

# Official Plugin Profile

Potential requirements:

```text id="impl-plugin-profile"
Repository Base
Plugin Compliance
Plugin Tests
Plugin Documentation
Architecture Checks
```

---

# Profile Tests

```text id="impl-profile-tests"
[ ] Valid profile loads
[ ] Unknown check rejected
[ ] Duplicate check behavior defined
[ ] Missing required field rejected
[ ] Version represented
```

---

# Phase 11 Exit Criteria

```text id="impl-phase11-exit"
[ ] Profile resolution works
[ ] Assessments use profiles
[ ] Profiles are version-controlled
```

---

# Phase 12 — Quality CLI

## Objective

Expose the first usable Quality Framework interface through the FamilyOS CLI.

---

# Initial Commands

Recommended initial commands:

```text id="impl-cli-initial"
familyos quality check
familyos quality assess
familyos quality report
```

---

# `quality check`

Responsibilities:

```text id="impl-cli-check"
[ ] Resolve target
[ ] Resolve profile
[ ] Execute quality checks
[ ] Display check results
[ ] Return meaningful exit code
```

---

# `quality assess`

Responsibilities:

```text id="impl-cli-assess"
[ ] Produce QualityAssessment
[ ] Display overall state
[ ] Display blocking findings
[ ] Display evidence summary
```

---

# `quality report`

Responsibilities:

```text id="impl-cli-report"
[ ] Produce human-readable report
[ ] Support structured output where useful
[ ] Preserve stable field semantics
```

---

# CLI Exit Codes

Define explicit behavior.

Conceptually:

```text id="impl-cli-exit-codes"
0
PASS

non-zero quality-specific code
FAIL

different non-zero code
ERROR
```

Checklist:

```text id="impl-cli-exit-checklist"
[ ] Define exit code policy
[ ] Document it
[ ] Test it
```

---

# CLI Architecture

```text id="impl-cli-architecture"
[ ] Follow FamilyOS CLI Architecture
[ ] Keep business logic out of CLI layer
[ ] Reuse application services
[ ] Add command tests
[ ] Add help text tests where appropriate
```

---

# Phase 12 Exit Criteria

```text id="impl-phase12-exit"
[ ] Local quality command available
[ ] Local results match application-layer semantics
[ ] CLI tests pass
```

---

# Phase 13 — CI Integration

## Objective

Run the same Quality Framework logic automatically in CI.

---

# CI Integration Principle

```text id="impl-ci-principle"
Local Quality Logic
      =
CI Quality Logic
```

The CI pipeline should invoke application capabilities rather than reimplement quality policy.

---

# CI Checklist

```text id="impl-ci-checklist"
[ ] Identify current CI provider/workflow
[ ] Add Quality Framework command
[ ] Generate structured report artifact
[ ] Preserve logs
[ ] Surface findings clearly
[ ] Distinguish quality FAIL from automation ERROR
[ ] Test CI failure behavior
```

---

# Pull Request Workflow

```text id="impl-pr-workflow"
[ ] Run required quality profile
[ ] Produce assessment
[ ] Publish actionable summary
[ ] Preserve report artifact
```

---

# Main Branch Workflow

```text id="impl-main-workflow"
[ ] Run required repository profile
[ ] Run full relevant tests
[ ] Persist authoritative evidence as needed
```

---

# Phase 13 Exit Criteria

```text id="impl-phase13-exit"
[ ] Quality checks automated in CI
[ ] CI and local semantics aligned
[ ] CI failures actionable
```

---

# Phase 14 — Architecture Quality Checks

## Objective

Introduce deterministic architecture protection where the current architecture already defines enforceable boundaries.

---

# Initial Architecture Rules

Potential rules include:

```text id="impl-architecture-rules"
Core does not import plugin implementation
Domain does not import infrastructure
Reserved package boundaries respected
Official plugin structure respected
```

Checklist:

```text id="impl-architecture-rule-checklist"
[ ] Identify authoritative architecture decisions
[ ] Define first architecture requirements
[ ] Implement deterministic validator
[ ] Produce architecture findings
[ ] Produce evidence
[ ] Add compliant fixtures
[ ] Add violating fixtures
```

---

# Architecture Rule Governance

```text id="impl-architecture-governance"
[ ] Rule linked to ADR / architecture authority
[ ] Rule severity defined
[ ] Rule owner defined
[ ] Rule rollout starts non-blocking if necessary
```

---

# Phase 14 Exit Criteria

```text id="impl-phase14-exit"
[ ] Initial architecture invariants machine-verifiable
[ ] No undocumented architecture policy introduced
```

---

# Phase 15 — Non-Blocking Quality Gates

## Objective

Introduce gate evaluation without initially blocking engineering progression.

---

# Gate Model

Suggested fields:

```text id="impl-gate-fields"
id
target
revision
policy
assessment_id
decision
blocking_conditions
evaluated_at
```

Checklist:

```text id="impl-gate-model"
[ ] Define QualityGate
[ ] Define GateDecision
[ ] Define policy representation
[ ] Define decision explanation
[ ] Add tests
```

---

# Initial Gate

Recommended first gate:

```text id="impl-first-gate"
Merge Readiness Gate
```

Initially in observation mode.

---

# Observation Mode

```text id="impl-gate-observe"
[ ] Gate evaluates PR quality
[ ] Gate reports would-pass / would-fail
[ ] Gate does not block merge
[ ] Collect false-positive feedback
[ ] Collect execution reliability metrics
```

---

# Gate Explainability

```text id="impl-gate-explainability"
[ ] Gate identifies blocking assessment
[ ] Gate identifies blocking finding
[ ] Gate identifies rule
[ ] Gate identifies evidence
```

---

# Phase 15 Exit Criteria

```text id="impl-phase15-exit"
[ ] Gate decisions deterministic
[ ] Gate diagnostics useful
[ ] Reliability demonstrated before enforcement
```

---

# Phase 16 — Blocking Merge Gate

## Objective

Promote trusted merge quality policy into enforcement.

---

# Preconditions

```text id="impl-merge-gate-preconditions"
[ ] Required checks stable
[ ] False-positive rate acceptable
[ ] Local reproduction available
[ ] Assessment semantics stable
[ ] Gate observation period complete
[ ] Governance approval obtained
```

---

# Merge Gate Policy

Potential initial requirements:

```text id="impl-merge-gate-policy"
Ruff PASS
MyPy PASS
Pytest PASS
Required Documentation Validation PASS
Required Plugin Compliance PASS where applicable
No blocking QualityFinding
```

---

# Repository Protection

```text id="impl-repository-protection"
[ ] Configure protected branch integration
[ ] Ensure gate binds to exact revision
[ ] Prevent stale PASS reuse
[ ] Document bypass policy
```

---

# Phase 16 Exit Criteria

```text id="impl-phase16-exit"
[ ] Merge gate blocks unacceptable state
[ ] Valid state merges normally
[ ] Gate cannot silently skip required checks
```

---

# Phase 17 — Quality Risk Model

## Objective

Introduce structured Quality Risk once findings and assessments are stable.

---

# Quality Risk Model

Potential fields:

```text id="impl-risk-fields"
id
title
description
domain
target
likelihood
impact
severity
owner
mitigation
status
```

Checklist:

```text id="impl-risk-checklist"
[ ] Define QualityRisk
[ ] Define likelihood scale
[ ] Define impact scale
[ ] Define risk severity semantics
[ ] Define ownership
[ ] Define lifecycle
[ ] Add tests
```

---

# Initial Risk Workflow

```text id="impl-risk-workflow"
[ ] Create risk manually from significant finding
[ ] Link finding to risk
[ ] Record mitigation
[ ] Support risk closure
```

Automation can come later.

---

# Phase 17 Exit Criteria

```text id="impl-phase17-exit"
[ ] Significant quality risks structured
[ ] Risks traceable to findings/evidence
```

---

# Phase 18 — Defect and Quality Debt Management

## Objective

Introduce persistent management of known quality deficiencies.

---

# Defect Model

Potential fields:

```text id="impl-defect-fields"
id
title
description
severity
priority
target
owner
status
finding_ids
evidence_ids
```

Checklist:

```text id="impl-defect-checklist"
[ ] Define defect model
[ ] Define lifecycle
[ ] Link findings
[ ] Link evidence
[ ] Add closure verification
```

---

# Quality Debt Model

Potential fields:

```text id="impl-debt-fields"
id
title
description
domain
target
risk
owner
status
reason
remediation_plan
```

Checklist:

```text id="impl-debt-checklist"
[ ] Define QualityDebt
[ ] Define ownership
[ ] Define lifecycle
[ ] Link originating finding / defect / exception
[ ] Define remediation verification
```

---

# Initial Debt Register

```text id="impl-debt-register"
[ ] Start with repository-backed structured records
[ ] Avoid database until operational need exists
[ ] Support human-readable review
```

---

# Phase 18 Exit Criteria

```text id="impl-phase18-exit"
[ ] Significant known quality debt cannot disappear silently
[ ] Defect/debt ownership visible
```

---

# Phase 19 — Compliance Model

## Objective

Introduce reusable compliance evaluation using existing requirements and evidence.

---

# Compliance Result

Potential states:

```text id="impl-compliance-states"
COMPLIANT
COMPLIANT_WITH_EXCEPTIONS
NON_COMPLIANT
INCOMPLETE
ERROR
```

Checklist:

```text id="impl-compliance-checklist"
[ ] Define ComplianceResult
[ ] Define requirement-level result
[ ] Implement aggregation
[ ] Ensure missing mandatory evidence → INCOMPLETE
[ ] Add tests
```

---

# Compliance Profile Integration

```text id="impl-compliance-profile"
[ ] Reuse QualityRequirement
[ ] Reuse QualityProfile where practical
[ ] Reuse QualityEvidence
[ ] Avoid parallel duplicate compliance domain model unless justified
```

---

# Phase 19 Exit Criteria

```text id="impl-phase19-exit"
[ ] Repository or plugin can produce compliance result
[ ] Compliance state traceable to requirements and evidence
```

---

# Phase 20 — Exception Model

## Objective

Introduce controlled quality exceptions only after normal quality enforcement exists.

---

# Exception Model

Potential fields:

```text id="impl-exception-fields"
id
requirement_id
target
reason
risk
owner
authority
created_at
expires_at
status
```

Checklist:

```text id="impl-exception-checklist"
[ ] Define QualityException
[ ] Require scope
[ ] Require reason
[ ] Require owner
[ ] Require authority
[ ] Support expiration
[ ] Validate matching requirement
[ ] Validate matching target
```

---

# Exception Integration

```text id="impl-exception-integration"
[ ] Assessment can expose active exception
[ ] Compliance can produce COMPLIANT_WITH_EXCEPTIONS
[ ] Gate can validate exception
[ ] Expired exception no longer changes decision
```

---

# Phase 20 Exit Criteria

```text id="impl-phase20-exit"
[ ] Exceptions are explicit and traceable
[ ] No silent suppression mechanism substitutes for exceptions
```

---

# Phase 21 — Release Gate

## Objective

Apply the Quality Framework to FamilyOS release readiness.

---

# Preconditions

```text id="impl-release-gate-preconditions"
[ ] Merge quality pipeline mature
[ ] Full test evidence reliable
[ ] Build evidence available
[ ] Release Framework integration defined
[ ] Release assessment model stable
```

---

# Initial Release Gate Inputs

Potential inputs:

```text id="impl-release-gate-inputs"
Full Test Evidence
Static Analysis
Build Validation
Documentation Validation
Plugin Compliance
Open Critical Findings
Open Critical Risks
Exceptions
```

---

# Release Gate Checklist

```text id="impl-release-gate-checklist"
[ ] Define release gate profile
[ ] Bind gate to release candidate revision
[ ] Integrate Build Framework evidence
[ ] Integrate Release Framework lifecycle
[ ] Produce gate evidence
[ ] Add release gate tests
```

---

# Phase 21 Exit Criteria

```text id="impl-phase21-exit"
[ ] Release quality decision explicit
[ ] Release cannot silently ignore required quality state
```

---

# Phase 22 — Quality Observability

## Objective

Retain and expose quality history.

---

# Initial Historical Record

Recommended fields:

```text id="impl-history-fields"
timestamp
target
revision
profile
assessment_state
finding_summary
gate_state
duration
```

---

# Initial Storage

```text id="impl-history-storage"
[ ] Evaluate repository artifacts first
[ ] Evaluate CI artifacts
[ ] Avoid centralized service until needed
```

---

# Initial Quality Report

```text id="impl-quality-report"
[ ] Current quality status
[ ] Findings by severity
[ ] Assessment
[ ] Gate state
[ ] Check duration
```

---

# Historical Queries

```text id="impl-history-queries"
[ ] Latest assessment
[ ] Assessment by revision
[ ] Findings by severity
[ ] Recent gate failures
```

---

# Phase 22 Exit Criteria

```text id="impl-phase22-exit"
[ ] Quality state no longer exists only in ephemeral CI logs
[ ] Basic trend analysis possible
```

---

# Phase 23 — Quality Metrics

## Objective

Introduce a minimal decision-oriented metric set.

---

# Initial Metrics

Recommended:

```text id="impl-initial-metrics"
Check Duration
Test Duration
Automation Error Rate
Critical Finding Count
Gate Failure Count
Quality Debt Count by Severity
```

---

# Metric Definition Checklist

For every metric:

```text id="impl-metric-checklist"
[ ] Purpose defined
[ ] Calculation defined
[ ] Source defined
[ ] Owner defined
[ ] Interpretation documented
[ ] Misuse risk considered
```

---

# Avoid Early Metric Explosion

```text id="impl-metric-avoid"
[ ] Do not add metric without decision use
[ ] Do not use individual developer productivity metrics
[ ] Do not use one aggregate quality score as authority
```

---

# Phase 23 Exit Criteria

```text id="impl-phase23-exit"
[ ] Metrics support real quality decisions
[ ] Metrics are observable over time
```

---

# Phase 24 — Continuous Improvement Workflow

## Objective

Use accumulated quality data to drive systemic engineering improvement.

---

# Improvement Model

Potential fields:

```text id="impl-improvement-fields"
id
problem
source
expected_outcome
priority
owner
status
validation
```

---

# Improvement Triggers

```text id="impl-improvement-triggers"
[ ] Repeated defect
[ ] Repeated gate failure
[ ] Growing debt
[ ] Automation instability
[ ] Significant incident
[ ] Repeated exception
```

---

# Root Cause Analysis

```text id="impl-root-cause"
[ ] Define lightweight RCA template
[ ] Link RCA to defect / incident
[ ] Record systemic improvement action
```

---

# Regression Prevention

```text id="impl-regression-prevention"
[ ] Evaluate regression test for significant defect
[ ] Evaluate new QualityRule
[ ] Evaluate documentation improvement
[ ] Evaluate architecture constraint
```

---

# Phase 24 Exit Criteria

```text id="impl-phase24-exit"
[ ] Repeated quality problems produce systemic improvements
[ ] Improvement effectiveness can be validated
```

---

# Phase 25 — Governance Registry

## Objective

Make authoritative quality ownership and policy discoverable.

---

# Initial Registry Scope

Potential registry entries:

```text id="impl-governance-registry"
QualityRequirement
QualityRule
QualityProfile
QualityGate
QualityException
Owner
Authority
```

---

# Repository-Based Registry

Prefer version-controlled registry files initially.

Checklist:

```text id="impl-registry-checklist"
[ ] Define registry format
[ ] Validate identifiers
[ ] Validate owners
[ ] Validate requirement-rule references
[ ] Validate profile references
[ ] Validate gate references
```

---

# Governance Findings

Automatically detect:

```text id="impl-governance-findings"
Unknown Owner
Unknown Requirement
Unknown Rule
Expired Exception
Broken Gate Profile
Duplicate Identifier
```

---

# Phase 25 Exit Criteria

```text id="impl-phase25-exit"
[ ] Important quality authority discoverable
[ ] Governance configuration machine-validatable
```

---

# Phase 26 — Framework Lifecycle Automation

## Objective

Make Quality Framework evolution itself machine-visible.

---

# Lifecycle Registry

```text id="impl-lifecycle-registry"
[ ] Add framework version
[ ] Add rule lifecycle status
[ ] Add profile lifecycle status
[ ] Add gate lifecycle status
[ ] Add deprecation metadata
[ ] Add replacement metadata
```

---

# Deprecation Validation

```text id="impl-deprecation-validation"
[ ] Detect deprecated rule usage
[ ] Detect retired profile usage
[ ] Detect expired migration windows
[ ] Report remaining legacy targets
```

---

# Phase 26 Exit Criteria

```text id="impl-phase26-exit"
[ ] Framework lifecycle state visible
[ ] Deprecated capabilities move toward retirement
```

---

# Phase 27 — Performance and Incremental Quality Execution

## Objective

Improve feedback speed without weakening assurance.

---

# Performance Baseline

```text id="impl-performance-baseline"
[ ] Measure current quality pipeline duration
[ ] Measure each check duration
[ ] Identify dominant bottlenecks
```

---

# Parallelization

```text id="impl-parallelization"
[ ] Identify independent checks
[ ] Execute safely in parallel
[ ] Preserve deterministic aggregation
```

---

# Caching

```text id="impl-caching"
[ ] Define cache keys
[ ] Include revision/config/tool version
[ ] Test invalidation
[ ] Prefer recomputation when uncertain
```

---

# Incremental Checks

```text id="impl-incremental"
[ ] Classify change scope
[ ] Resolve affected checks
[ ] Validate dependency analysis
[ ] Use conservative fallback
[ ] Retain periodic full validation
```

---

# Phase 27 Exit Criteria

```text id="impl-phase27-exit"
[ ] Feedback latency materially improved
[ ] No known quality coverage regression introduced
```

---

# Phase 28 — Quality Events

## Objective

Integrate Quality Framework activity with FamilyOS Event Architecture where beneficial.

---

# Initial Events

Potential events:

```text id="impl-quality-events"
quality.check.completed
quality.finding.created
quality.assessment.completed
quality.gate.failed
quality.risk.created
quality.exception.expired
```

---

# Event Checklist

```text id="impl-event-checklist"
[ ] Follow Event Architecture
[ ] Define stable event names
[ ] Define payload schema
[ ] Include target/revision
[ ] Avoid duplicating authoritative storage semantics
```

---

# Phase 28 Exit Criteria

```text id="impl-phase28-exit"
[ ] Important quality state changes can integrate with other FamilyOS capabilities
```

---

# Phase 29 — Notification Integration

## Objective

Notify responsible actors about significant actionable quality conditions.

---

# Candidate Notifications

```text id="impl-notifications"
Critical Finding
Critical Risk
Release Gate Failure
Expired High-Risk Exception
Quality Automation Unavailable
```

Checklist:

```text id="impl-notification-checklist"
[ ] Follow Notification Architecture
[ ] Alert only actionable conditions
[ ] Include owner
[ ] Deduplicate repeated events
[ ] Avoid notification fatigue
```

---

# Phase 29 Exit Criteria

```text id="impl-phase29-exit"
[ ] Significant quality failures reach accountable owners
```

---

# Phase 30 — Quality Intelligence Foundations

## Objective

Prepare structured historical data for advanced analysis.

Do not begin this phase before deterministic quality state is trustworthy.

---

# Data Quality Preconditions

```text id="impl-intelligence-preconditions"
[ ] Stable QualityFinding model
[ ] Stable QualityEvidence model
[ ] Stable Assessment model
[ ] Historical data retained
[ ] Rule identities stable
[ ] Target identities stable
[ ] Sufficient quality history exists
```

---

# Initial Analytical Capabilities

Start with deterministic analytics:

```text id="impl-analytics"
[ ] Finding trends
[ ] Debt trends
[ ] Gate failure trends
[ ] Recurring rule failures
[ ] Flaky test trends
```

---

# Phase 30 Exit Criteria

```text id="impl-phase30-exit"
[ ] Historical quality data supports reliable analysis
```

---

# Phase 31 — AI-Assisted Quality Analysis

## Objective

Introduce advisory AI capabilities only after deterministic foundations are mature.

---

# Candidate AI Capabilities

```text id="impl-ai-capabilities"
[ ] Summarize QualityAssessment
[ ] Explain blocking gate findings
[ ] Cluster related findings
[ ] Suggest likely root causes
[ ] Suggest remediation investigation
[ ] Summarize quality trends
```

---

# AI Guardrails

```text id="impl-ai-guardrails"
[ ] AI conclusions distinguish evidence from hypothesis
[ ] AI cannot change authoritative finding state automatically
[ ] AI cannot approve exceptions
[ ] AI cannot accept Critical risk
[ ] AI cannot override gates
[ ] AI cannot redefine QualityRule authority
```

---

# AI Evaluation

```text id="impl-ai-evaluation"
[ ] Test factual grounding
[ ] Test citation to underlying evidence
[ ] Measure hallucination risk
[ ] Require human validation for recommendations
```

---

# Phase 31 Exit Criteria

```text id="impl-phase31-exit"
[ ] AI improves interpretation without becoming hidden authority
```

---

# Cross-Cutting Testing Checklist

Every implementation phase should evaluate appropriate testing.

```text id="impl-testing-global"
[ ] Unit tests
[ ] Integration tests
[ ] Contract tests where applicable
[ ] Failure-path tests
[ ] Regression tests
[ ] CLI tests
[ ] Serialization tests
[ ] Static analysis
```

---

# Static Analysis Checklist

For Quality Framework implementation changes:

```text id="impl-static-checks"
[ ] Ruff PASS
[ ] MyPy PASS
```

according to current FamilyOS tooling.

---

# Full Repository Validation

Before significant Quality Framework milestones:

```text id="impl-full-validation"
[ ] Quality-specific tests PASS
[ ] Full repository Pytest PASS
[ ] Ruff PASS
[ ] MyPy PASS
[ ] Documentation validation PASS
```

---

# Test Fixture Strategy

Quality Framework adapters require controlled fixtures.

Recommended fixture classes:

```text id="impl-fixtures"
Compliant Repository
Lint Failure Repository
Type Failure Repository
Test Failure Repository
Invalid Plugin
Invalid Documentation EPIC
Architecture Violation
```

Checklist:

```text id="impl-fixture-checklist"
[ ] Keep fixtures minimal
[ ] Make expected result explicit
[ ] Avoid relying on current repository accidental state
```

---

# Error Handling Checklist

The Quality Framework should explicitly test:

```text id="impl-errors"
[ ] Tool executable missing
[ ] Tool timeout
[ ] Invalid tool output
[ ] Invalid profile
[ ] Missing evidence
[ ] Stale evidence
[ ] Unknown rule
[ ] Unknown requirement
[ ] Invalid exception
[ ] Gate evaluation error
```

---

# Serialization and Schema Checklist

If structured persistence is introduced:

```text id="impl-schema"
[ ] Define schema versioning
[ ] Validate backward compatibility requirements
[ ] Add round-trip tests
[ ] Reject unsupported versions explicitly
```

---

# Security Checklist

Because quality infrastructure may influence release decisions:

```text id="impl-security"
[ ] Apply least privilege in CI
[ ] Do not expose secrets in evidence
[ ] Treat external contribution code as untrusted
[ ] Protect gate configuration
[ ] Protect exception authority
[ ] Protect release quality evidence
```

---

# Observability Checklist

Every significant quality automation capability should expose:

```text id="impl-observability-global"
[ ] Status
[ ] Duration
[ ] Error state
[ ] Tool/version where relevant
[ ] Target
[ ] Revision
```

---

# Developer Experience Checklist

Quality tooling should remain usable.

```text id="impl-dx"
[ ] One clear CLI entry point
[ ] Failures explain what happened
[ ] Failures identify where
[ ] Failures identify governing rule
[ ] Local reproduction possible
[ ] CI semantics match local semantics
[ ] Output avoids unnecessary noise
```

---

# Documentation Checklist

For each implemented quality capability:

```text id="impl-documentation-global"
[ ] Purpose documented
[ ] Architecture documented
[ ] CLI usage documented
[ ] Failure semantics documented
[ ] Configuration documented
[ ] Ownership documented
```

---

# Governance Checklist

Before introducing blocking behavior:

```text id="impl-governance-global"
[ ] Requirement authority identified
[ ] Rule owner identified
[ ] Severity defined
[ ] Profile membership defined
[ ] Gate impact reviewed
[ ] Exception path defined if needed
```

---

# Compatibility Checklist

When changing Quality Framework semantics:

```text id="impl-compatibility"
[ ] Existing profiles reviewed
[ ] Existing evidence compatibility reviewed
[ ] Existing adapters reviewed
[ ] Existing CI integration reviewed
[ ] Migration documented if breaking
```

---

# Release Checklist for Quality Implementation

Before releasing a significant Quality Framework implementation milestone:

```text id="impl-release-checklist"
[ ] Implementation scope complete
[ ] Tests pass
[ ] Ruff passes
[ ] MyPy passes
[ ] Full repository tests pass
[ ] Documentation updated
[ ] CHANGELOG updated
[ ] VALIDATION updated
[ ] Known limitations recorded
[ ] Migration documented if needed
[ ] Release version selected
```

---

# Recommended Initial Implementation Milestone

The first practical implementation milestone should remain intentionally limited.

Recommended scope:

```text id="impl-first-milestone"
QualitySeverity
QualityStatus
QualityTarget
QualityFinding
QualityEvidence
QualityAssessment

Ruff Adapter
MyPy Adapter
Pytest Adapter

Repository Quality Profile

familyos quality check
familyos quality assess
```

This would establish a usable minimum quality platform without introducing premature governance infrastructure.

---

# First Milestone Acceptance Criteria

```text id="impl-first-milestone-acceptance"
[ ] Ruff results normalized
[ ] MyPy results normalized
[ ] Pytest results normalized
[ ] Evidence generated
[ ] Assessment generated
[ ] CLI usable locally
[ ] PASS / FAIL / ERROR differentiated
[ ] Unit tests pass
[ ] Integration tests pass
[ ] Full repository validation passes
```

---

# Recommended Second Milestone

After the first milestone is stable:

```text id="impl-second-milestone"
Documentation Validation
Plugin Compliance Integration
Quality Profiles
CI Integration
Non-Blocking Merge Gate
```

---

# Recommended Third Milestone

After CI quality execution is reliable:

```text id="impl-third-milestone"
Blocking Merge Gate
Quality Risk
Quality Debt
Compliance
Exceptions
Historical Reporting
```

---

# Recommended Fourth Milestone

After quality state becomes stable and historical:

```text id="impl-fourth-milestone"
Release Gate
Governance Registry
Quality Metrics
Continuous Improvement
Lifecycle Automation
```

---

# Advanced Milestone

Only after the previous capabilities are mature:

```text id="impl-advanced-milestone"
Quality Events
Notifications
Cross-Repository Quality Platform
Advanced Observability
Quality Intelligence
AI-Assisted Analysis
```

---

# Dependencies

The implementation depends on stable integration with:

```text id="impl-dependencies"
EPIC-ENG-001
Engineering Foundation

EPIC-TST-001
Testing Framework

EPIC-DOC-001
Documentation Framework

EPIC-BLD-001
Build Framework

EPIC-REL-001
Release Framework

EPIC-PLUGIN-002
Plugin Compliance Framework

FamilyOS Architecture Foundation
```

---

# Implementation Dependency Principle

The Quality Framework should consume existing domain capabilities instead of becoming their replacement.

Conceptually:

```text id="impl-dependency-principle"
Testing Framework
      ↓
Test Evidence

Documentation Framework
      ↓
Documentation Evidence

Plugin Compliance Framework
      ↓
Compliance Evidence

Quality Framework
      ↓
Unified Assessment and Governance
```

---

# Out-of-Scope for Initial Implementation

The following should not be considered required for the first executable Quality Framework release:

```text id="impl-out-of-scope"
Central Quality Database
Complex Web Dashboard
Distributed Quality Service
Predictive AI
Machine Learning Risk Model
Dynamic Adaptive Gates
Cross-Repository Quality Graph
Real-Time Notification Platform
```

These capabilities may become justified later.

---

# Implementation Anti-Patterns

The FamilyOS Quality Framework implementation should avoid the following anti-patterns.

## Reimplement Existing Tools

Do not recreate linting, type checking, or testing engines.

## Tool-Centric Domain Model

Do not design the quality domain around Ruff, MyPy, or Pytest internals.

## Database First

Do not introduce centralized persistence before lifecycle requirements justify it.

## Gate First

Do not create blocking gates before check reliability is demonstrated.

## Metrics First

Do not build dashboards before trustworthy evidence exists.

## AI First

Do not build quality intelligence before deterministic history exists.

## Duplicate Compliance

Do not reimplement Plugin Compliance rules inside the Quality Framework.

## CLI Logic Duplication

CLI and CI should share application-layer quality logic.

## Silent Errors

Tool or infrastructure errors must never silently become PASS.

## Unversioned Policy

Rules and profiles that affect authoritative decisions should be version-controlled.

---

# Completion Definition

The complete implementation of EPIC-QLT-001 should eventually mean that FamilyOS can:

```text id="impl-completion-definition"
Define Quality Requirements

Resolve Applicable Quality Profiles

Execute Deterministic Quality Rules

Collect Structured Quality Evidence

Produce Structured Quality Findings

Generate Reproducible Quality Assessments

Evaluate Compliance

Manage Quality Risk

Manage Defects and Quality Debt

Evaluate Quality Gates

Integrate Quality Into CI

Observe Quality Trends

Govern Exceptions and Overrides

Continuously Improve Quality Controls
```

---

# Minimum Viable Quality Framework

The minimum viable executable Quality Framework is considerably smaller.

It requires only:

```text id="impl-mvqf"
Quality Domain Models
      ↓
Tool Adapters
      ↓
Evidence
      ↓
Assessment
      ↓
CLI
      ↓
CI
```

This is the recommended starting point.

---

# Mature Quality Framework

A mature implementation adds:

```text id="impl-mature"
Profiles
Architecture Rules
Compliance
Risk
Debt
Gates
Observability
Governance
Continuous Improvement
```

---

# Advanced Quality Platform

An advanced implementation may eventually provide:

```text id="impl-advanced-platform"
Cross-Framework Quality Graph
Historical Quality Intelligence
Automated Regression Detection
Predictive Risk Analysis
AI-Assisted Quality Investigation
```

These capabilities remain future evolution, not initial requirements.

---

# Implementation Progress Review

Implementation progress should be reviewed based on capability, not code volume.

Useful questions include:

```text id="impl-progress-review"
Can FamilyOS produce structured quality evidence?

Can a developer reproduce a failed quality check?

Can an assessment explain why it failed?

Can CI consume the same quality logic?

Can quality progression decisions be traced?

Can known quality debt remain visible?

Can the system learn from repeated defects?
```

---

# Implementation Success Criteria

The implementation is successful when quality becomes easier to understand and harder to bypass accidentally.

A successful system should provide:

```text id="impl-success"
Fast Feedback
Reliable Verification
Structured Evidence
Clear Findings
Explainable Assessments
Consistent Local and CI Behavior
Traceable Gates
Visible Risk
Visible Debt
Governed Exceptions
```

---

# Reference Implementation Sequence

The complete implementation sequence can be represented as:

```text id="impl-reference-sequence"
Normative Quality Framework
      ↓
Quality Package Architecture
      ↓
Core Domain Models
      ↓
Quality Evidence
      ↓
Executor Contracts
      ↓
Ruff Integration
      ↓
MyPy Integration
      ↓
Pytest Integration
      ↓
Documentation Validation
      ↓
Plugin Compliance Integration
      ↓
Quality Assessment
      ↓
Quality Profiles
      ↓
Quality CLI
      ↓
CI Integration
      ↓
Architecture Rules
      ↓
Non-Blocking Gates
      ↓
Blocking Merge Gate
      ↓
Quality Risk
      ↓
Defect and Quality Debt
      ↓
Compliance
      ↓
Exceptions
      ↓
Release Gate
      ↓
Historical Quality State
      ↓
Quality Metrics
      ↓
Continuous Improvement
      ↓
Governance Registry
      ↓
Framework Lifecycle Automation
      ↓
Performance Optimization
      ↓
Quality Events
      ↓
Notifications
      ↓
Quality Intelligence
      ↓
AI-Assisted Quality Analysis
```

---

# Strategic Outcome

The Implementation Checklist enables FamilyOS to move from:

```text id="impl-strategic-before"
The Quality Framework architecture is documented,
but implementation can begin in many possible
directions.
```

toward:

```text id="impl-strategic-after"
The Quality Framework has a clear implementation path.

Foundational domain concepts are introduced first.

Existing tools are integrated rather than replaced.

Evidence precedes authoritative assessments.

Assessments precede blocking gates.

Observability follows trustworthy quality state.

Governance grows with actual engineering need.

Advanced intelligence is introduced only after
deterministic foundations are mature.
```

This reduces implementation risk and protects architectural coherence.

---

# Final Implementation Principle

The Quality Framework should not be implemented as one large platform project.

It should emerge through a sequence of small, validated engineering capabilities whose value is demonstrated before additional complexity is introduced.

The implementation progression is therefore:

```text id="impl-final-flow"
Model
   ↓
Verify
   ↓
Evidence
   ↓
Assess
   ↓
Automate
   ↓
Integrate
   ↓
Enforce
   ↓
Observe
   ↓
Govern
   ↓
Improve
```

Through this sequence, EPIC-QLT-001 can evolve from a normative engineering framework into a practical, reliable, explainable, and continuously improving FamilyOS quality platform without sacrificing simplicity, maintainability, or architectural integrity.

---

## Phase 2 Runtime Contract Reconciliation

The following decisions are prerequisites for implementation of the initial
Core Quality Domain Models:

- [x] Canonical Quality package architecture established.
- [x] Core Quality domain remains independent from Ruff, MyPy, Pytest, and CI
      providers.
- [x] `QualitySeverity` vocabulary reconciled as `INFO`, `LOW`, `MEDIUM`,
      `HIGH`, `CRITICAL`.
- [x] `QualityStatus` vocabulary reconciled as `PASS`, `WARNING`, `FAIL`,
      `ERROR`, `SKIPPED`, `UNKNOWN`.
- [x] `WARNING` selected as the canonical runtime status spelling.
- [x] Existing semantically distinct `WARN` modes/phases are not globally
      renamed.
- [x] `ERROR` remains distinct from `FAIL`.
- [x] `UNKNOWN` cannot silently become `PASS`.
- [x] `SKIPPED` remains distinct from `UNKNOWN`.
- [x] Runtime Quality identifiers remain compatible with the FamilyOS
      identifier specification and existing `QLT-*` namespaces.
- [x] Phase 2 does not authorize Quality Evidence implementation.
- [x] Phase 2 does not authorize tool adapters, Quality CLI, CI integration, or
      Quality gates.

This reconciliation authorizes implementation of the Core Quality Domain
Models only after the resulting documentation diff is reviewed and accepted.

## Phase 2 Core Model Shape Reconciliation

The Phase 2 implementation contract was reconciled before runtime model
implementation.

Contract decisions:

- [x] Quality runtime identifier categories preserve `SPEC-0002` stable-boundary
      validation without inventing a narrower suffix taxonomy.
- [x] `QualityTarget` initial runtime fields and reproducibility boundary are
      defined.
- [x] `QualityFinding` required fields and the Phase 2 opaque Evidence-reference
      boundary are defined without implementing `QualityEvidence`.
- [x] `QualityRequirement` authority, mandatory, applicability, and verification
      representation is defined for the initial runtime.
- [x] `QualityRule` requirement linkage and opaque executor-reference boundary
      are defined without implementing the Phase 4 Quality Executor port.
- [x] Phase 2 models remain tool-independent and do not authorize adapters,
      Quality CLI, CI integration, Quality gates, profiles, or assessment
      execution.

These reconciliation records do not close the original Phase 2 implementation
checklist. `Define QualitySeverity`, `Define QualityStatus`, `Define initial
domains`, `Define QualityTarget`, `Define QualityFinding`,
`Define QualityRequirement`, `Define QualityRule`, validation/testing items,
and the Phase 2 exit criteria remain open until their corresponding runtime
implementation and verification evidence exist.

Phase 3 `QualityEvidence` implementation remains explicitly open.
