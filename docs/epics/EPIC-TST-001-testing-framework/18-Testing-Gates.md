# Testing Framework

# 18 Testing Gates

## Overview

Testing provides evidence.

Testing gates determine whether that evidence is sufficient to allow an engineering change to progress.

The FamilyOS Testing Framework therefore defines testing gates as explicit decision points integrated into the engineering lifecycle.

A testing gate evaluates whether required validation has been completed successfully and whether known testing risks remain within acceptable limits.

Testing gates may protect:

* pull request integration;
* protected branches;
* framework changes;
* plugin changes;
* release candidates;
* production releases.

A gate is not merely a test command.

It is a policy-driven decision based on trustworthy testing evidence.

---

# Purpose

The purpose of this document is to define the official FamilyOS Testing Gate model.

It establishes principles and requirements for:

* gate architecture;
* gate inputs;
* mandatory validation;
* test-result evaluation;
* coverage evaluation;
* regression protection;
* flaky-test handling;
* skipped-test handling;
* performance evaluation;
* release gates;
* exception handling;
* gate ownership;
* gate traceability;
* gate automation;
* gate evolution.

The objective is to ensure that FamilyOS engineering progression is based on explicit evidence rather than assumptions.

---

# Core Principle

The FamilyOS Testing Framework follows this principle:

> A change must not progress beyond a protected lifecycle boundary unless the required testing evidence satisfies the applicable gate.

Testing gates convert validation results into engineering policy.

---

# Gate Model

A testing gate can be represented as:

```text
Engineering Change
        │
        ▼
Required Validation
        │
        ▼
Testing Evidence
        │
        ▼
Gate Evaluation
        │
        ├── PASS
        │      │
        │      ▼
        │   Progress
        │
        └── FAIL
               │
               ▼
            Block
```

The gate decision should be deterministic whenever the underlying policy and evidence are deterministic.

---

# Testing Gate Responsibilities

Testing gates are responsible for answering questions such as:

* Were the required tests executed?
* Did mandatory tests pass?
* Were critical tests skipped?
* Are known flaky tests affecting confidence?
* Did required regression tests execute?
* Is coverage acceptable where coverage policy applies?
* Did performance regress beyond accepted limits?
* Is validation evidence complete?
* Are unresolved testing risks acceptable for the current lifecycle stage?

The gate itself does not replace tests.

It evaluates their evidence.

---

# Gate Inputs

A testing gate may consume multiple evidence sources.

Conceptually:

```text
             Unit Tests
                 │
             Integration
                 │
              Contract
                 │
             Regression
                 │
              Coverage
                 │
            Performance
                 │
                ▼
          Testing Gate
```

Not every gate requires every input.

Requirements depend on the protected lifecycle boundary.

---

# Mandatory Evidence

Gate inputs must distinguish between:

* mandatory evidence;
* optional evidence;
* informational evidence.

Mandatory evidence directly affects the gate decision.

Optional evidence may increase confidence without blocking progression.

Informational evidence provides context for engineering review.

---

# Gate Result States

A testing gate should have explicit states.

At minimum:

```text
PASS
FAIL
```

Where useful, additional states may include:

```text
INCOMPLETE
BLOCKED
WAIVED
```

These states must have clearly defined semantics.

---

# PASS

A gate passes when:

* all required validation completed;
* all mandatory conditions were satisfied;
* no blocking testing condition remains.

A pass represents permission to progress through the protected testing boundary.

---

# FAIL

A gate fails when one or more mandatory testing requirements are not satisfied.

Typical causes include:

* required test failure;
* missing required execution;
* unacceptable regression;
* prohibited skip;
* missing mandatory report;
* failed performance threshold.

Failure should block the protected action.

---

# INCOMPLETE

A gate may be incomplete when required evidence cannot yet be evaluated.

Examples include:

* CI execution still running;
* required artifact unavailable;
* mandatory test stage not executed;
* infrastructure failure preventing validation.

Incomplete must not be interpreted as pass.

---

# BLOCKED

