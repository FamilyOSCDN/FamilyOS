# Testing Framework

# 10 Regression Testing

## Overview

Regression testing protects FamilyOS against the reintroduction of previously detected defects and unintended behavioral changes.

As the platform evolves, modifications to one component can affect other components, workflows, contracts, plugins, runtime services, or system behavior.

Regression testing provides automated evidence that previously validated behavior continues to work after change.

A regression test is not defined only by its testing level.

A regression test may be implemented as:

* a unit test;
* an integration test;
* a contract test;
* a functional test;
* a system test.

What makes it a regression test is its purpose:

> to prevent a known defect or previously validated behavior from silently breaking again.

Regression testing is therefore a cross-cutting responsibility across the complete FamilyOS Testing Framework.

---

# Purpose

The purpose of regression testing is to preserve known-good behavior throughout platform evolution.

Regression testing provides confidence that:

* resolved defects do not reappear;
* existing functionality survives refactoring;
* architectural changes do not break established behavior;
* plugin evolution does not invalidate platform expectations;
* compatibility remains preserved;
* bug fixes remain effective;
* previously supported workflows continue to function;
* release changes do not introduce known classes of failure.

Regression testing converts past failures into permanent engineering knowledge.

---

# Regression Testing Principles

FamilyOS regression testing follows several core principles.

## Every Reproduced Defect Should Become Knowledge

When a defect can be reliably reproduced, the conditions that caused it should normally be captured in an automated test.

This transforms a defect from a one-time incident into a protected behavior.

---

## Test at the Lowest Effective Level

A regression test should be implemented at the lowest testing level capable of reliably reproducing the defect.

Preferred order:

```text
Unit
  │
  ▼
Contract
  │
  ▼
Integration
  │
  ▼
Functional
  │
  ▼
System
```

A fast unit regression test is generally preferable to a slow system regression test when both protect the same failure.

Higher-level regression tests should be used only when the defect genuinely depends on broader component interaction.

---

## Reproduce Before Fixing

When practical, the regression test should be written before or alongside the defect fix.

The ideal sequence is:

```text
Defect Reported
      │
      ▼
Reproduce Failure
      │
      ▼
Create Failing Test
      │
      ▼
Implement Fix
      │
      ▼
Test Passes
      │
      ▼
Retain Test Permanently
```

This provides evidence that the test actually protects the defect.

---

## Protect Behavior, Not Accidental Implementation

Regression tests should preserve the correct externally meaningful behavior.

They should not unnecessarily freeze internal implementation details.

A refactoring that preserves behavior should not require unrelated regression tests to change.

---

## Keep Regression Tests Deterministic

A regression test must reproduce the relevant behavior reliably.

Tests that fail intermittently cannot provide dependable regression protection.

---

# Regression Sources

Regression tests may originate from many sources.

Common sources include:

* production defects;
* development defects;
* integration failures;
* CI failures;
* release candidate failures;
* plugin compatibility defects;
* customer or user reports;
* security defects;
* data migration failures;
* performance-related correctness defects;
* previously flaky behavior once root cause is understood.

Every confirmed defect should trigger consideration of appropriate regression coverage.

---

# Defect Lifecycle Integration

Regression testing should be integrated into the defect resolution lifecycle.

A recommended process is:

```text
Issue
  │
  ▼
Classification
  │
  ▼
Reproduction
  │
  ▼
Root Cause Analysis
  │
  ▼
Regression Test
  │
  ▼
Fix
  │
  ▼
Validation
  │
  ▼
Closure
```

A defect should not normally be considered fully resolved until appropriate regression protection exists.

Exceptions should be justified.

---

# Regression Test Classification

Regression describes purpose rather than execution scope.

For example:

```text
Regression Purpose
      │
      ├── Unit Regression Test
      ├── Contract Regression Test
      ├── Integration Regression Test
      ├── Functional Regression Test
      └── System Regression Test
```

This allows FamilyOS to preserve the existing testing architecture while still identifying tests created for regression protection.

---

# Unit Regression Testing

Unit regression tests are preferred for isolated defects.

Examples include:

* incorrect validation;
* boundary-condition errors;
* state-transition defects;
* parsing bugs;
* serialization defects;
* incorrect calculations;
* exception handling errors.

Example:

```python
def test_parser_preserves_colon_in_value():
    result = parse_value("name:family:primary")

    assert result == "family:primary"
```

