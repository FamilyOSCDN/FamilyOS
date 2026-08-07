# Plugin Compliance Framework

# 08 Validation Engine

## Introduction

The Validation Engine is the execution core of the FamilyOS Plugin Compliance Framework.

It transforms a compliance profile and a plugin validation context into a complete, structured compliance evaluation.

The engine coordinates:

* profile resolution;
* rule resolution;
* dependency analysis;
* validation planning;
* validator execution;
* evidence collection;
* rule evaluation;
* finding generation;
* error handling;
* result derivation;
* reporting inputs.

The engine must remain deterministic, explainable, extensible, and independent from presentation tooling.

---

# Purpose

The Validation Engine exists to provide one authoritative mechanism for evaluating plugin compliance.

It must ensure that the same plugin evaluated under the same context produces equivalent results regardless of whether validation is initiated through:

* local CLI;
* CI;
* build pipelines;
* release workflows;
* certification systems.

Consumers may differ.

Compliance semantics must not.

---

# Execution Model

The high-level execution model is:

```text
Plugin
  │
  ▼
Validation Request
  │
  ▼
Context Construction
  │
  ▼
Profile Resolution
  │
  ▼
Rule Resolution
  │
  ▼
Validation Planning
  │
  ▼
Validator Execution
  │
  ▼
Evidence Collection
  │
  ▼
Rule Evaluation
  │
  ▼
Finding Generation
  │
  ▼
Compliance Decision
  │
  ▼
Compliance Result
```

Each stage must have explicit contracts and failure semantics.

---

# Validation Request

Every engine execution begins with a validation request.

A conceptual request contains:

```text
ValidationRequest
├── plugin_target
├── requested_profile
├── execution_mode
├── platform_context
├── configuration
├── evidence_inputs
└── reporting_preferences
```

Not all consumers need to provide every field directly.

Defaults may be resolved through governed framework configuration.

---

# Plugin Target

The plugin target identifies the object being evaluated.

It may represent:

* a plugin source tree;
* an installed plugin;
* a build artifact;
* a release candidate;
* a packaged distribution;
* a future registry artifact.

The target abstraction should prevent validators from depending directly on one filesystem layout when broader artifact types become supported.

---

# Validation Context Construction

The engine must construct an explicit Validation Context before evaluating rules.

The context should include:

```text
ValidationContext
├── plugin_id
├── plugin_version
├── plugin_classification
├── plugin_target
├── platform_version
├── framework_version
├── profile_id
├── profile_version
├── execution_mode
├── source_revision
├── environment
└── configuration
```

This context becomes part of the final compliance result.

---

# Context Validation

The engine must validate its own context before compliance evaluation begins.

Examples of invalid contexts include:

* missing plugin identity;
* unsupported framework version;
* unknown requested profile;
* incompatible profile and plugin classification;
* invalid platform version;
* malformed execution configuration.

Context failures must be reported separately from plugin compliance failures.

---

# Profile Resolution

The Validation Engine delegates profile selection to the Profile Resolver.

The resolver considers:

* explicit profile selection;
* plugin classification;
* lifecycle stage;
* execution mode;
* release context;
* certification target.

The output is one exact profile version.

Conceptually:

```text
Validation Request
       │
       ▼
Profile Resolver
       │
       ▼
Resolved Profile
```

The resolved profile must be recorded in the result.

---

# Rule Resolution

Once a profile is resolved, the engine determines the Effective Rule Set.

The rule set is derived from:

```text
Profile Rules
    +
Inherited Rules
    +
Mandatory Rules
    -
Valid Exclusions
    =
Effective Rule Set
```

Only active and applicable rule versions may participate in normal evaluation.

Deprecated rules may participate when required by profile or compatibility policy.

---

# Applicability Resolution

A rule included by the profile may still be contextually not applicable.

Applicability evaluation may consider:

* plugin classification;
* capability declarations;
* contribution types;
* platform version;
* plugin version;
* lifecycle stage;
* configuration.

