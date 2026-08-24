# Build Framework

# 13 Build Execution

## Overview

EPIC-BLD-001 — Build Framework defines how FamilyOS build execution transforms a resolved and validated build context into candidate artifacts.

Build execution is the operational core of the Build Framework.

It is the stage where controlled inputs, dependencies, configuration, toolchain, and environment are actively transformed into technical outputs.

However, execution is not equivalent to trust.

A successful execution produces candidate outputs.

Those outputs only become trusted artifacts after validation and evidence requirements are satisfied.

The central principle is:

> Build execution performs transformation; validation establishes trust.

---

# Purpose

The purpose of the Build Execution model is to define how FamilyOS build operations are initiated, orchestrated, executed, observed, failed, retried, finalized, and integrated with artifact processing.

It establishes requirements for:

* execution entry points;
* execution stages;
* orchestration;
* build targets;
* build profiles;
* preconditions;
* state transitions;
* working directories;
* temporary state;
* generation;
* packaging;
* failure handling;
* cancellation;
* retries;
* observability;
* concurrency;
* reproducibility;
* security;
* automation;
* result reporting.

---

# Execution Boundary

Build execution begins only after required build context has been resolved and validated.

The canonical boundary is:

```text
Resolved Build Context
        ↓
Pre-Execution Validation
        ↓
BUILD EXECUTION
        ↓
Candidate Outputs
        ↓
Artifact Processing
        ↓
Artifact Validation
```

Execution must not silently resolve foundational uncertainty that should have been handled earlier.

---

# Execution Preconditions

Before significant build execution begins, applicable preconditions SHOULD be satisfied.

These may include:

* build target exists;
* build profile is valid;
* required source inputs exist;
* configuration has resolved;
* dependencies are available;
* toolchain is supported;
* environment is valid;
* output locations are writable;
* required policy checks have passed.

Invalid preconditions should fail early.

---

# Execution Request

A build execution begins from an explicit request.

A conceptual request may contain:

```text
BuildExecutionRequest
│
├── Build ID
├── Target
├── Profile
├── Resolved Context
├── Effective Configuration
├── Output Expectations
└── Execution Options
```

The exact implementation may initially remain simpler.

The architectural responsibility should remain explicit.

---

# Build Target

A build target identifies what is being transformed.

Examples may include:

* FamilyOS CLI package;
* official plugin;
* documentation bundle;
* generated reference material;
* validation artifact;
* future platform component.

A target must have defined:

* input scope;
* execution behavior;
* expected outputs;
* applicable validation.

---

# Target Principle

A build target should not be inferred accidentally from the current working directory or arbitrary filesystem state.

The preferred model is:

```text
Explicit Target
      ↓
Resolved Inputs
      ↓
Build Execution
```

---

# Build Profile

The build profile defines the purpose and strictness of execution.

Possible profiles include:

```text
development
validation
ci
documentation
plugin
release-candidate
```

Profiles may influence:

* execution stages;
* optimization;
* validation;
* evidence;
* output behavior.

They must not redefine foundational build semantics.

---

# Execution Entry Point

FamilyOS SHOULD expose canonical build entry points.

These may eventually include:

* CLI commands;
* Python module entry points;
* task runner targets;
* CI adapters.

The entry point should delegate to the canonical build architecture rather than reproduce build logic independently.

---

# Canonical Execution Principle

The preferred relationship is:

```text
User / CI
    ↓
Canonical Build Entry Point
    ↓
Build Orchestration
    ↓
Execution Stages
```

The framework rejects multiple incompatible execution paths for the same build target.

---

# Build Orchestration

Build orchestration coordinates execution stages.

Its responsibility includes:

* stage sequencing;
* context propagation;
* error propagation;
* stage activation;
* artifact collection;
* result assembly.

Orchestration should remain understandable.

---

# Orchestration Model

A canonical orchestration sequence may be:

```text
Initialize
   ↓
Prepare Workspace
   ↓
Generate Required Inputs
   ↓
Execute Transformation
   ↓
Package
   ↓
Collect Outputs
   ↓
Finalize Execution
```

Artifact validation occurs after execution output has been identified.

---

# Current Execution Contract

The current canonical FamilyOS package-build implementation uses one explicit
application-owned orchestration path for the `familyos-cli-package` target.

The implemented execution contract is intentionally simpler than the complete
conceptual execution model described by this document.

At the current implementation level, the canonical flow is:

```text
Build Request
    ↓
Resolve Target And Profile Policy
    ↓
Validate Build Inputs
    ↓
Validate Repository Layout
    ↓
Resolve And Validate Toolchain
    ↓
Capture And Validate Environment
    ↓
Resolve Immutable Build Context
    ↓
Validate Effective Configuration
    ↓
Execute Python Packaging
    ↓
Discover Candidate Package Outputs
    ↓
Validate Package Structure
    ↓
Establish Artifact Identity
    ↓
Establish Artifact Integrity
    ↓
Build Artifact Manifest
    ↓
Optional Wheel Functional Validation
    ↓
Canonical Package-Build Result
```

This orchestration sequence is now represented by canonical immutable
execution-stage observations owned by the application layer.

Each stage observation records the canonical stage identifier, terminal status,
elapsed monotonic duration, and an optional diagnostic.

Mandatory validation or execution failure prevents later dependent operations
from being reported as a successful build.

Packaging failure, discovery failure, structural-validation failure, and
requested functional-validation failure therefore propagate through the
canonical result.

The packaging execution boundary itself remains deliberately narrow.

The package-builder port receives the canonical project root and resolved
output directory and returns process-level status, direct outputs, an optional
exit code, and an optional diagnostic.