The test should reproduce the original failure condition as directly as possible.

---

# Integration Regression Testing

Integration regression tests are appropriate when a defect depends on collaboration between components.

Examples include:

* repository adapter incompatibility;
* configuration propagation errors;
* plugin registration failures;
* event routing defects;
* capability resolution problems;
* runtime lifecycle interactions.

The test should remain focused on the failing integration boundary.

---

# Contract Regression Testing

Contract regression tests should be added when a defect reveals a missing or incorrectly enforced compatibility rule.

Examples include:

* previously accepted event payload becoming invalid;
* plugin metadata incompatibility;
* capability schema drift;
* repository behavior differing between implementations;
* configuration compatibility breakage.

The contract suite should be extended so every future provider or implementation remains protected.

---

# Functional Regression Testing

Functional regression tests protect complete user-visible or business behaviors.

Examples include:

* command produces incorrect result;
* workflow fails for a specific valid input;
* capability behaves differently after refactoring;
* plugin contribution is no longer exposed;
* configuration changes break a supported scenario.

Functional regression tests should validate the observable behavior affected by the defect.

---

# System Regression Testing

System regression tests are appropriate when a defect requires the assembled platform to reproduce.

Examples include:

* startup failures;
* shutdown deadlocks;
* multi-plugin registration conflicts;
* restart persistence problems;
* environment initialization defects;
* cross-component lifecycle failures.

System regression tests should be used sparingly because they generally cost more to execute and diagnose.

---

# Regression Test Naming

Regression tests should describe the protected behavior.

They should not rely solely on issue numbers.

Preferred:

```text
test_plugin_registration_rejects_duplicate_capability
```

Less useful:

```text
test_bug_231
```

Issue identifiers may be added through metadata or comments when useful.

For example:

```python
def test_plugin_registration_rejects_duplicate_capability():
    # Regression: FAMILYOS-231
    ...
```

The test should remain understandable even if the issue tracker is unavailable.

---

# Regression Metadata

Where useful, regression tests may include metadata linking them to their origin.

Potential metadata includes:

* issue identifier;
* defect identifier;
* incident identifier;
* release identifier;
* affected component;
* original failure version.

Metadata should support traceability without becoming required for understanding the test.

---

# Minimal Reproduction

A regression test should use the smallest realistic scenario that reproduces the defect.

A minimal reproduction improves:

* execution speed;
* diagnosis;
* maintainability;
* understanding;
* stability.

Unrelated infrastructure should be removed from the test whenever possible.

---

# Boundary Conditions

Many regressions occur at boundary conditions.

Regression coverage should pay particular attention to:

* empty collections;
* missing values;
* maximum values;
* minimum values;
* duplicate identifiers;
* malformed input;
* unsupported versions;
* reordered operations;
* partial initialization;
* repeated lifecycle operations.

Boundary defects should usually be protected through focused tests.

---

# Data Regression Testing

Data-related defects may involve:

* serialization;
* deserialization;
* persistence;
* migrations;
* schema evolution;
* identifier preservation;
* legacy representations.

Regression tests should preserve representative historical data fixtures when compatibility requires it.

Example:

```text
tests/regression/fixtures/
├── configuration-v1.yaml
├── plugin-metadata-v1.yaml
└── persisted-family-v2.json
```

These fixtures should be minimal and intentionally maintained.

---

# Migration Regression Testing

Data or configuration migrations require regression protection.

Tests should verify:

* supported old representation loads correctly;
* migration produces expected new representation;
* information is not silently lost;
* invalid migration inputs fail predictably;
* migration is idempotent where required.

Migration regressions are particularly important when FamilyOS introduces persistent user data.

---

# Plugin Regression Testing

Plugins introduce additional regression surfaces.

Regression tests may protect:

* plugin discovery;
* registration;
* metadata parsing;
* capability exposure;
* contribution loading;
* lifecycle execution;
* dependency validation;
* compatibility with runtime changes.

Official plugins should preserve regression coverage for every confirmed plugin defect.

---

# Runtime Regression Testing

The runtime is a critical integration point.

Regression tests should protect defects involving:

* service registration;
* dependency resolution;
* initialization order;
* plugin activation;
* capability lookup;
* lifecycle transitions;
* shutdown;
* error propagation.

Runtime regressions should be captured at the narrowest reliable level.

---

# CLI Regression Testing