Rules evaluated as not applicable must produce explicit `NOT_APPLICABLE` outcomes.

They must not disappear from traceability.

---

# Rule Dependency Graph

Rules may depend on prerequisite rules.

The engine must build a dependency graph before execution when such dependencies exist.

Conceptually:

```text
RULE-A
   │
   ▼
RULE-B
   │
   ├────► RULE-C
   │
   └────► RULE-D
```

The dependency graph supports:

* deterministic ordering;
* prerequisite validation;
* cascading failure control;
* parallel execution;
* clear diagnostics.

---

# Dependency Validation

The engine must validate the rule graph itself.

Invalid rule configurations include:

* circular dependencies;
* references to unknown rules;
* dependencies on retired rules without compatibility mapping;
* contradictory profile composition.

These conditions represent framework configuration errors.

They must not be reported as plugin failures.

---

# Validation Planning

The engine generates a Validation Plan from the Effective Rule Set.

The plan identifies:

* applicable rules;
* prerequisite relationships;
* required validators;
* required evidence;
* reusable evidence;
* execution groups;
* manual validation requirements.

Conceptually:

```text
Effective Rule Set
        │
        ▼
Evidence Requirements
        │
        ▼
Validator Requirements
        │
        ▼
Dependency Analysis
        │
        ▼
Validation Plan
```

---

# Validation Plan

A conceptual plan may contain:

```text
ValidationPlan
├── evaluation_id
├── profile
├── rules
├── dependency_graph
├── validator_tasks
├── evidence_requirements
├── reusable_evidence
├── execution_groups
└── manual_review_tasks
```

The plan should be inspectable for debugging and audit purposes.

---

# Validator Selection

Rules do not directly execute themselves.

The engine selects validators according to their registered validation bindings.

A validator may satisfy evidence requirements for one or many rules.

For example:

```text
Import Graph Validator
        │
        ├── PLUGIN-ARCH-001
        ├── PLUGIN-ARCH-004
        └── PLUGIN-DEP-007
```

Validator reuse reduces unnecessary repeated analysis.

---

# Validator Registry

Validators must be resolved through a governed Validator Registry.

The registry maps logical validator identities to implementations.

Conceptually:

```text
architecture.import-boundary
metadata.schema
dependency.graph
capability.contract
testing.results
documentation.structure
```

Rules should reference logical validator identities rather than concrete implementation modules.

---

# Validator Contract

Every validator must conform to a stable contract.

A validator receives:

```text
ValidationContext
+
ValidatorInput
```

and returns:

```text
ValidatorResult
```

A conceptual result includes:

```text
ValidatorResult
├── validator_id
├── validator_version
├── status
├── evidence
├── diagnostics
├── started_at
├── completed_at
└── execution_metadata
```

Validators must never directly declare overall plugin compliance.

---

# Validator Status

Validator execution status should remain separate from rule outcome.

Conceptual validator statuses may include:

```text
SUCCESS
PARTIAL
FAILED
SKIPPED
ERROR
```

For example:

```text
Validator Status: SUCCESS
Rule Outcome: FAIL
```

means the validator executed successfully and demonstrated a compliance violation.

---

# Validator Errors

A validator crash or infrastructure failure must not be interpreted as rule failure automatically.

The engine must distinguish:

```text
Requirement Violated
        ≠
Validator Failed
```

A validator error may cause affected rules to become:

```text
ERROR
```

or:

```text
NOT_EVALUATED
```

depending on the failure semantics.

---

# Evidence Collection

Validators produce or consume evidence.

The engine coordinates evidence collection through a normalized evidence layer.

Evidence may come from:

* direct inspection;
* external engineering tools;
* trusted CI artifacts;
* previous compatible validation;
* runtime checks;
* manual review.

Every evidence item must preserve provenance.

---

# Evidence Store

The engine should expose an Evidence Store abstraction.

Conceptually:

```text
EvidenceStore
├── add()
├── get()
├── query()
├── validate_freshness()
├── validate_provenance()
└── invalidate()
```

The implementation may initially be in-memory.

The abstraction allows future persistence or distributed evidence systems.

---

# Evidence Deduplication

Equivalent evidence should not be collected repeatedly.

For example:

```text
Plugin Manifest
      │
      ▼
Metadata Parser
      │
      ▼
Shared Metadata Evidence
      │
      ├── Identity Rules
      ├── Metadata Rules
      ├── Dependency Rules
      └── Compatibility Rules
```

Evidence reuse improves performance and consistency.

---

# Evidence Freshness

Before evidence is reused, the engine must verify that it matches the current validation context.

Freshness may depend on:

* source revision;
* plugin version;
* platform version;
* dependency state;
* validator version;
* framework version.

Invalid or stale evidence must be rejected or explicitly downgraded according to policy.

---

# Trusted External Evidence

The engine may consume evidence produced outside the immediate execution.

Examples include:

* CI test results;
* MyPy output;
* Ruff output;
* security scanner results;
* build metadata;
* signed attestations.

External evidence must pass provenance and compatibility validation.

---

# Rule Evaluation

Once required evidence is available, each applicable rule is evaluated.

The conceptual model is:

```text
Rule
  +
Validation Context
  +
Evidence
  =
Rule Outcome
```

The evaluator must remain independent from report formatting.

---

# Rule Evaluator

The Rule Evaluator determines whether the requirement is satisfied.

It must consider:

* rule semantics;
* applicability;
* evidence completeness;
* prerequisite outcomes;
* validation errors;
* exception policy.

A validator may produce raw observations.

The Rule Evaluator translates those observations into compliance outcomes.

---

# Canonical Rule Outcomes

The engine should converge on a small canonical set of rule outcomes.

The preferred baseline is:

```text
PASS
FAIL
NOT_APPLICABLE
NOT_EVALUATED
ERROR
```

Warning behavior should normally be represented through severity rather than an additional ambiguous outcome state.

This keeps status and severity orthogonal.

---

# Prerequisite Failure Handling

If a prerequisite rule fails, dependent rules should not automatically generate duplicate failures.

For example:

```text
PLUGIN-META-001 -> FAIL
       │
       ▼
PLUGIN-CAP-001 -> NOT_EVALUATED
```

The dependent rule should explain that evaluation was blocked by a prerequisite.

This reduces compliance noise.

---

# Finding Generation

The engine generates findings from rule outcomes according to compliance policy.

A typical mapping is:

```text
PASS
  -> no finding

FAIL
  -> compliance finding

NOT_APPLICABLE
  -> no violation finding

NOT_EVALUATED
  -> incomplete validation finding

ERROR
  -> validation error finding
```

Findings must reference the originating rule and relevant evidence.

---

# Finding Normalization

All validators must ultimately produce findings through the same normalized Finding Model.

This prevents tool-specific output formats from fragmenting compliance reporting.

The engine may preserve native diagnostics as supporting evidence.

The canonical finding remains framework-owned.

---

# Severity Resolution

Rule severity is defined by the rule.

Profile policy determines its impact.

Conceptually:

```text
Rule Severity
      +
Profile Severity Policy
      =
Decision Impact
```

The engine must not mutate the original rule severity.

---

# Mandatory Rule Handling

Mandatory rules require special decision semantics.

A mandatory failed rule should normally prevent compliant status regardless of ordinary profile thresholds.

Conceptually:

```text
Mandatory Rule
      │
      ├── PASS -> Continue
      │
      └── FAIL -> Block Compliance
```

Governed exceptions may alter this only when the rule's exception policy permits it.

---

# Exception Evaluation

Exceptions must be resolved before final decision derivation.

The engine validates:

* exception identity;
* affected rule;
* scope;
* authority;
* expiration;
* applicability.

Invalid or expired exceptions must not influence compliance status.