These process-level outputs do not establish artifact identity, integrity,
validation, evidence, or trust by themselves.

The current canonical package contract expects exactly one Python wheel and one
source distribution in the resolved output directory.

Artifact Discovery owns that classification after packaging execution.

The current implementation exposes ordered canonical execution-stage records
through the package-build result.

The implemented stage vocabulary is:

```text
VALIDATE_INPUTS
VALIDATE_REPOSITORY_LAYOUT
VALIDATE_TOOLCHAIN
VALIDATE_ENVIRONMENT
INITIALIZE_WORKSPACE
RESOLVE_BUILD_CONTEXT
VALIDATE_EFFECTIVE_CONFIGURATION
STAGE_BUILD_INPUTS
PACKAGE
DISCOVER_ARTIFACTS
VALIDATE_ARTIFACTS
ESTABLISH_ARTIFACT_IDENTITY
ESTABLISH_ARTIFACT_INTEGRITY
BUILD_ARTIFACT_MANIFEST
FUNCTIONALLY_VALIDATE_WHEEL
FINALIZE_EXECUTION
```

`FUNCTIONALLY_VALIDATE_WHEEL` is present only when functional validation is
requested and reached.

Execution observations preserve orchestration order. A mandatory failure
records the failing stage and prevents later dependent stages from being
reported as executed.

The current implementation does not define stage start or end timestamps,
per-stage tool invocation records, retry history, cancellation state, or a
general-purpose structured execution trace beyond this ordered terminal-stage
history.

---

# Current Canonical CLI Contract

The implemented package-build entry point is:

```text
familyos build
```

Its current explicit execution controls include:

```text
--output-dir
--functional-validation
--profile
--evidence-output
```

The currently supported build profiles are:

```text
development
validation
ci
release-candidate
```

The currently supported canonical target is:

```text
familyos-cli-package
```

Target selection is represented explicitly in the application Build Context,
although the current CLI package-build command does not expose a separate
`--target` option.

The CLI delegates to the canonical application-owned package-build use case.

CI therefore reuses canonical build semantics rather than defining an
independent packaging implementation.

The CLI currently reports process-level and effective-context information,
including Build ID, profile, target, runtime and environment observations,
critical toolchain versions, output configuration, evidence configuration,
candidate outputs, validation outcomes, and failure diagnostics where
available.

It also renders the ordered execution-stage observations already established by
the application result.

For each reached stage, the CLI exposes the canonical stage identifier,
terminal status, elapsed duration, and diagnostic when one exists.

The CLI remains a presentation surface for application-owned observations. It
does not independently establish execution-stage state or Build Evidence
semantics.

---

# Stage Model

Execution SHOULD be divided into logical stages where doing so improves clarity.

A conceptual model is:

```text
PREPARE
GENERATE
ASSEMBLE
PACKAGE
COLLECT
FINALIZE
```

Not every build type requires all stages.

---

# Stage Responsibility

Each stage SHOULD have:

* clear purpose;
* defined inputs;
* expected outputs;
* explicit failure behavior.

This improves diagnosis and future automation.

---

# Stage Independence

Stages should avoid unnecessary hidden coupling.

For example:

```text
PACKAGE
```

should not depend on an undocumented file created manually before the build.

Dependencies between stages should be explicit.

---

# Stage Ordering

Stage order must be deterministic.

The framework rejects stage sequencing that depends on:

* unordered filesystem traversal;
* incidental script invocation order;
* race conditions;
* CI job timing.

---

# Execution Context

Every stage executes within the resolved Build Context.

Conceptually:

```text
Build Context
│
├── Source
├── Configuration
├── Dependencies
├── Toolchain
├── Environment
├── Profile
└── Policies
        ↓
Execution Stage
```

Stages should not independently re-resolve critical context unless explicitly required.

---

# Context Stability

The effective build context SHOULD remain stable throughout execution.

The preferred model is:

```text
Resolve
  ↓
Validate
  ↓
Freeze Logical Context
  ↓
Execute
```

Mid-build mutation weakens traceability.

---

# Build Workspace

Execution occurs inside a workspace.

The canonical package-build implementation now initializes an isolated
build-owned workspace before Build Context resolution.

The workspace root is derived from the validated environment temporary
directory and the canonical Build ID:

```text
<temporary-directory>/
└── familyos-build/
    └── <build-id>/
        ├── staging/
        └── intermediate/
```

The workspace is represented by the immutable application-owned
`BuildWorkspace` model.

Workspace initialization is owned by `BuildWorkspaceInitializer`.

The initializer receives the canonical Build ID and validated environment
temporary directory, derives the workspace paths, and creates the required
directories.

The workspace is therefore:

* outside authoritative project source;
* namespaced by Build ID;
* isolated from unrelated build executions;
* writable and disposable;
* initialized before Build Context resolution and packaging.

The `staging` and `intermediate` directories establish canonical workspace
structure only.

Level 13.4 does not yet define staging operations, generation behavior,
execution finalization, partial-output handling, cleanup, cancellation, or
retry semantics.

Workspace initialization is represented explicitly by the canonical
`INITIALIZE_WORKSPACE` execution stage.

Initialization failure is fail-fast. If workspace creation raises an operating
system error, the stage is recorded as `FAILED`, its diagnostic is retained,
and Build Context resolution and all later dependent stages are not executed.

The workspace must not become an unofficial source of truth.

---

# Workspace Requirements

A build workspace SHOULD be:

* predictable;
* writable where required;
* disposable;
* isolated from unrelated state;
* safe to clean.

The workspace must not become an unofficial source of truth.

---

# Clean Workspace

High-trust builds SHOULD support execution from a clean workspace.

This helps detect dependence on:

* stale intermediates;
* cached generated files;
* previous build output;
* manual preparation.

---

# Workspace Preparation

The canonical package-build implementation now stages authoritative build
inputs after successful effective-configuration validation and before package
execution.

`BuildInputStager` materializes the authoritative package-build input set
beneath the Build-ID-scoped workspace:

```text
<workspace-root>/
├── staging/
│   └── project/
└── intermediate/
```

The staged project is represented by the immutable `StagedBuildInputs` model.

The current canonical staging set materializes the package project inputs
required by the FamilyOS CLI build contract, including root packaging files
and the `src/familyos_cli` package tree, while excluding unrelated repository
state and Python cache state.

Staging is explicit and fail-fast. It is represented by the canonical
`STAGE_BUILD_INPUTS` execution stage.

If staging fails, the stage is recorded as `FAILED`, its diagnostic is
retained, and package execution and all later dependent stages are not
executed.

The current staging contract establishes an isolated materialized snapshot
for subsequent build work. It does not yet make that staged snapshot the
source consumed by the canonical Python package builder.

The Python package builder therefore continues to consume authoritative
`project_root` directly and continues to write candidate distributions to
the canonical output directory.

This distinction is intentional. Level 13.5 defines staging behavior without
claiming implementation of package assembly from staged inputs.

Preparation must not silently alter authoritative source.

---

# Temporary State

Temporary files are expected during execution.

They must remain:

* isolated;
* disposable;
* non-authoritative;
* excluded from trusted artifact identity unless deliberately included.

---

# Intermediate Outputs

Intermediate outputs support later execution stages.

Examples may include:

* generated source;
* package staging trees;
* temporary metadata;
* transformed resources.

Intermediate outputs are not trusted artifacts.

---

# Intermediate Output Principle

The relationship is:

```text
Intermediate Output
        ↓
Further Transformation
        ↓
Candidate Artifact
```

Intermediate state should not be passed directly to the Release Framework.

---

# Generation Stage

Some builds may generate content before packaging.

Examples include:

* manifests;
* schemas;
* documentation;
* metadata;
* generated code.

Generation must follow the rules defined in the Build Input and Project Structure model.

---

# Generation Requirements

Generation SHOULD be:

* deterministic where practical;
* repeatable;
* based on explicit inputs;
* attributable to a known generator;
* validated where necessary.

For the current canonical FamilyOS CLI package build, no dedicated generation
stage is required before package assembly.

The authoritative package inputs required by that build are already
materialized before canonical execution. The generated dependency lock
`requirements.txt` is treated as a controlled build input and its freshness
against the canonical dependency declarations in `pyproject.toml` is validated
by the build-input validation boundary.

The existing FamilyOS generation subsystem is not part of the current
canonical package-build execution path. Project, domain, documentation, schema,
metadata, or other future build targets may require explicit generation stages,
but such stages must be introduced only when the corresponding target actually
depends on generated content.

The absence of a generation stage for the current package target is therefore
an explicit execution decision rather than an implicit omission.

A future target that requires generation MUST define:

* the authoritative source inputs;
* the responsible generator;
* the generated destination;
* ordering relative to staging and transformation;
* freshness or regeneration semantics;
* validation requirements;
* failure propagation behavior.

---

# Source Mutation

Build execution SHOULD avoid modifying tracked authoritative source.

If generation intentionally updates committed derived files, this must be a documented workflow rather than an accidental build side effect.

---

# Build Transformation

The transformation stage performs the core build work.

For Python packaging this may include invoking a standards-compatible builder or backend.

Future FamilyOS technologies may use different transformation mechanisms.

The framework defines behavior, not one universal tool.

---

# Transformation Requirements

The transformation must:

* consume the resolved context;
* use declared tooling;
* produce outputs in known locations;
* expose failure clearly;
* avoid unauthorized side effects.

---

# Package Assembly

Package assembly determines which source and resource content enters the resulting artifact.

For the current canonical FamilyOS CLI package target, package assembly now consumes the isolated project snapshot produced by `BuildInputStager`.

After successful `STAGE_BUILD_INPUTS`, the `PACKAGE` stage passes `StagedBuildInputs.project_root` to the canonical `PythonPackageBuilder` instead of passing authoritative `project_root` directly.

The effective package source is therefore:

```text
Authoritative Project
        ↓
BuildInputStager
        ↓
<workspace-root>/staging/project
        ↓
PythonPackageBuilder
```

The canonical output directory remains independent from the staged project root. Candidate wheel and source-distribution artifacts continue to be written to the resolved canonical build output directory.

Real PyPA validation confirms that the staged project contains the complete input set required by the current package target and can produce exactly one wheel and one source distribution through the standard Python build frontend.

Package assembly therefore no longer consumes authoritative project source directly.

The current contract remains intentionally target-specific. Future build targets must define their own authoritative assembly inputs and staging requirements.

Assembly must prevent accidental inclusion of:

* secrets;
* caches;
* development-only files;
* unrelated repository content;
* temporary state.

---

# Inclusion Rules

Artifact inclusion should derive from explicit package or build configuration.

The framework rejects packaging-by-accident.

---

# Exclusion Rules

Files that must not enter artifacts include, where applicable:

* local secrets;
* virtual environments;
* caches;
* temporary files;
* test artifacts not intended for distribution;
* local configuration.

---

# Packaging Stage

Packaging converts prepared build state into defined artifact formats.

For current Python-based FamilyOS components, this may include:

* wheels;
* source distributions.

Future components may introduce other artifact formats.

---

# Packaging Requirements

Packaging must produce:

* known artifact types;
* predictable output names;
* defined metadata;
* structurally valid candidate artifacts.

