# Testing Framework

# 06 Unit Testing

## Introduction

Unit testing forms the fastest and most localized verification layer of the FamilyOS Testing Framework.

Its purpose is to validate isolated behavior with precise, deterministic, and rapidly executable tests.

Unit tests provide the first line of executable confidence during development.

They are expected to detect defects close to their source and provide developers with immediate feedback when local behavior changes.

FamilyOS treats unit testing as a permanent engineering capability rather than an activity performed only after implementation.

---

# Purpose

The purpose of unit testing is to verify that individual engineering units behave according to their defined responsibilities.

Unit testing must support:

* rapid developer feedback;
* precise defect localization;
* deterministic validation;
* safe refactoring;
* behavioral regression protection;
* architectural maintainability;
* local verification before broader testing levels;
* reliable automation in continuous integration.

Unit testing must remain sufficiently lightweight to execute frequently throughout development.

---

# Unit Definition

A unit is the smallest practical behavioral boundary that can be tested independently.

Depending on the FamilyOS component, a unit may be:

```text
Function
Method
Class
Value Object
Entity Behavior
Policy
Rule
Service
Recipe
Parser
Validator
Capability Component
Configuration Component
Transformation
```

A unit is defined by behavioral responsibility rather than source-file size.

A large class may contain several independently testable behaviors.

A small function may require integration testing if its behavior fundamentally depends on external infrastructure.

---

# Governing Principle

The governing principle of FamilyOS unit testing is:

> Validate one behavioral responsibility through a controlled and deterministic boundary.

A unit test should make it easy to determine:

```text
Given
  a controlled initial state

When
  one behavior is executed

Then
  an observable result is produced
```

Failures should point directly toward the behavior responsible for the defect.

---

# Unit Testing Objectives

FamilyOS unit testing optimizes for:

```text
Speed
Isolation
Determinism
Clarity
Precision
Repeatability
Maintainability
Diagnostic Value
```

These properties are more important than maximizing the raw number of tests.

---

# Unit Testing Boundary

The canonical unit testing boundary is:

```text
Controlled Inputs
       │
       ▼
┌───────────────────┐
│  Unit Under Test  │
└───────────────────┘
       │
       ▼
Observable Behavior
```

Dependencies outside the unit boundary should either:

* remain absent;
* use lightweight real implementations;
* be replaced by controlled test doubles;
* be explicitly controlled by the test environment.

---

# Observable Behavior

Unit tests should validate observable behavior.

Observable behavior may include:

* returned values;
* state transitions;
* emitted domain events;
* raised exceptions;
* collaborator interactions when interaction itself is part of the contract;
* generated structures;
* validation results;
* policy decisions;
* rule outcomes.

Tests should avoid asserting irrelevant implementation details.

---

# Behavioral Testing

FamilyOS unit tests should primarily describe behavior.

For example:

```text
Given a valid plugin identifier
When the identifier is created
Then the identifier is preserved
```

is preferable to a test that merely mirrors internal implementation statements.

Tests should communicate why the behavior matters.

---

# Unit Test Structure

A unit test should normally contain three conceptual phases:

```text
Arrange
Act
Assert
```

Equivalent terminology may be used:

```text
Given
When
Then
```

The conceptual separation should remain clear even when the implementation is compact.

---

# Arrange Phase

The Arrange phase establishes controlled preconditions.

It may create:

* domain objects;
* configuration values;
* test doubles;
* deterministic clocks;
* temporary values;
* expected results.

Only data relevant to the behavior should be prepared.

Excessive setup often indicates that the unit boundary is too broad.

---

# Act Phase

The Act phase performs the behavior under test.

A focused unit test should normally contain one primary action.

Multiple unrelated actions may make failures ambiguous.

---

# Assert Phase

The Assert phase verifies the observable outcome.

Assertions should be:

* explicit;
* meaningful;
* minimal;
* behavior-oriented.

A test should assert everything necessary to prove the intended behavior, but nothing unrelated.

---

# Test Independence

Every unit test must be independently executable.

A unit test must not depend on:

* another test executing first;
* state created by another test;
* global mutable state left by previous execution;
* shared temporary resources;
* execution ordering.

The following must hold:

```text
Test A
Test B
Test C

A → PASS independently
B → PASS independently
C → PASS independently
```

Any execution order should produce equivalent results.

---

# Determinism

Given the same controlled inputs and execution environment, a unit test must produce the same result.

Conceptually:

```text
Same Input
+
Same Controlled State
+
Same Code
=
Same Test Outcome
```

Sources of nondeterminism must be controlled.

---

# Time Control

Tests involving time should not depend directly on uncontrolled wall-clock time.

Problematic behavior includes:

```text
current_time = now()
```

when the result depends on the exact execution instant.

Preferred designs introduce controllable time boundaries.

Conceptually:

```text
Clock
  │
  ├── Production Clock
  │
  └── Controlled Test Clock
```

This enables exact assertions.

---

# Randomness Control

Random behavior must be deterministic during unit testing.

Possible approaches include:

* deterministic seeds;
* injectable generators;
* fixed test values;
* controlled factories.

Tests must not fail unpredictably because random values happened to produce an unusual case.

---

# Identifier Control

Automatically generated identifiers may also introduce nondeterminism.

Where identifier values matter to assertions, tests should use controlled identifiers or injectable generators.

Tests should not rely on incidental generated values.

---

# Environment Isolation

Unit tests must not depend unnecessarily on developer-machine configuration.

Examples of environment dependencies to avoid include:

* user home directory content;
* installed local services;
* machine-specific paths;
* shell configuration;
* local credentials;
* external environment variables not controlled by the test.

Required environment state must be explicitly established.

---

# Network Isolation

Unit tests should not perform external network operations.

External HTTP services, APIs, cloud systems, package registries, or remote databases belong outside the normal unit boundary.

Network-dependent behavior should be validated through higher-level testing where appropriate.

---

# Filesystem Isolation

Unit tests should avoid persistent filesystem dependencies.

If filesystem behavior is genuinely part of the unit responsibility, tests should use controlled temporary locations.

They must not rely on arbitrary files already present on the developer machine.

---

# Database Isolation

Production databases must never be required for unit testing.

Database collaboration normally belongs to integration testing.

If local behavior depends on a repository abstraction, a controlled fake or other suitable test double may be used.

---

# External Service Isolation

External services must not be necessary to execute the unit suite.

Examples include:

```text
GitHub
Cloud APIs
Email Services
External Identity Providers
Remote Registries
Third-Party APIs
```

Tests requiring those systems belong to broader testing boundaries.

---

# Test Doubles

Test doubles may be used to control dependencies outside the unit boundary.

Canonical categories include:

```text
Stub
Fake
Mock
Spy
Dummy
```

The appropriate test double depends on the behavior being validated.

Detailed test-double governance is defined by `12-Mocks-and-Test-Doubles.md`.

---

# Stubs

A stub provides controlled responses required by the test.

Conceptually:

```text
Unit
 │
 ▼
Stub Dependency
 │
 ▼
Known Response
```

Stubs are useful when collaborator output influences the behavior under test.

---

# Fakes

A fake provides a lightweight working implementation.

Examples may include:

* in-memory repositories;
* deterministic clocks;
* in-memory registries;
* lightweight event collectors.

Fakes can reduce excessive interaction-based testing.

---

# Mocks

Mocks validate expected interactions.

They should be used when interaction itself is behaviorally significant.

Examples include verifying that:

* an event is published;
* a repository operation is requested;
* a security boundary is invoked.

Mocks should not be used merely because mocking is convenient.

---

# Avoid Excessive Mocking

Excessive mocking can create tests that validate implementation structure instead of behavior.

For example:

```text
Unit
 ├── Mock A
 ├── Mock B
 ├── Mock C
 ├── Mock D
 └── Mock E
```

may indicate excessive coupling or an inappropriate unit boundary.

Tests should prefer simple real collaborators when they are deterministic and inexpensive.

---

# Mocking Internal Details

Private implementation details should not normally be mocked.

Tests should interact through stable behavioral boundaries.

Mocking internal methods creates fragile coupling between tests and implementation structure.