---

# Suppression Evaluation

Suppressions may affect finding presentation or workflow handling.

They must not erase the underlying rule outcome.

Conceptually:

```text
Rule FAIL
   │
   ▼
Finding
   │
   ▼
Suppression Applied
   │
   ▼
Finding Remains Traceable
```

---

# Compliance Decision

After all applicable rule outcomes are resolved, the engine derives the overall Compliance Result.

The decision considers:

```text
Rule Outcomes
      +
Mandatory Rules
      +
Severity Policy
      +
Exceptions
      +
Evidence Completeness
      =
Compliance Status
```

The algorithm must be documented and deterministic.

---

# Overall Compliance States

A compact overall status model is preferred.

The baseline model is:

```text
COMPLIANT
NON_COMPLIANT
INCOMPLETE
ERROR
```

## COMPLIANT

All required blocking rules are satisfied according to the active profile.

## NON_COMPLIANT

One or more blocking requirements are violated.

## INCOMPLETE

Required compliance decisions could not be completed because evidence or required validation is missing.

## ERROR

The framework encountered a failure severe enough to prevent a reliable compliance decision.

---

# Status Precedence

When multiple conditions exist, precedence must be explicit.

A conceptual precedence may be:

```text
ERROR
  >
NON_COMPLIANT
  >
INCOMPLETE
  >
COMPLIANT
```

The final policy must define exact semantics.

The engine must not derive status through undocumented heuristics.

---

# Deterministic Execution

The engine must produce equivalent semantic results for equivalent validation contexts.

Determinism applies to:

* profile resolution;
* rule resolution;
* dependency planning;
* evidence interpretation;
* rule evaluation;
* decision derivation.

Parallel execution may change timing.

It must not change outcome semantics.

---

# Parallel Execution

Independent validators may execute concurrently.

For example:

```text
                 Validation Plan
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    Metadata       Architecture     Testing
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                    Evidence
```

The engine must ensure deterministic aggregation regardless of execution order.

---

# Concurrency Safety

Parallel validation requires:

* immutable validation context;
* thread-safe or process-safe evidence handling;
* deterministic finding ordering;
* isolated validator failures;
* explicit shared-resource contracts.

Concurrency is an optimization.

It must not leak into compliance semantics.

---

# Finding Ordering

Reports should produce stable finding order.

A canonical sorting strategy may use:

```text
Domain
Rule ID
Severity
Location
```

Stable ordering improves:

* reproducibility;
* CI diffs;
* developer experience;
* testing.

---

# Incremental Validation

The engine should support future incremental execution.

Incremental validation may reuse valid evidence for unchanged areas.

Potential inputs include:

* source diff;
* dependency diff;
* changed plugin metadata;
* affected compliance domains;
* rule dependencies.

The engine must always prefer correctness over optimization.

---

# Invalidation

Evidence must be invalidated when relevant context changes.

Examples:

```text
Source changed
  -> source-derived evidence invalid

Dependencies changed
  -> dependency evidence invalid

Platform version changed
  -> compatibility evidence may be invalid

Rule implementation changed
  -> validator evidence may require regeneration
```

Invalidation rules should themselves be explicit.

---

# Execution Modes

The engine may support execution modes such as:

```text
FAST
STANDARD
FULL
CERTIFICATION
```

Execution mode controls strategy, not compliance meaning.

A mode may influence:

* expensive validator execution;
* evidence reuse;
* runtime checks;
* manual review scheduling.

The active profile still determines required assurance.

---

# Fast Execution

FAST mode may prioritize validators that are:

* inexpensive;
* local;
* deterministic;
* high-value during development.

If required profile rules remain unevaluated, the result must be `INCOMPLETE` rather than falsely compliant.

---

# Full Execution

FULL mode attempts to evaluate all rules required by the profile.

It may include:

* complete test evidence;
* lifecycle tests;
* documentation checks;
* security validation;
* compatibility verification.