Packaging success alone does not establish artifact trust.

---

# Multi-Artifact Execution

A build may produce several related outputs.

For example:

```text
Build
│
├── Wheel
├── Source Distribution
├── Manifest
├── Documentation
└── Validation Metadata
```

Execution should associate these outputs with the same build identity.

---

# Artifact Collection

After transformation, candidate outputs must be collected.

Collection identifies:

* which outputs were produced;
* which outputs match expected artifact classes;
* which outputs are intermediate;
* which outputs are unexpected.

---

# Artifact Collection Principle

The build should not discover official candidate artifacts by guessing.

The preferred model is:

```text
Defined Output Contract
        ↓
Collect Expected Outputs
```

---

# Unexpected Output

Unexpected files may indicate:

* configuration drift;
* packaging error;
* stale workspace;
* toolchain change.

Significant unexpected output should be investigated.

---

# Missing Output

If a required artifact is absent, execution cannot be considered complete.

The build must fail or enter an invalid final state.

---

# Build Execution State Machine

A conceptual execution state model is:

```text
REQUESTED
   ↓
INITIALIZING
   ↓
PREPARING
   ↓
RUNNING
   ↓
COLLECTING
   ↓
FINALIZING
   ↓
SUCCEEDED
```

Failures may transition to:

```text
FAILED
```

Cancellation may transition to:

```text
CANCELLED
```

---

# State Transition Principle

State transitions should be explicit enough to support:

* observability;
* diagnostics;
* automation;
* evidence.

The implementation need not initially expose a formal state machine API.

---

# Successful Execution

Successful execution means:

* all required execution stages completed;
* required candidate outputs were produced;
* no fatal execution failure occurred.

It does not yet mean:

```text
Trusted Artifact
```

Artifact validation remains required.

---

# Failed Execution

Execution failure occurs when a required stage cannot complete correctly.

Possible causes include:

* tool execution error;
* missing generated input;
* package assembly failure;
* filesystem error;
* invalid staging output;
* unexpected command exit.

---

# Failure Propagation

Failures must propagate to the overall build result.

The framework rejects patterns where errors are logged but ignored and execution continues as though successful.

---

# Failure Context

A useful execution failure should identify:

* build ID;
* target;
* profile;
* failing stage;
* operation;
* diagnostic message;
* relevant tool;
* relevant paths where safe.

---

# Failure Categories

Possible conceptual categories include:

```text
PREPARATION_FAILURE
GENERATION_FAILURE
TRANSFORMATION_FAILURE
PACKAGING_FAILURE
OUTPUT_COLLECTION_FAILURE
FILESYSTEM_FAILURE
TOOL_EXECUTION_FAILURE
```

Formal machine-readable codes may be introduced later.

---

# Exit Codes

Canonical command-line build interfaces SHOULD use meaningful process exit behavior.

At minimum:

```text
0 → requested execution succeeded
non-zero → execution or required validation failed
```

More detailed exit-code models may be introduced if useful.

---

# Partial Outputs

A failed or errored package-build invocation may create or modify files before
the package frontend terminates unsuccessfully.

Canonical package execution now observes these filesystem consequences.

`PythonPackageBuilder` snapshots direct files in the canonical output directory
before package execution and compares that state with the filesystem state
after execution.

This comparison is performed for all package-execution outcomes:

* `SUCCEEDED`;
* `FAILED`;
* `ERROR`.

Files created or changed by the invocation are returned through
`PackageBuildResult.outputs`.

For failed or errored package execution, these outputs are partial process-level
outputs only.

They are not automatically promoted to canonical artifact candidates.

The failure path is:

    Package Execution
            ↓
    FAILED / ERROR
            ↓
    Observe Created Or Changed Outputs
            ↓
    PackageBuildResult.outputs
            ↓
    CanonicalPackageBuildResult.execution.outputs
            ↓
    FINALIZE_EXECUTION

Artifact Discovery is not executed after failed or errored package execution.

Therefore:

    Partial Process Output
            ≠
    Discovered Candidate Artifact

`CanonicalPackageBuildResult.candidates` remains empty when package execution
fails before Artifact Discovery.

Unchanged pre-existing files in the output directory are excluded from the
partial-output set.

Partial-output handling does not assign artifact identity, integrity, manifest,
validation, trust, or release semantics.

It also does not delete partial outputs.

Retention or removal after failure belongs to the separate failure-cleanup
policy.

---

# Cleanup After Failure

Canonical package-build execution now applies explicit failure cleanup to the
Build-ID-scoped internal workspace.

Once `INITIALIZE_WORKSPACE` has completed successfully, every terminal
non-successful build result is finalized with the current `BuildWorkspace`.

Before `FINALIZE_EXECUTION`, the centralized finalization boundary removes the
workspace through `BuildWorkspaceCleaner`.

The failure-cleanup flow is:

    Last Failed Or Errored Business Stage
            ↓
    Preserve Build Result And Diagnostics
            ↓
    Preserve Process-Level Partial Outputs
            ↓
    Remove BuildWorkspace.root
            ↓
    FINALIZE_EXECUTION
            ↓
    CanonicalPackageBuildResult

`BuildWorkspaceCleaner` removes the complete canonical workspace:

    <temporary-root>/familyos-build/<build-id>/

including:

* `staging/`;
* `intermediate/`;
* staged project inputs;
* other non-authoritative internal workspace state.

Cleanup is applied only when:

* a canonical workspace was successfully created; and
* the terminal canonical build result is not successful.

Failures that occur before workspace initialization do not invoke workspace
cleanup because no canonical workspace exists yet.

Successful builds do not trigger failure cleanup.

Failure cleanup deliberately does not remove the canonical package output
directory.