A gate may be blocked when external conditions prevent evaluation.

For example:

* required environment unavailable;
* dependent test infrastructure unavailable;
* required upstream validation not completed.

The distinction between blocked and failed can improve diagnosis.

---

# WAIVED

A gate may support explicit waiver under governed exceptional circumstances.

A waiver must not be equivalent to a normal pass.

It should remain visible as an exception to standard policy.

---

# Gate Hierarchy

FamilyOS may define testing gates at multiple lifecycle levels.

For example:

```text
Developer Validation Gate
        │
        ▼
Pull Request Gate
        │
        ▼
Protected Branch Gate
        │
        ▼
Release Candidate Gate
        │
        ▼
Release Gate
```

Each level may impose increasingly strict requirements.

---

# Developer Gate

A developer-level gate may define the minimum validation expected before a change is considered locally ready.

This may include:

* targeted tests;
* relevant unit tests;
* static validation;
* type validation.

The developer gate may remain primarily procedural rather than repository-enforced.

---

# Pull Request Gate

The pull request gate protects integration.

It may require:

* static validation;
* unit tests;
* relevant integration tests;
* contract tests;
* regression tests;
* required reporting.

A pull request should not become merge-eligible while mandatory testing conditions are failing.

---

# Protected Branch Gate

Protected branch gates provide stronger repository protection.

They may require:

* current validation against the integrated source state;
* complete mandatory test groups;
* no unresolved critical testing failures;
* required status checks;
* successful testing gate evaluation.

Protected branch policy should prevent accidental bypass of testing requirements.

---

# Release Candidate Gate

Release candidates require broader confidence.

A release candidate gate may include:

* full automated suite;
* regression validation;
* system testing;
* compatibility validation;
* performance validation;
* unresolved-risk review.

The gate should verify that the candidate is suitable for final release evaluation.

---

# Release Gate

The release gate is the strongest testing boundary.

It should answer:

> Does the available testing evidence provide sufficient confidence to release this version of FamilyOS?

The release gate may consider:

* complete required automated validation;
* mandatory manual validation;
* known defects;
* waived tests;
* quarantine status;
* performance status;
* compatibility status;
* release-specific acceptance criteria.

---

# Gate Composition

A gate may consist of several subordinate checks.

For example:

```text
Pull Request Testing Gate
        │
        ├── Unit Gate
        ├── Integration Gate
        ├── Contract Gate
        ├── Regression Gate
        └── Coverage Gate
```

The parent gate passes only when all mandatory child conditions are satisfied.

---

# Test Category Gates

Different testing categories may have dedicated gate rules.

Examples include:

* unit-test gate;
* integration-test gate;
* contract-test gate;
* regression-test gate;
* system-test gate;
* performance gate.

Category gates improve policy clarity.

---

# Unit Test Gate

A unit-test gate normally requires:

* required tests discovered;
* required tests executed;
* no blocking unit-test failures.

Unit tests typically form one of the earliest automated gates because they provide fast feedback.

---

# Integration Test Gate

Integration gates verify interaction between components.

Failure may indicate problems in:

* boundaries;
* adapters;
* persistence;
* service integration;
* plugin interaction.

Integration gates may execute later than unit gates because their execution cost is typically higher.

---

# Contract Test Gate

Contract testing gates protect published interfaces.

These are particularly important for FamilyOS because platform components and plugins interact through governed contracts.

A contract gate should block incompatible changes when those changes violate required interface expectations.

---

# Regression Gate

Regression gates ensure that previously known defects remain protected.

When a defect has been fixed and an appropriate regression test exists, that test should participate in future automated gate evaluation.

---

# System Test Gate

System-level gates may protect high-confidence lifecycle stages.

These gates may be too expensive for every small change but can be mandatory for:

* protected branches;
* release candidates;
* releases.

---

# Coverage Gate

Coverage may be included in gate evaluation where explicitly governed.

Coverage gates should avoid simplistic assumptions.

For example:

```text
Coverage >= Threshold
```

does not automatically guarantee strong testing.