---

# Interaction Assertions

Interaction assertions are appropriate when the interaction is part of the required behavior.

They are less appropriate when only the final outcome matters.

The framework therefore prefers:

```text
State / Result Verification
```

unless:

```text
Interaction Verification
```

is required to prove the contract.

---

# Positive Cases

Unit tests should cover expected valid behavior.

Examples include:

* valid identifier creation;
* accepted configuration;
* successful policy evaluation;
* valid state transitions;
* supported contribution resolution.

Positive tests establish the expected operating path.

---

# Negative Cases

Unit tests should also validate invalid behavior.

Examples include:

* malformed identifiers;
* unsupported states;
* invalid metadata;
* rejected configuration;
* prohibited transitions;
* incompatible values.

Negative behavior is part of the contract.

---

# Boundary Cases

Boundary conditions should receive explicit attention.

Examples include:

```text
Minimum Value
Maximum Value
Empty Collection
Single Item
Missing Optional Value
Maximum Allowed Length
Exact Threshold
Threshold ± 1
```

Boundary defects frequently remain invisible when only typical values are tested.

---

# Error Behavior

Expected errors should be tested explicitly.

Tests should validate the appropriate observable contract.

Depending on the component, this may include:

* exception type;
* error code;
* validation result;
* failure status;
* structured finding.

Tests should not rely unnecessarily on unstable implementation-specific error text.

---

# Exception Testing

When an exception is part of the behavioral contract, the test should validate it intentionally.

Conceptually:

```text
Invalid Input
     │
     ▼
Unit Under Test
     │
     ▼
Expected Exception
```

Unexpected exceptions indicate test failure.

---

# Domain Model Unit Testing

Domain models should be heavily unit-testable.

Typical targets include:

* invariants;
* value-object validation;
* entity state transitions;
* domain policies;
* domain rules;
* domain events;
* calculations.

Domain behavior should generally not require infrastructure to validate.

---

# Value Object Testing

Value objects should be tested for:

* valid construction;
* invalid construction;
* equality;
* normalization where defined;
* immutability expectations;
* serialization where part of their contract.

---

# Entity Testing

Entity tests should focus on behavior and invariants.

Examples include:

* permitted state transitions;
* prohibited transitions;
* identity preservation;
* domain event generation;
* invariant enforcement.

---

# Policy Testing

Policies should normally be testable as deterministic units.

A policy test should establish:

```text
Context
   │
   ▼
Policy
   │
   ▼
Decision
```

Both permitted and denied outcomes should be covered where relevant.

---

# Rule Testing

Rules should expose deterministic outcomes for controlled inputs.

Rule tests should validate:

* applicability;
* passing behavior;
* failing behavior;
* relevant severity or metadata when part of the rule contract;
* edge cases.

---

# Service Testing

Services may be unit tested when collaborators can be controlled without destroying the behavior being validated.

A service with many required mocks may indicate that integration testing provides more meaningful assurance.

---

# Parser Testing

Parsers should validate:

* valid inputs;
* invalid inputs;
* missing fields;
* malformed structures;
* boundary values;
* normalization behavior;
* error semantics.

Representative fixtures should remain minimal.

---

# Validator Testing

Validators should be tested for:

```text
Valid Input     → Accepted
Invalid Input   → Rejected
Missing Input   → Defined Outcome
Boundary Input  → Defined Outcome
```

Validation semantics must remain explicit.

---

# Configuration Unit Testing

Configuration components may be unit tested for:

* default values;
* precedence logic;
* validation;
* normalization;
* parsing;
* missing required values.

Actual integration with environment sources belongs to integration testing where appropriate.

---

# Recipe Testing

FamilyOS generation recipes should be unit tested for:

* declared outputs;
* deterministic generation behavior;
* required metadata;
* path generation;
* template selection;
* invalid input handling.

Generated output semantics may require broader tests depending on the recipe.

---

# Capability Unit Testing

Capability implementations should be unit tested when their behavior can be meaningfully isolated.

Tests may validate:

* input validation;
* local orchestration decisions;
* return semantics;
* failure handling;
* policy enforcement.