Therefore `PackageBuildResult.outputs` produced before failed or errored
package termination remain available as process-level partial outputs under the
Level 13.9 contract.

The cleanup boundary therefore preserves the distinction:

    Internal Build Workspace
            → removable after failure

    Package Output Directory
            → preserved for partial-output diagnostics

Cleanup does not overwrite the original failure status or diagnostic.

The failed business stage remains observable immediately before terminal
finalization.

Cleanup is idempotent with respect to an already absent workspace.

This policy does not introduce artifact trust, release, publication,
cancellation, retry, or distributed tracing semantics.

---

# Cancellation

Execution may be cancelled because of:

* user request;
* CI supersession;
* infrastructure shutdown;
* upstream workflow cancellation.

Cancellation must produce a non-successful final state.

The current canonical package-build implementation is synchronous and does not
yet expose a runtime cancellation boundary.

In particular, the current implementation does not provide:

* a cancellation token or cancellation request API;
* managed asynchronous package execution;
* explicit `SIGINT` or `SIGTERM` handling;
* child-process termination orchestration;
* a runtime `CANCELLED` package-build status.

`CANCELLED` therefore remains a reserved lifecycle state rather than a
currently emitted `PackageBuildStatus`.

Introducing a runtime cancellation state before an execution boundary can
actually observe and control cancellation would create a state that the
canonical build cannot reliably produce.

Cancellation semantics are consequently defined for the current slice as:

```text
Cancellation requested outside canonical runtime
                    |
                    v
       Host/runtime interruption semantics

Canonical runtime cancellation boundary absent
                    |
                    v
       No synthetic CANCELLED build result
```

A future cancellation implementation must introduce an explicit execution
boundary capable of observing cancellation, controlling the active child
process, preserving diagnostics, and producing a deterministic terminal
result.

---

# Cancellation Safety

Cancellation must not leave an incomplete build appearing successful or
trusted.

When runtime cancellation support is introduced, it must preserve the same
safety principles already applied to canonical failure handling:

* incomplete execution must remain non-successful;
* candidate outputs must not gain trust because cancellation occurred;
* workspace cleanup must be deterministic once the active workspace is known;
* process-level partial outputs must remain observable according to the
  canonical partial-output policy;
* cancellation must not be silently normalized into success.

The current synchronous implementation deliberately does not synthesize a
`CANCELLED` result when no canonical cancellation boundary exists.

---
# Retry Philosophy

Retries must be used cautiously.

Automatically retrying a deterministic source, configuration, validation, or
packaging failure wastes time and can hide defects.

Retries are appropriate only for failures that an execution boundary can
reliably classify as transient.

The current canonical package-build runtime does not provide such a
classification boundary.

It therefore performs no automatic retries.

---

# Canonical Retry Policy

The current canonical retry policy is:

```text
Build attempt
     |
     v
Terminal result
     |
     +-- explicitly classified transient failure
     |        |
     |        v
     |   Future retry policy may apply
     |
     +-- deterministic failure
     |        |
     |        v
     |   No retry
     |
     +-- unknown or unclassified failure
              |
              v
          No retry
```

A failure must not become retryable merely because it produces
`PackageBuildStatus.ERROR`.

Likewise, a non-zero packaging subprocess exit must not be retried merely
because it produces `PackageBuildStatus.FAILED`.

Status and retry classification are separate concerns.

The current implementation has no canonical failure-classification model that
can distinguish transient infrastructure failure from deterministic failure
with sufficient reliability.

Unknown or unclassified failures are therefore non-retryable by default.

---

# Retry Classification

Potentially retryable failures may include, once explicitly and reliably
classified:

* temporary network interruption;
* transient registry unavailability;
* temporary CI infrastructure failure;
* temporary remote-service unavailability.

Non-retryable failures include deterministic failures such as:

* invalid configuration;
* failed tests;
* missing authoritative source;
* incompatible dependencies;
* deterministic packaging errors;
* artifact-validation failures;
* functional-validation failures.

These examples do not themselves create runtime retry behavior.

A future retry implementation must introduce an explicit classification
boundary before automatic retry is permitted.

---

# Retry Safety

A future retry mechanism must:

* retry only failures explicitly classified as transient;
* use a finite and deterministic attempt limit;
* avoid retrying deterministic failures;
* preserve diagnostics from failed attempts;
* preserve partial-output semantics;
* apply workspace cleanup consistently between attempts where required;
* avoid granting artifact trust because a later attempt succeeds;
* make retry activity observable;
* preserve the canonical final result semantics.

Retry must never silently convert an unexplained failure into apparent
reliability.

---

# Retry Transparency

Retries must be visible in diagnostics and execution evidence.

The final result must not hide the fact that earlier attempts failed.

If retry support is introduced, attempt count, classification reason, and
terminal outcome must remain observable.

The current canonical package-build runtime performs exactly one packaging
attempt and therefore emits no retry metadata.

---
# Idempotence

Where practical, repeated execution of the same build request should not create uncontrolled cumulative effects.

The preferred model is:

```text
Run Build
   ↓
Result

Run Again
   ↓
Equivalent Result
```

subject to controlled non-deterministic metadata.

---

# Build Side Effects

Build execution should minimize side effects outside defined workspace and output boundaries.

Potential side effects requiring control include:

* source modification;
* environment modification;
* external publication;
* network writes;
* global tool installation.

---

# Publication Is Not Build Execution

Publishing artifacts to an official registry is not ordinary Build Execution responsibility.

The boundary is:

```text
Build
  ↓
Validated Artifact
  ↓
Release
  ↓
Publication
```

This prevents release credentials from becoming ordinary build requirements.

---