Coverage gates should be used to protect against significant loss of validation rather than to encourage meaningless test inflation.

---

# Coverage Regression Gate

A coverage regression gate may compare current coverage against an accepted baseline.

For example:

```text
Previous Coverage
      │
      ▼
Current Coverage
      │
      ▼
Allowed Change
      │
      ├── Acceptable → PASS
      └── Excessive Drop → FAIL
```

This can be more meaningful than a single global threshold.

---

# Performance Gate

Performance gates may be used where stable benchmarks exist.

A performance gate can evaluate:

* latency;
* throughput;
* startup time;
* resource use;
* benchmark regression.

Performance gates should only be used when measurements are sufficiently stable to avoid false blocking.

---

# Performance Tolerance

Performance gates must include realistic tolerance.

For example:

```text
Baseline
   │
   ▼
Measured Result
   │
   ▼
Variance Analysis
   │
   ├── Within Tolerance → PASS
   └── Outside Tolerance → INVESTIGATE / FAIL
```

Natural environmental noise must be considered.

---

# Flaky Test Gate Policy

Flaky tests require special treatment.

A flaky test should not be silently converted into a normal pass through retries.

Gate evaluation should preserve visibility into instability.

Possible policy states may include:

```text
Stable Pass
Flaky Pass
Flaky Failure
Quarantined
```

These states may produce different gate outcomes depending on criticality.

---

# Flaky Test Blocking

Critical flaky tests may justify blocking progression because they undermine confidence in the protected behavior.

Low-risk quarantined tests may be tolerated temporarily under explicit governance.

There must be no universal assumption that flakiness is acceptable.

---

# Retry-Aware Gates

Retries must remain visible to gate logic where retries are enabled.

For example:

```text
Test
 │
 ├── Attempt 1 → FAIL
 └── Attempt 2 → PASS
```

should not necessarily be treated identically to:

```text
Test
 └── Attempt 1 → PASS
```

The difference indicates instability.

---

# Skip Gate Policy

Skipped tests require explicit gate semantics.

Not all skips are equal.

Examples include:

* intentional unsupported-platform skip;
* optional-feature skip;
* temporarily disabled test;
* missing dependency;
* unexplained skip.

Gate policy should distinguish acceptable and unacceptable reasons.

---

# Mandatory Test Skips

A mandatory test that is skipped unexpectedly should normally prevent a gate from passing.

This protects against false confidence caused by incomplete execution.

---

# Quarantine Gate Policy

Quarantined tests may be excluded from ordinary mandatory success calculations only under explicit policy.

The gate should still surface:

* quarantine count;
* affected tests;
* quarantine age;
* criticality.

Quarantine must never become invisible.

---

# Quarantine Limit

FamilyOS may define limits for acceptable quarantine.

Possible policies may include:

* no critical quarantined tests;
* maximum allowed quarantine age;
* maximum quarantine count;
* mandatory remediation ownership.

Exact thresholds may evolve.

---

# Execution Completeness

A gate must verify not only test success but execution completeness.

For example:

```text
100 required tests
99 executed
99 passed
1 missing
```

must not be interpreted as:

```text
100% success
```

The missing test matters.

---

# Discovery Completeness

Unexpected changes in discovered test counts may indicate:

* tests accidentally removed;
* discovery configuration broken;
* file renaming problems;
* environment problems.

Gate logic may compare discovered tests against expectations where useful.

---

# Missing Test Stage

If a mandatory CI stage never executed, the gate should not pass.

Examples include:

* integration job skipped unexpectedly;
* system test workflow not triggered;
* report generation failed before gate evaluation.

Absence of evidence is not evidence of success.

---

# Report Completeness

Gates relying on structured reports must verify that required reports are:

* present;
* readable;
* associated with the correct source revision;
* complete enough for evaluation.

---

# Source Revision Integrity

Gate evidence must correspond to the exact source state being evaluated.

A passing test result from an older commit must not automatically satisfy a gate for a newer commit.

---

# Stale Gate Evidence

If the source changes after validation, relevant gate evidence may become stale.