Runtime registration and capability resolution belong primarily to integration testing.

---

# Plugin Unit Testing

Official and third-party plugins use the same unit-testing semantics as the rest of FamilyOS.

Typical plugin unit targets include:

```text
Models
Policies
Rules
Recipes
Validators
Local Capability Logic
Transformations
Configuration Logic
```

Plugin origin does not change the definition of a unit test.

---

# Built-In Plugin Expectations

Built-in plugins should maintain strong unit coverage because they are part of the governed FamilyOS distribution.

Their unit suites should provide rapid evidence before broader plugin validation executes.

---

# Third-Party Plugin Expectations

Third-party plugins may be required by compliance profiles to provide unit-testing evidence.

The Testing Framework defines the meaning of that evidence.

The Plugin Compliance Framework determines whether required evidence is present and acceptable.

---

# Naming Tests

Test names should describe behavior clearly.

A useful test name communicates:

```text
Behavior
+
Condition
+
Expected Outcome
```

For example:

```text
test_identifier_rejects_empty_value
```

is preferable to:

```text
test_identifier_1
```

Naming conventions may vary by language or framework, but semantic clarity is required.

---

# Test Readability

Tests are executable engineering documentation.

A developer should be able to understand:

* the scenario;
* the relevant precondition;
* the action;
* the expected result.

without reconstructing excessive hidden setup.

---

# Test Setup

Shared setup should be used carefully.

Useful shared setup removes irrelevant repetition.

Harmful shared setup hides important test conditions.

The test should remain understandable locally.

---

# Fixtures

Fixtures may provide reusable test state.

Fixtures should be:

* focused;
* deterministic;
* composable;
* easy to understand;
* free from unrelated state.

Detailed fixture governance is defined by `11-Test-Data-and-Fixtures.md`.

---

# Fixture Scope

Fixture scope should be as narrow as practical.

Broad shared fixtures increase coupling between tests.

Changes to one fixture should not unexpectedly alter unrelated behavioral scenarios.

---

# Test Data

Unit test data should be minimal.

Tests should not require large production-like datasets unless the behavior specifically depends on data scale.

Minimal data improves readability and diagnostic precision.

---

# Test Builders

Builders and factories may reduce repetitive setup for complex objects.

They should expose important scenario differences clearly.

A builder must not hide values that materially affect the behavior being tested.

---

# Parameterized Testing

Parameterized tests are appropriate when the same behavioral rule should be validated against multiple inputs.

Conceptually:

```text
Input A ─┐
Input B ─┼──► Same Behavioral Rule
Input C ─┘
```

Parameterized tests should not combine unrelated behaviors merely to reduce line count.

---

# Property-Based Testing

Property-based testing may complement example-based unit tests.

It is particularly useful for:

* parsers;
* serializers;
* identifiers;
* mathematical transformations;
* invariant-heavy value objects.

Generated cases must remain reproducible when failures occur.

---

# Mutation Testing

Mutation testing may be used to evaluate the effectiveness of unit tests.

It can reveal tests that execute code without meaningfully validating behavior.

Mutation score is a quality signal.

It must not become an isolated optimization target.

---

# Coverage

Unit-test coverage is an evidence signal.

Coverage may identify untested code paths.

Coverage alone does not prove correctness.

The following is invalid reasoning:

```text
100% Coverage
=
100% Correctness
```

The correct interpretation is:

```text
Coverage
+
Behavioral Assertions
+
Risk Awareness
=
Stronger Testing Evidence
```

The canonical coverage model is defined by `14-Test-Coverage.md`.

---

# Branch Coverage

Branch coverage is particularly relevant for:

* policies;
* validators;
* rules;
* state transitions;
* error handling.

Critical branches should receive explicit behavioral tests.

---

# Meaningful Coverage

FamilyOS prioritizes meaningful behavioral coverage over superficial numerical coverage.

A test that executes a branch without validating its result provides weak evidence.

---

# Unit Test Performance

The unit suite should remain fast enough for frequent execution.

Developers should be able to run relevant unit tests continuously during implementation.