FULL mode is suitable for release preparation.

---

# Certification Execution

CERTIFICATION mode may require stronger evidence provenance and forbid certain shortcuts.

Examples include:

* release artifact validation;
* trusted CI evidence;
* signed attestations;
* restricted exceptions;
* full evidence completeness.

Certification mode still produces compliance evidence rather than certification itself.

---

# Manual Review Integration

The engine must support rules requiring manual review.

Manual tasks should appear explicitly in the validation plan.

Conceptually:

```text
Automated Validation
       │
       ▼
Manual Review Required
       │
       ▼
Review Evidence
       │
       ▼
Rule Evaluation
```

Until required review evidence exists, affected rules remain `NOT_EVALUATED`.

---

# Cancellation

Validation execution may support cancellation.

Cancellation must produce an explicit incomplete execution state.

A cancelled run must never emit a complete compliance result.

Partial evidence may be retained if clearly marked.

---

# Timeouts

Validators may require execution timeouts.

A timeout is an infrastructure or validation execution issue.

It must not automatically become a plugin violation.

Affected rules should become `ERROR` or `NOT_EVALUATED` according to policy.

---

# Retry Policy

Some validator failures may be retryable.

Retry behavior must be controlled.

Retries must not hide persistent validation failures.

The final result should preserve retry diagnostics where relevant.

---

# Engine Diagnostics

The engine should produce diagnostic information separate from compliance findings.

Diagnostics may include:

* validator load failure;
* profile registry error;
* rule graph error;
* evidence corruption;
* timeout;
* unsupported configuration.

This separation helps determine whether the plugin or the compliance infrastructure requires correction.

---

# Audit Trail

Every validation execution should produce enough metadata for audit.

The audit trail should identify:

```text
Evaluation ID
Plugin
Source Revision
Platform Version
Framework Version
Profile
Rule Set
Validator Versions
Evidence Sources
Exceptions
Start Time
Completion Time
Final Status
```

This metadata may be embedded in the structured Compliance Result.

---

# Evaluation Identity

Every complete validation run should receive a unique Evaluation ID.

The Evaluation ID allows:

* report correlation;
* evidence correlation;
* certification reference;
* historical comparison;
* audit tracking.

It identifies an execution instance, not a plugin identity.

---

# Result Immutability

A finalized Compliance Result should be treated as immutable.

If evidence or rules change, the system should create a new evaluation rather than modifying historical results.

Conceptually:

```text
Evaluation A -> Result A
Evaluation B -> Result B
```

Historical results remain interpretable in their original context.

---

# Engine Extension Points

The Validation Engine may expose governed extension points for:

* validators;
* evidence adapters;
* result renderers;
* execution strategies.

Extensions must not be allowed to redefine:

* compliance rule meaning;
* mandatory rule semantics;
* decision policy;
* profile security constraints.

---

# Plugin Isolation

The plugin under evaluation must not be able to control compliance execution.

Plugins must not:

* register validators that validate their own mandatory compliance;
* modify active rule definitions;
* override severity policy;
* suppress findings silently;
* replace compliance decision logic.

This preserves the compliance trust boundary.

---

# Engine API Boundary

The engine should expose a stable service interface.

Conceptually:

```text
ComplianceEngine.evaluate(request) -> ComplianceResult
```

Additional APIs may support:

```text
plan()
explain()
validate_context()
```

Consumers should depend on these service contracts rather than engine internals.

---

# CLI Consumer

The CLI should invoke the Validation Engine and render its structured result.

The CLI must not duplicate:

* profile resolution;
* rule resolution;
* severity policy;
* final compliance logic.

Its responsibility is user interaction and presentation.

---

# CI Consumer

CI should invoke the same engine interface.

It may convert compliance status into pipeline exit codes.

For example:

```text
COMPLIANT      -> success
NON_COMPLIANT  -> failure
INCOMPLETE     -> failure or policy-specific state
ERROR          -> infrastructure failure
```