CI and repository protection should require fresh validation where applicable.

---

# Gate Automation

Testing gates should be automated where practical.

Automated gates reduce:

* inconsistent enforcement;
* human oversight;
* accidental integration;
* policy ambiguity.

Automation is particularly important for pull request and branch protection.

---

# Gate as Code

Where supported, gate policies should be represented in version-controlled configuration or code.

This provides:

* reviewability;
* traceability;
* history;
* repeatability.

Gate definitions are part of the FamilyOS engineering platform.

---

# Gate Evaluation Order

Gate checks may be evaluated progressively.

For example:

```text
Required Execution
        │
        ▼
Test Success
        │
        ▼
Skip Policy
        │
        ▼
Flaky Policy
        │
        ▼
Coverage Policy
        │
        ▼
Performance Policy
        │
        ▼
Final Decision
```

Ordering should optimize clarity and efficiency.

---

# Fail-Fast Gate Evaluation

A gate may terminate evaluation when a decisive blocking condition is found.

For example:

```text
Mandatory Unit Tests Failed
        │
        ▼
Gate FAIL
```

Further computation may be unnecessary.

However, collecting additional diagnostics may still be useful in some contexts.

---

# Aggregate Evaluation

Some gates evaluate multiple independent jobs.

For example:

```text
Linux Validation      PASS
macOS Validation      PASS
Plugin Validation     PASS
Contract Validation   PASS
                           │
                           ▼
                     Final PASS
```

A failure in any mandatory child job should affect the aggregate decision.

---

# Quality Gate Integration

Testing gates are part of the broader FamilyOS quality model.

A quality gate may consume:

```text
Testing Gate
Security Gate
Documentation Gate
Build Gate
Release Gate
```

The Testing Framework owns testing-specific evidence and policies.

The Quality Framework coordinates broader engineering quality decisions.

---

# Gate Severity

Testing conditions may have different severity.

For example:

```text
Critical
Major
Minor
Informational
```

Critical conditions should usually block progression.

Lower-severity conditions may produce warnings depending on policy.

Severity must be defined explicitly rather than inferred ad hoc.

---

# Warning Gates

Some conditions may generate a warning without blocking progression.

Examples might include:

* moderate execution-time increase;
* non-critical coverage decrease;
* aging but still permitted quarantine.

Warning conditions should remain visible.

Repeated warnings may eventually justify stricter policy.

---

# Hard Gates

Hard gates block progression automatically when conditions fail.

Typical hard gates may include:

* mandatory test failure;
* missing required test stage;
* incompatible contract change;
* critical regression;
* invalid release validation.

Hard gates should be used for conditions where bypass would create unacceptable risk.

---

# Soft Gates

Soft gates provide decision support but may allow progression.

They may be useful during early framework maturity.

For example:

```text
Performance Warning
Coverage Warning
Flaky-Test Warning
```

Soft gates can later evolve into hard gates as measurement quality improves.

---

# Progressive Enforcement

FamilyOS gate maturity may evolve progressively.

For example:

```text
Observe
   │
   ▼
Warn
   │
   ▼
Require Review
   │
   ▼
Block
```

This progression can help introduce new quality policies without destabilizing development unnecessarily.

---

# Gate Ownership

Every testing gate should have identifiable ownership.

Ownership includes responsibility for:

* policy definition;
* threshold review;
* failure investigation;
* tooling reliability;
* exception handling;
* lifecycle evolution.

Ownerless gates tend to become outdated or ignored.

---

# Component Ownership

Where gates fail because of component-specific tests, the responsible engineering area should be identifiable.

This improves remediation speed.

---

# Gate Failure Reporting

A failed gate should explain:

* which condition failed;
* which evidence caused the failure;
* where detailed diagnostics are available;
* whether remediation or exception is required.

A gate that only reports:

```text
Gate Failed
```

is insufficient.

---

# Gate Diagnostics

Useful gate diagnostics may include:

```text
Gate:
Integration Testing

Status:
FAIL

Reason:
3 mandatory integration tests failed

Evidence:
integration-results.xml

Affected Component:
communication
```