Performance degradation in the unit suite is an engineering concern.

---

# Slow Unit Tests

A test classified as a unit test but requiring substantial execution time should be reviewed.

Possible causes include:

* unintended I/O;
* expensive setup;
* excessive object graphs;
* uncontrolled retries;
* hidden integration dependencies.

Classification should reflect actual semantics.

---

# Parallel Execution

Unit tests should support parallel execution where the test infrastructure allows it.

Parallel safety requires:

* no shared mutable state;
* isolated temporary resources;
* deterministic identifiers where required;
* no dependency on execution order.

---

# Repeated Execution

A healthy unit suite should survive repeated execution.

Conceptually:

```text
Run 1 → PASS
Run 2 → PASS
Run 3 → PASS
...
Run N → PASS
```

Intermittent failures indicate a determinism or isolation problem.

---

# Flaky Unit Tests

Flaky unit tests are defects in the testing system.

They must not be normalized as expected behavior.

A flaky test should be:

* investigated;
* repaired;
* reclassified if it is not truly a unit test;
* temporarily quarantined only under governed conditions.

Permanent silent exclusion is not acceptable.

---

# Failure Diagnostics

A unit-test failure should make the failing behavior easy to identify.

Useful diagnostics include:

* descriptive test names;
* focused assertions;
* meaningful assertion differences;
* minimal setup;
* precise failure messages where needed.

---

# Assertion Quality

Assertions should validate behavior directly.

Weak assertion:

```text
result is not None
```

when the actual contract requires:

```text
result.status == ACCEPTED
```

Stronger assertions provide stronger evidence.

---

# Over-Specification

Tests must avoid over-specifying behavior that is not part of the contract.

Examples include unnecessary assertions about:

* internal call ordering;
* private state;
* incidental collection ordering;
* implementation-specific object structure.

Over-specification makes safe refactoring unnecessarily difficult.

---

# Refactoring Safety

A strong unit suite should permit internal refactoring while detecting behavioral regressions.

The expected relationship is:

```text
Implementation Changes
+
Behavior Preserved
=
Tests Continue Passing
```

If harmless refactoring breaks large numbers of tests, test coupling should be reviewed.

---

# Test Maintenance

Unit tests are production engineering assets.

They require maintenance.

Obsolete tests must be updated or removed when the governed behavior changes.

Tests must not be retained merely because they once existed.

---

# Regression Tests

When a defect is fixed, a regression test should normally be introduced at the lowest appropriate level.

If the defect can be reproduced as an isolated unit behavior, the regression should normally be a unit test.

This provides fast permanent protection.

---

# Bug Reproduction

A useful defect workflow is:

```text
Observed Defect
      │
      ▼
Reproduce with Test
      │
      ▼
Confirm Failure
      │
      ▼
Implement Fix
      │
      ▼
Confirm Test Passes
```

This converts the defect into durable executable evidence.

---

# Test-First Development

FamilyOS does not require one universal development methodology.

Test-first development may be used where beneficial.

The important requirement is that expected behavior becomes executable and maintainable testing evidence.

---

# Unit Testing And Architecture

Unit-test difficulty can reveal architectural problems.

A component that is extremely difficult to unit test may contain:

* excessive responsibilities;
* hidden global dependencies;
* strong infrastructure coupling;
* uncontrolled side effects;
* unclear boundaries.

Testing feedback may therefore inform architectural improvement.

---

# Dependency Injection

Dependency injection can improve testability when external collaborators need controlled substitution.

It should be introduced for architectural clarity, not solely to satisfy mocking patterns.

---

# Pure Functions

Pure functions are naturally unit-testable because they provide:

```text
Input
  │
  ▼
Transformation
  │
  ▼
Output
```

without hidden external state.

Where appropriate, critical transformation logic should favor designs with explicit inputs and outputs.

---

# Side Effects

Side effects should be isolated behind clear boundaries.

Examples include:

* persistence;
* network access;
* filesystem writes;
* process execution;
* notifications;
* external integrations.

Local decision logic should remain independently testable where practical.

---

# Unit Tests And Public Interfaces

Tests should generally exercise stable public or behavioral interfaces.