# Concurrency

FamilyOS may eventually execute independent build operations concurrently.

Concurrency must preserve correctness.

Potential issues include:

* shared output directories;
* shared temporary files;
* mutable caches;
* shared generated state;
* race conditions.

---

# Concurrent Build Principle

Independent builds should use isolated build identities and workspaces where concurrency could otherwise create interference.

---

# Parallel Stage Execution

Some stages may eventually run in parallel when dependencies permit.

Parallelization must not change build semantics.

The rule is:

```text
Sequential Semantics
        =
Parallel Semantics
```

---

# Execution Ordering

When one stage depends on another, the dependency must be explicit.

Parallel execution must not rely on timing assumptions.

---

# Incremental Execution

Incremental execution may reuse previous results to reduce build time.

Incremental behavior is an optimization.

It must not alter correctness.

---

# Incremental Build Principle

The target is:

```text
Clean Build Result
       =
Incremental Build Result
```

for equivalent build context.

---

# Incremental Validity

An incremental step may only be skipped when the build system can establish that relevant inputs have not changed.

Future fingerprinting may strengthen this capability.

---

# Cache Integration

Execution may use caches for:

* dependency downloads;
* intermediate outputs;
* generated state;
* tool results.

Caching must follow cache safety rules.

---

# Cache Key Philosophy

A valid cache key should reflect the state that determines cached output.

Conceptually:

```text
Relevant Inputs
      +
Configuration
      +
Toolchain
      ↓
Cache Identity
```

Incomplete cache identity risks stale reuse.

---

# Cache Miss

A cache miss must result in correct recomputation.

It is not an execution failure.

---

# Cache Corruption

Invalid cache state must not silently corrupt candidate artifacts.

When detected, the build should discard or invalidate affected cache entries.

---

# Reproducible Execution

Execution SHOULD minimize uncontrolled sources of variability.

Potential influences include:

* random values;
* current time;
* file ordering;
* local paths;
* process environment;
* network responses.

---

# Time During Execution

Operational timestamps are useful for logs and metrics.

Artifact content should avoid unnecessary dependence on wall-clock time if reproducibility matters.

---

# Ordering

Generation and packaging should use deterministic ordering where the underlying artifact format is order-sensitive.

---

# Randomness

Randomness must not influence trusted artifact content unless explicitly required.

If randomness is required, its role should be documented and potentially seeded.

---

# Network Access

Execution-time network access should be minimized.

Dependencies should preferably be resolved before core transformation stages when practical.

This narrows execution variability.

---

# External Services

A build SHOULD avoid requiring live external services to generate canonical artifacts unless the dependency is architecturally necessary.

Remote mutable state weakens reproducibility.

---

# Execution Observability

The canonical package-build implementation now exposes ordered immutable
execution-stage observations through its application result.

Each reached stage records:

* canonical stage identifier;
* terminal status;
* elapsed monotonic duration;
* optional diagnostic.

The terminal statuses are:

```text
SUCCEEDED
FAILED
```

Observations preserve canonical orchestration order.

Successful execution without requested functional validation records fourteen
stages from `VALIDATE_INPUTS` through `BUILD_ARTIFACT_MANIFEST`.

When functional validation is requested and reached,
`FUNCTIONALLY_VALIDATE_WHEEL` is recorded as the fifteenth and final stage.

Mandatory failure is fail-fast. The failing stage is recorded with `FAILED`,
including its diagnostic when available, and later dependent stages are not
reported as executed.

The CLI renders this ordered observation history without becoming the owner of
the underlying execution state.

This implementation closes the current Level 13 requirements to define build
execution stages and add execution-stage logging.

The current execution-observability contract remains deliberately bounded. It
does not yet provide:

* stage start or end timestamps;
* per-stage tool invocation records;
* retry history;
* cancellation history;
* a general-purpose event stream or distributed execution trace.

Those capabilities remain separate future concerns and are not implied by the
current terminal-stage observation model.

Build execution must expose enough information to understand progress and
failure.

Useful dimensions include:

* build ID;
* target;
* profile;
* reached execution stages;
* terminal stage status;
* stage duration;
* artifact count;
* warnings;
* failure stage and diagnostic.

---

# Logging

Execution logs should be:

* structured enough to interpret;
* concise enough to remain useful;
* detailed enough for diagnostics;
* free of secrets.

---

# Log Levels

A future execution interface may support levels such as:

```text
ERROR
WARNING
INFO
DEBUG
```

The exact mechanism is implementation-specific.

---

# Debug Mode

Debug execution may provide additional diagnostics.

Debug mode MUST NOT silently change artifact semantics unless clearly documented.

---

# Quiet Mode

Automation may request reduced console output.

Important failures must remain visible.

---

# Execution Metrics

Potential metrics include:

* total build duration;
* stage duration;
* generation duration;
* packaging duration;
* cache hit rate;
* retry count;
* failure rate.

Metrics should support decisions rather than create noise.

---

# Build Duration

Build duration should be measured at well-defined boundaries.

A useful model may distinguish:

```text
Preparation Time
Execution Time
Artifact Processing Time
Validation Time
```

This helps identify bottlenecks.

---

# Performance Optimization

Execution performance should be optimized only after correctness and reproducibility are protected.

Potential techniques include:

* caching;
* incremental execution;
* parallel stages;
* reused environments.

---

# Performance Regression

Significant build-time regressions should be investigated when they materially impact developer or CI productivity.

The Quality Framework may eventually formalize thresholds.

---

# Resource Consumption

Build execution consumes:

* CPU;
* memory;
* storage;
* network.

Resource assumptions should remain reasonable and observable where needed.

---

# Disk Usage