Diagnostics should remain concise but actionable.

---

# Gate Traceability

Gate decisions should be traceable to:

* source revision;
* execution;
* policy version;
* timestamp;
* evidence.

This is especially important for release decisions.

---

# Historical Gate Results

Historical gate data may support analysis of:

* failure frequency;
* recurring blockers;
* unstable components;
* policy effectiveness;
* engineering bottlenecks.

Gate history should be retained when it provides meaningful operational value.

---

# Gate Bypass

Mandatory testing gates should not be casually bypassed.

If bypass is technically supported, it must remain exceptional and governed.

---

# Exception Policy

A testing gate exception should require:

* explicit reason;
* identified approver;
* known risk;
* scope;
* expiration or remediation expectation.

An exception must be traceable.

---

# Emergency Exceptions

Emergency changes may occasionally require expedited progression.

Even in emergencies:

* testing evidence should be maximized;
* skipped validation should be documented;
* follow-up validation should occur;
* exceptions should remain auditable.

Emergency does not mean ungoverned.

---

# Waiver Expiration

Waivers should not remain open indefinitely.

Where possible, they should define:

* expiration date;
* affected version;
* affected test;
* remediation condition.

---

# No Silent Bypass

A bypassed testing gate must not appear identical to a normal pass.

For example:

```text
PASS
```

and:

```text
WAIVED
```

must remain distinguishable.

---

# Release Gate Evidence

Release gate decisions should retain durable evidence.

Relevant evidence may include:

* test reports;
* gate summaries;
* coverage reports;
* performance results;
* compatibility results;
* waiver records.

This allows future traceability of release confidence.

---

# Plugin Gates

FamilyOS official plugins may have plugin-specific gates.

These may verify:

* unit validation;
* capability behavior;
* policy behavior;
* rule behavior;
* manifest correctness;
* contract compatibility;
* runtime integration.

Plugin gates should align with the common FamilyOS testing model.

---

# Shared Platform Gates

Changes to shared FamilyOS frameworks may require broader gates.

For example:

```text
Runtime Change
     │
     ▼
Core Tests
     │
     ▼
Plugin Compatibility Tests
     │
     ▼
Integration Tests
     │
     ▼
Platform Gate
```

High-impact platform changes require broader confidence than isolated component changes.

---

# Dependency Change Gates

Dependency changes may require dedicated gate evaluation.

Relevant validation may include:

* complete test suite;
* compatibility checks;
* security checks outside this framework;
* build validation;
* performance checks where relevant.

Dependency upgrades can create broad behavior changes despite minimal source modifications.

---

# Test Framework Change Gates

Changes to the Testing Framework itself require special care.

A change to:

* fixtures;
* markers;
* test discovery;
* execution configuration;
* reporting;
* CI logic

can affect the validity of the entire testing system.

Such changes should receive broad validation.

---

# Gate Reliability

A gate must be trustworthy.

An unreliable gate creates two dangerous conditions:

```text
False Positive
Change accepted when validation should fail

False Negative
Change blocked when validation should pass
```

Both reduce confidence in engineering governance.

---

# False Positives

False-positive passes are particularly dangerous because they create false confidence.

Potential causes include:

* missing tests;
* ignored failures;
* stale evidence;
* broken report parsing;
* skipped stages.

Testing gate design should prioritize preventing false acceptance.

---

# False Negatives

False-negative failures reduce productivity.

Potential causes include:

* flaky tests;
* unstable infrastructure;
* overly strict thresholds;
* unreliable benchmarks.

False negatives should be investigated rather than normalized through repeated reruns.

---

# Gate Performance

Gate evaluation itself should remain efficient.

Most gate logic should operate on already-produced validation evidence.

It should not unnecessarily duplicate expensive test execution.

---

# Gate Observability

Gate health should be observable.

Useful signals may include:

* pass rate;
* failure rate;
* most common blockers;
* waiver count;
* gate evaluation duration;
* false failure rate;
* policy changes.