CLI regressions may affect:

* command discovery;
* parsing;
* option handling;
* exit codes;
* output;
* error behavior;
* configuration propagation.

Regression tests should focus on stable CLI contracts.

Exact human-readable output should only be asserted when it is intentionally part of the public contract.

---

# Event Regression Testing

Event-related regressions may involve:

* missing publication;
* duplicate publication;
* incorrect payloads;
* handler routing;
* ordering;
* unsupported schema versions.

Regression tests should capture the specific event behavior that failed.

---

# Configuration Regression Testing

Configuration regressions frequently occur when defaults, precedence, or schemas evolve.

Tests should protect:

* default values;
* environment overrides;
* file-based configuration;
* precedence ordering;
* deprecated keys;
* invalid configuration handling.

Previously supported configurations should remain testable throughout their defined compatibility period.

---

# Compatibility Regression Testing

Compatibility failures should result in regression protection.

This includes:

* API compatibility;
* plugin compatibility;
* event compatibility;
* capability compatibility;
* serialized data compatibility;
* configuration compatibility.

These regression tests should usually become part of the applicable contract suite.

---

# Security Regression Testing

Confirmed security defects should receive regression tests whenever safe and technically appropriate.

Examples include:

* authorization bypass;
* validation failure;
* unsafe input handling;
* sensitive data exposure;
* insecure default behavior.

Security regression tests must avoid introducing unsafe production artifacts or real secrets.

---

# Flaky Defect Regression

When a defect originally appears intermittently, the underlying cause should be identified before permanent regression coverage is accepted.

A regression test should not intentionally remain flaky simply because the original defect was intermittent.

The test should isolate the deterministic condition responsible for the failure whenever possible.

---

# Regression Test Placement

Regression tests should normally reside within the testing level that best represents their behavior.

For example:

```text
tests/
├── unit/
│   └── ...
├── integration/
│   └── ...
├── functional/
│   └── ...
└── system/
    └── ...
```

A separate regression directory may be used for scenarios that do not naturally belong elsewhere:

```text
tests/regression/
```

However, creating a separate directory should not force all regression tests out of their natural testing levels.

---

# Recommended Classification Strategy

FamilyOS should prefer dual classification:

1. place the test in its natural testing level;
2. mark it as regression where useful.

For example:

```python
@pytest.mark.integration
@pytest.mark.regression
def test_runtime_preserves_plugin_registration_order():
    ...
```

This allows execution by testing level or regression purpose.

---

# Regression Markers

Regression tests may use:

```python
@pytest.mark.regression
def test_previous_failure_condition():
    ...
```

This allows targeted execution:

```bash
pytest -m regression
```

The exact marker configuration is governed by the FamilyOS testing toolchain.

---

# Full Regression Suite

A full regression suite represents the collection of automated tests protecting established platform behavior.

It may include:

```text
Static Validation
      +
Unit Tests
      +
Contract Tests
      +
Integration Tests
      +
Functional Tests
      +
System Tests
```

Not every test must carry a regression marker for the entire suite to provide regression protection.

In practice, the complete automated test suite acts as the primary regression safety net.

---

# Targeted Regression Suites

For faster feedback, FamilyOS may define targeted regression suites based on changed areas.

Examples:

* plugin regression suite;
* runtime regression suite;
* persistence regression suite;
* configuration regression suite;
* CLI regression suite.

Targeted execution should supplement rather than permanently replace complete release validation.

---

# Change-Based Regression Selection

Future FamilyOS tooling may select regression tests based on changed components.

For example:

```text
Changed Files
     │
     ▼
Impact Analysis
     │
     ▼
Affected Components
     │
     ▼
Relevant Tests
     │
     ▼
Targeted Regression Suite
```

This can reduce feedback time while maintaining appropriate protection.

Impact analysis must be conservative enough not to omit critical tests.

---

# Regression Testing in Continuous Integration

Regression testing is a core responsibility of CI.

A typical validation pipeline may include:

```text
Change
  │
  ▼
Static Validation
  │
  ▼
Fast Test Suite
  │
  ▼
Integration / Contract Validation
  │
  ▼
Functional Validation
  │
  ▼
System Validation
```

Different pipelines may run different portions depending on context.

---

# Pull Request Regression Validation

Pull requests should execute sufficient regression coverage to detect likely unintended changes.

At minimum, this generally includes:

* unit tests;
* relevant contract tests;
* relevant integration tests.

Critical functional or system tests should also run when affected.

---

# Release Regression Validation

Release candidates require broader regression confidence.

Release validation should normally include:

* complete mandatory test suites;
* supported compatibility tests;
* critical functional workflows;
* critical system scenarios;
* official plugin validation.

A known failing regression test must not be silently ignored during release approval.

---

# Regression Test Failures

A regression test failure indicates one of several possibilities:

1. the protected behavior has broken;
2. the expected behavior has intentionally changed;
3. the test is incorrect;
4. the test environment is defective.

The failure must be investigated.

Deleting or weakening the test solely to restore a green pipeline is not acceptable.

---

# Intentional Behavioral Changes

Sometimes a regression test fails because the expected behavior has intentionally changed.

In that case:

1. verify the change is authorized;
2. confirm applicable specification updates;
3. update affected contracts;
4. update documentation;
5. update or replace the regression test;
6. verify versioning implications;
7. record breaking changes where applicable.

Regression tests should evolve with intentionally changed requirements.

---

# Obsolete Regression Tests

A regression test may become obsolete when:

* the protected feature is removed;
* the contract is no longer supported;
* the architecture eliminates the failure condition;
* the scenario is replaced by stronger coverage.

Obsolete tests may be removed only after confirming that their protection is no longer required.

Test removal should be intentional.

---

# Regression Suite Maintenance

Regression suites must be actively maintained.

Maintenance includes:

* removing obsolete duplication;
* fixing flaky tests;
* simplifying fixtures;
* improving diagnostics;
* reducing unnecessary execution cost;
* updating deprecated interfaces;
* preserving historical compatibility fixtures where needed.

A regression suite that only grows without maintenance eventually becomes expensive and difficult to trust.

---

# Duplicate Regression Coverage

Multiple tests may protect the same defect at different levels.

Some duplication can be valuable when different risks are covered.

However, unnecessary duplication should be avoided.

For example, if a unit test fully protects a parsing defect, adding an identical system scenario may provide little additional value.

Higher-level duplication should exist only when it validates meaningful broader behavior.

---

# Regression Test Performance

Regression suites can become large over time.

Performance should therefore be monitored.

Optimization strategies may include:

* test-level selection;
* parallel execution;
* fixture optimization;
* eliminating unnecessary system setup;
* removing redundant scenarios;
* caching immutable test artifacts where safe.

Performance optimization must not reduce meaningful coverage solely to improve execution speed.

---

# Regression Test Reliability

Regression tests must be trusted.

They should be:

* deterministic;
* isolated;
* reproducible;
* understandable;
* maintainable;
* diagnostically useful.

Repeatedly flaky regression tests should be treated as engineering defects.

---

# Historical Fixtures

Some regression scenarios require historical representations.

These may include:

* previous schema versions;
* old configuration formats;
* old plugin metadata;
* serialized entities;
* migration inputs.

Historical fixtures should be explicitly versioned and documented.

They should not contain production personal data.

---

# Regression Coverage

Regression coverage cannot be measured solely through code coverage percentages.

Meaningful regression protection considers whether important historical failure modes remain protected.

Useful indicators may include:

* defects with regression tests;
* recurring defect rate;
* escaped regressions;
* flaky regression tests;
* critical workflows protected;
* compatibility scenarios protected.

Metrics should guide improvement rather than become arbitrary targets.

---

# Escaped Regressions

An escaped regression is a previously working behavior that breaks without being detected before reaching a later environment or release.

Every escaped regression should trigger analysis of:

* why existing tests did not detect it;
* whether the appropriate testing level was missing;
* whether test selection omitted relevant coverage;
* whether requirements were unclear;
* whether environment differences contributed.

The resulting improvement should strengthen the framework.

---

# Root Cause and Regression Scope

The regression test should protect the root cause when possible, not merely the visible symptom.

For example:

```text
Visible Failure
     │
     ▼
Root Cause Analysis
     │
     ▼
Minimal Failing Contract
     │
     ▼
Focused Regression Test
```

This often produces faster and more durable protection.

---

# Relationship With Unit Testing

Unit tests form the largest and fastest portion of regression protection.

Many defects should be preserved as focused unit regression tests.

This provides rapid feedback during development.

---

# Relationship With Integration Testing

Integration regression tests protect failures caused by incorrect collaboration between components.