Large temporary or artifact output may require cleanup controls.

Build systems should avoid unbounded accumulation of derived state.

---

# Execution Security

Build execution is security-sensitive because tools and dependencies may execute code with access to source and environment.

Security principles include:

* least privilege;
* secret minimization;
* controlled network access;
* trusted tooling;
* workspace isolation;
* output integrity.

---

# Secret Exposure

Ordinary build stages SHOULD not require release or production secrets.

If a build stage requires a secret, exposure must be limited to that stage.

---

# Command Injection

Build inputs or configuration that reach shell commands must be handled safely.

Dynamic shell composition should be minimized.

---

# Untrusted Input

External or user-controlled input should not automatically become executable build instructions.

Validation boundaries must be explicit.

---

# Subprocess Execution

When build tooling invokes subprocesses, command, arguments, environment, and working directory should remain controlled.

---

# Environment Propagation

Child processes should receive only necessary environment state where practical.

Blindly propagating all environment variables can expose secrets or create hidden dependencies.

---

# File Permissions

Generated artifacts should use appropriate filesystem permissions.

Build execution must not accidentally produce over-privileged files.

---

# Artifact Modification After Execution

Candidate artifacts may undergo validation and metadata inspection after execution.

However, any modification that changes artifact bytes should be treated as part of the build transformation and occur before final trust is established.

---

# Execution And Artifact Integrity

The flow should be:

```text
Build Transformation
       ↓
Final Candidate Bytes
       ↓
Integrity Calculation
       ↓
Validation
       ↓
Trusted Artifact
```

Integrity data calculated before later mutation would be invalid.

---

# Execution Finalization

Canonical package-build execution has an explicit terminal finalization
boundary.

Every terminal path from `RunPackageBuildUseCase.execute()` passes through the
centralized `_finalize_result()` boundary before returning its
`CanonicalPackageBuildResult`.

Finalization records `FINALIZE_EXECUTION` after the last business stage reached
by the build.

The canonical terminal pattern is:

    Last Reached Business Stage
            ↓
    FINALIZE_EXECUTION
            ↓
    CanonicalPackageBuildResult

`FINALIZE_EXECUTION` records successful establishment of the terminal execution
result. It does not overwrite or reinterpret the underlying build outcome.

A failed package execution therefore remains failed:

    PACKAGE [FAILED]
            ↓
    FINALIZE_EXECUTION [SUCCEEDED]
            ↓
    CanonicalPackageBuildResult [FAILED]

The failed business stage retains its diagnostic and the canonical build result
remains failed.

All current terminal paths are routed through this common finalization
boundary.

The canonical execution vocabulary contains sixteen stages through
`FINALIZE_EXECUTION`.

Successful execution without requested functional validation records fifteen
ordered observations, ending with `FINALIZE_EXECUTION`.

Successful execution with functional validation records sixteen ordered
observations, with `FUNCTIONALLY_VALIDATE_WHEEL` immediately preceding
`FINALIZE_EXECUTION`.

Finalization is intentionally distinct from cleanup. It does not delete the
Build-ID-scoped workspace, staging state, intermediate state, or partial
candidate outputs. It does not introduce cancellation or retry semantics.

Those concerns remain separate Build Execution policies.

---

# Build Result

Execution should produce a structured conceptual result.

```text
BuildExecutionResult
│
├── Build ID
├── Target
├── Profile
├── Status
├── Stage Results
├── Candidate Outputs
├── Metrics
└── Diagnostics
```

Artifact validation later enriches the overall Build Result.

---

# Stage Result

A stage result may conceptually contain:

```text
StageResult
│
├── Name
├── Status
├── Start
├── End
├── Outputs
└── Diagnostics
```

A formal implementation may be introduced when orchestration complexity justifies it.

---

# Execution Evidence

Important execution facts may become build evidence.

Examples include:

* stage statuses;
* tool versions;
* execution duration;
* output manifest;
* selected profile.

Raw verbose logs do not necessarily need permanent retention.

---

# Local Execution

Local execution should remain straightforward.

The developer should be able to:

* invoke the canonical build;
* see useful progress;
* inspect candidate artifacts;
* diagnose failure.

Local execution should not require CI-specific infrastructure.

---

# CI Execution

CI should invoke the same canonical build model.

The relationship is:

```text
CI Workflow
    ↓
Environment Setup
    ↓
Canonical Build Execution
```

CI-specific configuration should remain outside core build semantics.

---

# Release Candidate Execution

Release-candidate execution SHOULD use stronger controls.

Possible requirements include:

* clean source state;
* controlled dependencies;
* canonical toolchain;
* clean workspace;
* complete execution;
* strict artifact collection;
* complete validation.

---

# Plugin Build Execution

Plugin builds may include additional stages such as:

```text
Plugin Input Validation
        ↓
Compliance Preparation
        ↓
Plugin Packaging
        ↓
Plugin Artifact Collection
```

The canonical execution principles still apply.

---

# Documentation Build Execution

Documentation builds may execute:

* source validation;
* generation;
* reference generation;
* bundle creation.

Generated documentation can be treated as a candidate artifact where appropriate.

---

# Multi-Target Execution

Future FamilyOS workflows may build multiple targets.

A multi-target build should preserve target isolation.

Conceptually:

```text
Build Request
│
├── Target A → Artifact A
├── Target B → Artifact B
└── Target C → Artifact C
```

Failure semantics should be explicit.

---

# Fail-Fast Versus Continue

Multi-target builds may choose between:

* fail-fast;
* continue independent targets.

The policy must be explicit.

Release-candidate workflows may prefer stricter failure behavior.

---

# Execution Dependency Graph

As build complexity grows, target relationships may form a graph.