This allows the gate system itself to improve over time.

---

# Gate Policy Versioning

Gate policies evolve.

Significant policy changes should be versioned or otherwise historically traceable.

This helps explain why the same evidence may produce different decisions at different points in the framework lifecycle.

---

# Gate Evolution

Testing gates should evolve as FamilyOS matures.

Possible evolution includes:

* stronger coverage expectations;
* improved performance gates;
* expanded compatibility validation;
* stricter quarantine limits;
* better regression detection.

Gate evolution should be deliberate and evidence-based.

---

# Testing Debt and Gates

Not every testing weakness can immediately become a hard gate.

Existing testing debt may require phased improvement.

For example:

```text
Current State
    │
    ▼
Measure Debt
    │
    ▼
Introduce Warning
    │
    ▼
Reduce Debt
    │
    ▼
Enable Hard Gate
```

This supports sustainable quality improvement.

---

# Anti-Patterns

The following gate practices are discouraged or prohibited.

## Gate Without Defined Evidence

A gate must specify what it evaluates.

---

## Gate Based Only on Test Count

Test quantity alone does not demonstrate sufficient validation.

---

## Hidden Gate Conditions

Developers must be able to understand why a gate passes or fails.

---

## Stale Evidence

Old test results must not satisfy current-source validation requirements.

---

## Automatic Retry Until Pass

Repeated execution must not be used to manufacture a successful gate result.

---

## Invisible Skips

Mandatory skipped tests must remain visible.

---

## Permanent Waivers

Exceptions should not become a normal operating state.

---

## Unowned Gates

Every enforced policy must have responsible ownership.

---

## Unstable Performance Gates

Performance thresholds should not block changes when measurement noise is too high to support reliable decisions.

---

## Gate Proliferation

Too many overlapping gates can create unnecessary complexity.

Each gate should protect a clear engineering boundary.

---

# Governance

Testing gates are governed by the FamilyOS Testing Framework and broader FamilyOS engineering governance.

Changes affecting:

* mandatory gates;
* blocking criteria;
* testing thresholds;
* exception policy;
* release validation;
* gate automation;
* required test categories;
* waiver rules

must follow the appropriate governance process.

---

# Relationship With Test Reporting

Testing gates consume evidence produced according to:

```text
16-Test-Reporting-and-Observability.md
```

Reliable reporting is therefore a prerequisite for reliable gates.

---

# Relationship With Automation and CI

Automated enforcement of testing gates depends on:

```text
17-Automation-and-CI-Integration.md
```

CI provides the execution environment and integration points through which gate policies become enforceable.

---

# Relationship With Quality Framework

Testing gates provide testing-specific quality signals.

The broader FamilyOS Quality Framework may combine those signals with:

* build quality;
* security;
* documentation;
* architecture;
* release readiness.

Testing gates are therefore one layer of the wider quality governance system.

---

# Relationship With Governance and Test Lifecycle

Testing gates themselves require lifecycle governance.

Policies must be:

* introduced;
* monitored;
* reviewed;
* evolved;
* deprecated when necessary.

This lifecycle is defined further in:

```text
19-Governance-and-Test-Lifecycle.md
```

---

# Success Criteria

The FamilyOS Testing Gate model is considered effective when:

* protected changes cannot progress without required validation;
* gate requirements are understandable;
* gate evidence is traceable;
* missing execution cannot appear as success;
* stale results cannot satisfy current validation;
* flaky tests remain visible;
* skipped mandatory tests are controlled;
* exceptions remain explicit;
* release gates provide strong evidence;
* gate failures provide actionable diagnostics;
* false-positive passes are minimized;
* false-negative failures are actively reduced;
* gate policies evolve deliberately;
* testing governance remains enforceable.

---

# Final Principle

Tests determine what happened.

Reports explain what happened.

Testing gates determine whether what happened is sufficient to move forward.

The governing principle is:

> Engineering progression must be earned by evidence, not assumed from intention.

A gate does not create quality.

It prevents insufficiently validated change from being mistaken for trusted FamilyOS state.