They should remain scoped to the affected boundary rather than unnecessarily exercising the complete system.

---

# Relationship With Contract Testing

Contract regression tests are essential when a defect exposes missing compatibility guarantees.

The relevant contract should be strengthened so future implementations cannot reproduce the same incompatibility.

---

# Relationship With Functional Testing

Functional regression tests preserve user-visible and business-level behaviors.

They are especially useful when a defect cannot be represented accurately through lower-level tests.

---

# Relationship With System Testing

System regression tests protect defects requiring complete platform assembly.

Because they are more expensive, they should complement rather than replace lower-level regression tests.

---

# Relationship With Quality Engineering

Regression testing provides direct evidence of continuous quality improvement.

Each defect can strengthen the platform by adding permanent protection against recurrence.

This creates a feedback loop:

```text
Failure
  │
  ▼
Learning
  │
  ▼
Regression Test
  │
  ▼
Platform Protection
  │
  ▼
Higher Reliability
```

---

# Regression Testing Anti-Patterns

The following practices should be avoided.

## Fix Without Test

A defect may silently return if no permanent automated protection exists.

---

## Test Only the Symptom

Tests should protect the underlying failure condition where possible.

---

## Always Use System Tests

Regression tests should use the lowest effective testing level.

---

## Issue Number Only Naming

Tests must remain understandable without external issue systems.

---

## Deleting Failing Tests

A regression test should not be removed merely because it detects an inconvenient failure.

---

## Excessive Duplication

Identical regression scenarios across many levels increase maintenance cost without necessarily increasing confidence.

---

## Permanent Flakiness

An unreliable regression test cannot reliably protect behavior.

---

## Production Data Fixtures

Real sensitive data must not be retained as regression fixtures.

---

# Quality Gates

Regression validation participates in FamilyOS quality gates.

Potential gates include:

* pull request validation;
* protected branch validation;
* plugin certification;
* release candidate validation;
* final release approval.

Critical regression failures must block promotion unless the protected behavior has been intentionally changed through approved governance.

---

# Governance

Regression testing is governed by the FamilyOS Testing Framework and broader engineering governance.

Relevant sources include:

* Engineering Foundation;
* Testing Framework;
* Quality Framework;
* Build Framework;
* Release Framework;
* Plugin Architecture;
* applicable ADRs;
* applicable RFCs;
* specifications.

Changes to previously supported behavior must respect applicable compatibility and versioning rules.

---

# Evolution Strategy

FamilyOS regression testing should evolve with platform maturity.

Future improvements may include:

* automated defect-to-test traceability;
* regression impact analysis;
* changed-code test selection;
* historical compatibility matrices;
* automatic fixture version validation;
* escaped regression analytics;
* regression risk scoring;
* plugin-specific regression certification;
* release regression dashboards;
* automated regression suite optimization.

Evolution should improve feedback speed without weakening behavioral protection.

---

# Validation Checklist

A regression testing implementation is aligned with this framework when:

* [ ] reproducible defects receive appropriate automated regression coverage;
* [ ] regression tests use the lowest effective testing level;
* [ ] tests protect externally meaningful behavior;
* [ ] defects are reproduced before or alongside fixes where practical;
* [ ] regression tests are deterministic;
* [ ] regression tests are isolated;
* [ ] tests remain understandable without issue tracker access;
* [ ] defect identifiers are used only as supplemental metadata;
* [ ] compatibility defects strengthen applicable contract suites;
* [ ] plugin defects receive regression coverage where appropriate;
* [ ] runtime defects receive regression coverage where appropriate;
* [ ] configuration regressions are protected;
* [ ] migration regressions are protected where applicable;
* [ ] security defects receive safe regression coverage where appropriate;
* [ ] historical fixtures contain no production-sensitive data;
* [ ] flaky regression tests are investigated;
* [ ] obsolete regression tests are removed intentionally;
* [ ] regression suites participate in CI;
* [ ] release candidates receive appropriate regression validation;
* [ ] critical regression failures block applicable quality gates.

---

# Final Principle

Regression testing transforms past failures into permanent protection for the FamilyOS platform.

The fundamental rule is:

> A resolved defect should become lasting engineering knowledge whenever it can be represented by a reliable automated test.

By preserving focused regression coverage at the appropriate testing level, FamilyOS can continuously refactor, extend, and evolve its architecture while reducing the probability that previously solved problems return.