Exact exit-code semantics belong to CLI and CI integration specifications.

---

# Release Consumer

Release workflows may require a specific profile and execution mode.

For example:

```text
Profile: release
Mode: FULL
```

The release system consumes the result.

It does not independently reinterpret rule outcomes.

---

# Certification Consumer

Certification infrastructure consumes structured compliance evidence.

It may verify:

* profile;
* result status;
* evidence provenance;
* execution identity;
* framework version.

Certification remains a separate governance layer.

---

# Performance Objectives

The engine should be designed to scale with increasing:

* rule counts;
* plugin counts;
* validator complexity;
* evidence volume;
* profile complexity.

Performance strategies may include:

* validator reuse;
* evidence reuse;
* parallel execution;
* incremental validation;
* caching.

No optimization may weaken compliance correctness.

---

# Observability

The engine should expose operational telemetry for its own execution.

Useful metrics may include:

* evaluation duration;
* validator duration;
* rule counts;
* evidence counts;
* validator failures;
* cache reuse;
* incomplete evaluations.

Operational observability is distinct from plugin compliance reporting.

---

# Engine Testing

The Validation Engine itself requires extensive tests.

Core test categories include:

* context validation;
* profile resolution;
* rule resolution;
* dependency graph construction;
* validator execution;
* evidence reuse;
* rule evaluation;
* exception handling;
* error propagation;
* decision derivation;
* deterministic output;
* parallel execution.

Compliance infrastructure must meet at least the quality level expected from the plugins it evaluates.

---

# Reference Execution Flow

The complete reference execution is:

```text
Validation Request
       │
       ▼
Validate Request
       │
       ▼
Build Validation Context
       │
       ▼
Resolve Profile
       │
       ▼
Resolve Effective Rule Set
       │
       ▼
Evaluate Applicability
       │
       ▼
Build Rule Dependency Graph
       │
       ▼
Create Validation Plan
       │
       ▼
Resolve Existing Evidence
       │
       ▼
Execute Required Validators
       │
       ▼
Normalize Evidence
       │
       ▼
Evaluate Rules
       │
       ▼
Generate Findings
       │
       ▼
Apply Exceptions and Suppressions
       │
       ▼
Derive Compliance Status
       │
       ▼
Finalize Compliance Result
```

This sequence defines conceptual responsibility, not necessarily strict physical execution order.

---

# Engine Invariants

The Validation Engine establishes the following invariants:

1. Every validation run has an explicit context.
2. Every run resolves one exact compliance profile.
3. Every evaluated rule belongs to the Effective Rule Set.
4. Rule dependencies are explicit.
5. Validators do not declare overall compliance.
6. Validator failures remain distinct from rule failures.
7. Evidence has provenance.
8. Stale evidence cannot silently satisfy current requirements.
9. Rule outcomes are normalized.
10. Unknown evaluation never becomes PASS.
11. Findings derive from governed rules.
12. Mandatory rule failures cannot be silently ignored.
13. Exceptions and suppressions remain traceable.
14. Final status is derived deterministically.
15. Parallel execution does not change semantics.
16. Finalized results are immutable.
17. Consumers do not reimplement compliance logic.
18. Plugins cannot alter the rules governing their own compliance.

---

# Engine Summary

The Validation Engine transforms a plugin and a governed compliance context into a reproducible compliance result.

The complete model is:

```text
Plugin
  +
Validation Context
  +
Compliance Profile
  +
Rule Catalog
  +
Validators
  +
Evidence
  =
Compliance Result
```

The engine provides the operational foundation required to make FamilyOS plugin compliance executable rather than merely documented.

---

# Final Engine Principle

The governing principle of the Validation Engine is:

> Validation execution may be optimized, distributed, or extended, but the meaning of compliance must remain deterministic and centrally governed.

This principle ensures that every FamilyOS compliance consumer can trust that a compliance result has the same semantic meaning regardless of where or how it was produced.