Direct testing of private methods should be exceptional.

If a private method requires extensive independent testing, it may represent a hidden responsibility deserving its own abstraction.

---

# Security-Sensitive Unit Tests

Security-sensitive local behavior requires explicit unit testing.

Examples include:

* input validation;
* permission rules;
* policy evaluation;
* secure defaults;
* identifier restrictions;
* trust-state transitions.

Security testing may additionally require higher testing levels.

---

# Compatibility-Sensitive Unit Tests

Version parsing, compatibility decisions, and local migration rules should receive unit tests when they can be isolated.

Cross-component compatibility still requires broader evidence.

---

# Serialization Unit Tests

Serialization logic may be unit tested for:

* stable field mapping;
* required fields;
* optional fields;
* invalid values;
* round-trip behavior where applicable.

External protocol compatibility may require contract or integration testing.

---

# CLI Unit Testing

CLI-local logic may be unit tested for:

* argument parsing;
* option validation;
* command selection;
* formatting helpers;
* error mapping.

Complete command execution through the assembled application belongs to functional or system testing.

---

# Event Unit Testing

Event-producing behavior may be unit tested by observing emitted domain events through a controlled collector.

Event infrastructure delivery belongs to integration testing.

---

# Repository Logic

Repository interfaces and local mapping logic may have unit tests.

Actual database persistence belongs to integration testing.

An in-memory repository used as a fake must not be treated as evidence that the production persistence adapter works.

---

# Unit Testing Profiles

Testing profiles may define different unit-testing expectations.

Examples include:

```text
Development
Official Plugin
Release
Certification
```

A profile may define:

* required suites;
* coverage expectations;
* allowed exclusions;
* execution environments;
* evidence requirements.

Profiles do not redefine unit-test semantics.

---

# Local Development

During local development, unit tests should provide the primary rapid-feedback loop.

Developers should run:

```text
Relevant Unit Tests
```

after localized changes and:

```text
Complete Unit Suite
```

before broader validation when practical.

---

# Continuous Integration

The unit suite should normally execute early in CI.

Conceptually:

```text
Source Change
     │
     ▼
Static Validation
     │
     ▼
Unit Tests
     │
     ▼
Broader Test Levels
```

Fast failures reduce wasted pipeline execution.

---

# CI Failure Semantics

A required unit-test failure must fail the corresponding validation gate.

Required tests must not be silently ignored.

Infrastructure failures must be distinguishable from behavioral test failures.

---

# Unit Test Reporting

Reports should expose enough information to identify:

* test identity;
* outcome;
* execution duration;
* failure details;
* source revision;
* execution environment where governed.

Detailed reporting requirements are defined by `16-Test-Reporting-and-Observability.md`.

---

# Unit Testing Evidence

A successful unit-test execution may produce evidence consumed by:

* Quality Framework;
* Build Framework;
* Release Framework;
* Plugin Compliance Framework;
* certification processes.

Evidence consumers must not reinterpret what constitutes a unit test.

---

# Quality Framework Relationship

The Quality Framework may define expectations for:

* unit-test reliability;
* coverage;
* failure rates;
* flakiness;
* execution performance.

The Testing Framework remains authoritative for unit-testing semantics.

---

# Build Framework Relationship

The Build Framework may require successful unit-test evidence before artifact construction or promotion.

Build does not redefine the tests.

---

# Release Framework Relationship

The Release Framework may require successful unit suites as release evidence.

Higher release maturity may require broader testing levels in addition to unit testing.

---

# Plugin Compliance Relationship

The Plugin Compliance Framework may define rules such as:

```text
Official plugin must provide unit-test evidence
```

The compliance framework validates that requirement.

This document defines what valid unit-testing behavior means.

---

# Certification Relationship

Certification may require stronger provenance for unit-test evidence.

Examples may include:

* trusted CI execution;
* immutable source revision;
* approved toolchain;
* complete required suite;
* retained reports.

Certification remains separate from ordinary unit-test execution.

---

# Unit Test Governance

Unit-testing policy changes must follow Testing Framework governance.

Examples include changes to:

* isolation requirements;
* determinism requirements;
* mandatory evidence;
* coverage policy;
* suite classification;
* CI requirements.

---

# Unit Test Review

Code review should evaluate tests alongside production changes.

Reviewers should consider:

* whether important behavior is covered;
* whether the level is appropriate;
* whether tests are deterministic;
* whether mocks are excessive;
* whether assertions are meaningful;
* whether test names communicate behavior;
* whether regression protection is adequate.

---

# Test Deletion

Deleting a unit test requires understanding what evidence is being removed.

Deletion is appropriate when:

* behavior no longer exists;
* behavior intentionally changed;
* duplicate coverage adds no value;
* the test validates obsolete implementation details.

Deletion should not silently remove required behavioral assurance.

---

# Disabled Tests

Disabled tests must remain exceptional.

A required failing test must not simply be disabled to obtain a passing pipeline.

Temporary disabling should have:

* explicit reason;
* ownership;
* remediation path;
* governed visibility where required.

---

# Unit Test Anti-Patterns

The following patterns should be avoided:

```text
Tests dependent on execution order
Tests using production databases
Tests requiring external network access
Tests depending on developer machine state
Tests with uncontrolled time
Tests with uncontrolled randomness
Tests asserting private implementation details
Tests dominated by excessive mocking
Tests without meaningful assertions
Tests covering many unrelated behaviors
Tests silently swallowing exceptions
Tests disabled indefinitely
Tests classified as unit tests despite real integration dependencies
```

---

# Unit Testing Invariants

The FamilyOS Testing Framework establishes the following unit-testing invariants:

1. Unit tests validate isolated behavioral responsibilities.
2. Unit tests must be independently executable.
3. Unit tests must be deterministic under controlled conditions.
4. Unit tests must not depend on execution order.
5. Production databases are not unit-test dependencies.
6. External network services are not normal unit-test dependencies.
7. Uncontrolled wall-clock time must not determine test outcomes.
8. Random behavior must be reproducible.
9. Test doubles must preserve the behavioral meaning of the test.
10. Excessive mocking must not replace meaningful integration testing.
11. Tests should assert observable behavior rather than irrelevant implementation details.
12. Positive, negative, and boundary behavior should be covered according to risk.
13. Expected error behavior must be explicitly testable.
14. Regression tests should be added at the lowest appropriate level.
15. Unit tests should remain fast enough for frequent execution.
16. Flaky unit tests are testing defects.
17. Coverage is evidence but not proof of correctness.
18. Unit-test evidence may be consumed by other frameworks without semantic redefinition.
19. Plugin unit tests follow the same semantics as platform unit tests.
20. Required unit-test failures must remain visible to lifecycle gates.

---

# Unit Testing Maturity

FamilyOS unit-testing maturity can progress through the following conceptual stages:

```text
Basic
  │
  ▼
Repeatable
  │
  ▼
Deterministic
  │
  ▼
Governed
  │
  ▼
Evidence-Driven
```

Maturity should increase without sacrificing execution speed or developer usability.

---

# Minimum Unit Testing Standard

At minimum, a FamilyOS unit test should:

```text
Validate one coherent behavior
Use controlled inputs
Remain independent
Remain deterministic
Produce a meaningful assertion
Avoid unnecessary external infrastructure
Provide clear failure diagnostics
```

Tests that cannot satisfy these properties should be reviewed for correct classification.

---

# Unit Testing Decision Model

The following decision model may guide test design:

```text
Can the behavior be validated independently?
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
   Unit Test     Higher Level
        │
        ▼
Does it require external infrastructure?
        │
   ┌────┴────┐
  NO        YES
   │          │
   ▼          ▼
Remain     Reconsider
Unit       Boundary
```

---

# Final Unit Testing Principle

The governing FamilyOS unit-testing principle is:

> Unit tests must provide fast, isolated, deterministic, and behavior-focused evidence that local engineering responsibilities remain correct.

A strong unit-testing foundation enables FamilyOS to evolve rapidly while preserving confidence in domain behavior, plugin logic, platform components, architectural refactoring, and future framework implementation.