```text
Target A
   ↓
Artifact A
   ↓
Target B
```

Graph execution should only be introduced when required.

Simple linear execution remains preferred while sufficient.

---

# Build Execution API

A future internal build API may eventually expose operations such as:

```text
resolve()
validate()
execute()
collect()
finalize()
```

The Build Framework does not require implementation of this API now.

It defines the conceptual separation.

---

# CLI Execution Interface

A future CLI may expose build capabilities such as:

```text
familyos build
familyos build --profile ci
familyos build --target plugin
```

These examples are illustrative, not yet normative interface requirements.

---

# Execution Documentation

Canonical execution must be documented.

Documentation should state:

* entry command;
* prerequisites;
* profile options;
* target options;
* artifact location;
* failure behavior.

---

# Execution Change Management

Changes to execution behavior may affect:

* developer workflows;
* CI;
* artifact contents;
* release compatibility.

They must be reviewed according to impact.

---

# Low-Risk Execution Changes

Examples may include:

* clearer diagnostics;
* internal refactoring;
* safe performance improvements.

---

# High-Risk Execution Changes

Examples include:

* new build stages;
* changed packaging semantics;
* altered artifact contents;
* new external network dependency;
* changed failure policy;
* changed build/release boundary.

These may require architectural review.

---

# Execution Governance

Significant execution architecture changes may require:

* ADR;
* RFC;
* EPIC revision;
* Quality review;
* Security review.

Governance must remain proportional.

---

# Execution Technical Debt

Execution debt includes:

* duplicated commands;
* monolithic scripts;
* hidden stage coupling;
* fragile shell logic;
* unexplained retries;
* inconsistent local and CI execution;
* unbounded side effects.

This debt should be reduced continuously.

---

# Execution Anti-Pattern — Build By Shell History

A canonical build must not depend on a developer remembering previous commands.

---

# Execution Anti-Pattern — CI-Only Build

A build that can only be reproduced inside one CI workflow is too tightly coupled to automation infrastructure.

---

# Execution Anti-Pattern — Ignored Failure

Required stage failures must not be swallowed.

---

# Execution Anti-Pattern — Output Mutation After Trust

Artifacts must not be changed after integrity and validation are finalized without invalidating prior trust.

---

# Execution Anti-Pattern — Hidden Network Calls

Canonical artifact generation should not unexpectedly depend on live remote services.

---

# Execution Anti-Pattern — Shared Mutable Workspace

Concurrent builds should not accidentally overwrite each other's state.

---

# Execution Anti-Pattern — Unbounded Retry

Repeated retry of deterministic failures hides defects and wastes resources.

---

# Execution Anti-Pattern — Packaging And Publishing Combined

Official publication must remain in Release Framework scope.

---

# Execution Maturity Model

FamilyOS build execution maturity may evolve through:

```text
Level 1
Documented Manual Execution

    ↓

Level 2
Canonical Build Command

    ↓

Level 3
Structured Execution Stages

    ↓

Level 4
Automated CI Execution

    ↓

Level 5
Reproducible Workspaces

    ↓

Level 6
Evidence-Aware Execution

    ↓

Level 7
Policy-Driven Execution
```

Each level should solve real engineering needs.

---

# Execution Success Criteria

The Build Execution model is successful when FamilyOS can answer:

1. what build was requested;
2. which target was selected;
3. which profile was active;
4. whether execution preconditions were satisfied;
5. which stages executed;
6. in which order they executed;
7. which tools performed each transformation;
8. where temporary and intermediate state existed;
9. which candidate outputs were produced;
10. why an execution failed;
11. whether retries occurred;
12. whether execution altered authoritative source;
13. whether local and CI used equivalent semantics;
14. whether build execution remained separated from release publication.

---

# Execution Invariants

The following invariants should remain true.

## Invariant 1

Build execution must begin from a resolved and validated context.

## Invariant 2

Required execution-stage failure must prevent successful build completion.

## Invariant 3

Execution output must not automatically be considered trusted.

## Invariant 4

Temporary and intermediate state must remain distinguishable from candidate artifacts.

## Invariant 5

Canonical build execution must not rely on undocumented prior shell actions.

## Invariant 6

CI must invoke canonical build semantics rather than implement a separate build.

## Invariant 7

Artifact publication must remain outside ordinary Build Execution.

## Invariant 8

Execution should not unexpectedly mutate authoritative source.

## Invariant 9

Retries must not hide deterministic engineering failures.

## Invariant 10

Execution behavior must remain observable and explainable.

---

# Execution Model Summary

The canonical FamilyOS Build Execution flow is:

```text
Receive Request
      ↓
Validate Preconditions
      ↓
Initialize Workspace
      ↓
Resolve Build Context
      ↓
Prepare Staged Inputs
      ↓
Package
      ↓
Discover Candidate Outputs
      ↓
Validate Candidate Outputs
      ↓
Establish Artifact Identity
      ↓
Establish Artifact Integrity
      ↓
Build Artifact Manifest
      ↓
Functionally Validate Wheel (when requested)
      ↓
Finalize Execution
      ↓
Return Canonical Build Result
```

This model makes execution an explicit transformation stage within the larger Build Lifecycle.

---

# Final Principle

The FamilyOS Build Execution model is founded on the following rule:

> Execution must produce predictable candidate outputs from a known build context without hiding failures, introducing uncontrolled state, or assuming that successful transformation alone establishes trust.

A build system is not reliable because a command can run.

It is reliable when execution is repeatable, observable, constrained, diagnosable, and integrated into a lifecycle where candidate outputs are subsequently identified, validated, and supported by evidence.

That is the role of Build Execution within EPIC-BLD-001.
