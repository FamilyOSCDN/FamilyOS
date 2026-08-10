# Testing Framework

# 05 Testing Levels

## Introduction

The FamilyOS Testing Framework defines a layered testing model.

Each testing level exists to answer a different engineering question.

The purpose of the testing-level model is to prevent:

* unnecessary duplication;
* inappropriate test scope;
* excessive execution cost;
* weak confidence;
* ambiguous test responsibilities;
* overreliance on high-level tests;
* excessive mocking;
* unclear lifecycle expectations.

Testing levels must remain semantically distinct.

They may share infrastructure.

They must not collapse into one undifferentiated test suite.

---

# Purpose

The purpose of this document is to define the canonical FamilyOS testing levels and the responsibility of each level.

The framework recognizes the following primary levels:

```text
Unit
Integration
Contract
Functional
System
```

Additional specialized testing categories may complement these levels.

Examples include:

```text
Regression
Performance
Security
Compatibility
Migration
Resilience
```

These specialized categories describe testing objectives.

They do not automatically replace the primary level classification.

---

# Governing Principle

The governing principle for testing levels is:

> Validate behavior at the lowest level that can provide trustworthy evidence for that behavior.

The lowest level is preferred because it normally provides:

* faster feedback;
* stronger isolation;
* easier diagnosis;
* lower execution cost;
* greater determinism.

Higher levels are required when behavior depends on real collaboration or assembled-system behavior.

---

# Testing Level Model

The canonical testing-level progression is:

```text
Unit
 │
 ▼
Integration
 │
 ▼
Contract
 │
 ▼
Functional
 │
 ▼
System
```

The model does not imply that every feature requires every level.

Required levels depend on:

* architectural boundaries;
* risk;
* lifecycle context;
* contract criticality;
* implementation complexity.

---

# Testing Level Responsibility

Each level answers a different question.

```text
Unit
  -> Does this isolated behavior work correctly?

Integration
  -> Do real components collaborate correctly?

Contract
  -> Does this boundary satisfy its agreed contract?

Functional
  -> Does the requested capability behave correctly?

System
  -> Does the assembled FamilyOS system operate correctly?
```

Testing confidence emerges from the combination of these answers.

---

# Unit Testing

## Definition

Unit testing validates isolated behavior within the smallest practical engineering boundary.

A unit may be:

* function;
* class;
* policy;
* rule;
* value object;
* service;
* recipe;
* capability implementation;
* small component.

The exact unit boundary depends on architecture.

---

# Unit Testing Objective

Unit tests should provide fast and precise evidence that local behavior is correct.

They optimize for:

```text
Speed
Isolation
Determinism
Diagnostic Precision
```

---

# Unit Test Boundary

Conceptually:

```text
Controlled Input
      │
      ▼
Unit Under Test
      │
      ▼
Observable Result
```

External dependencies should normally be absent or controlled.

---

# Unit Test Characteristics

A strong unit test is typically:

* fast;
* isolated;
* deterministic;
* focused;
* easy to understand;
* easy to reproduce;
* independent of network access;
* independent of shared databases;
* independent of execution order.

---

# Unit Test Dependencies

Unit tests may use:

* real lightweight collaborators;
* fakes;
* stubs;
* mocks;
* controlled clocks;
* deterministic random generators.

The chosen dependency strategy must preserve the behavior being tested.

---

# Unit Test Examples

Examples include validating:

* identifier validation;
* policy evaluation;
* rule behavior;
* configuration parsing;
* domain state transitions;
* recipe generation logic;
* capability-local behavior;
* error handling.

---

# Unit Test Anti-Patterns

Unit tests should avoid unnecessary dependence on:

* actual network services;
* full application startup;
* production databases;
* unrelated plugins;
* filesystem state outside controlled temporary locations.

If these dependencies are required, the test may belong to a higher level.

---

# Unit Testing Success Criteria

Unit testing is effective when:

* failures identify local defects precisely;
* the suite runs quickly;
* tests remain deterministic;
* implementation changes do not require unnecessary test rewrites;
* core behavioral branches are covered meaningfully.

---

# Integration Testing

## Definition

Integration testing validates real collaboration between multiple components.

The focus is not on complete end-user functionality.

The focus is on the interaction boundary.

---

# Integration Testing Objective

Integration tests answer:

> Do these real components work together correctly?

Examples include collaboration between:

* service and repository;
* repository and database;
* plugin registry and plugin descriptor;
* runtime and capability provider;
* configuration loader and configuration source;
* event publisher and event infrastructure.

---

# Integration Boundary

Conceptually:

```text
Component A
     │
     ▼
Component B
     │
     ▼
Real Integration Boundary
```

The interaction being validated must remain real.

---

# Integration Test Characteristics

Integration tests are typically:

* broader than unit tests;
* slower than unit tests;
* dependent on more infrastructure;
* more expensive to diagnose;
* more representative of real collaboration.

They should still be deterministic where possible.

---

# Integration Test Infrastructure

Integration testing may require:

* temporary databases;
* real serializers;
* filesystem adapters;
* service containers;
* plugin registries;
* runtime services;
* message infrastructure.

Infrastructure should remain controlled and reproducible.

---

# Integration Test Isolation

Integration tests should avoid unintended shared state.

Possible strategies include:

* transaction rollback;
* disposable databases;
* isolated schemas;
* temporary directories;
* unique resource identifiers.

Parallel execution should remain safe where supported.

---

# Integration Test Examples

Examples include:

* saving and retrieving an entity through a real repository adapter;
* loading plugin metadata through the actual manifest loader;
* resolving capabilities through the runtime registry;
* loading configuration through actual providers;
* persisting and retrieving versioned records.

---

# Integration Test Anti-Patterns

An integration test should not mock away every interaction it claims to validate.

For example:

```text
Repository
   mocked
Database
   mocked
Configuration
   mocked
```

does not provide meaningful repository integration evidence.

---

# Integration Testing Success Criteria

Integration testing is effective when:

* real boundaries are exercised;
* dependency failures are visible;
* environment setup remains reproducible;
* failures identify integration defects rather than unrelated environment noise.

---

# Contract Testing

## Definition

Contract testing validates explicit agreements across architectural boundaries.

A contract may define:

* interface shape;
* request schema;
* response schema;
* capability interface;
* plugin manifest;
* contribution interface;
* event structure;
* serialization format;
* compatibility expectations.

---

# Contract Testing Objective

Contract tests answer:

> Does this producer or consumer satisfy the contract that governs this boundary?

---

# Contract Boundary

Conceptually:

```text
Provider
   │
   ▼
Contract
   │
   ▼
Consumer
```

The contract itself is the validation subject.

---

# Provider Contract Testing

Provider tests validate that an implementation satisfies the contract it exposes.

Examples include:

* required fields;
* supported methods;
* response types;
* version behavior;
* error behavior.

---

# Consumer Contract Testing

Consumer tests validate assumptions that a consumer makes about a provider.

Consumer-driven contract testing may be used where appropriate.

The consumer must not silently rely on undocumented behavior.

---

# Plugin Contract Testing

Plugin contracts are especially important in FamilyOS.

Contract tests may validate:

* plugin metadata;
* plugin identifiers;
* capability declarations;
* contribution declarations;
* lifecycle methods;
* runtime interfaces;
* compatibility constraints.

---

# Schema Contract Testing

Schema-driven contracts may validate:

```text
Input Schema
Output Schema
Configuration Schema
Manifest Schema
Event Schema
```

Schema validation may be static or executable.

---

# Versioned Contract Testing

Contracts may evolve across versions.

Contract testing should validate:

* supported versions;
* backward compatibility;
* intentional breaking changes;
* migration requirements.

Hidden version assumptions are not acceptable.

---

# Contract Test Independence

Contract tests should avoid depending on unrelated system behavior.

Their purpose is boundary assurance.

Functional behavior beyond the contract belongs to other testing levels.

---

# Contract Testing Success Criteria

Contract testing is effective when:

* boundary expectations are explicit;
* producer and consumer assumptions align;
* incompatible changes are detected early;
* plugin compatibility can be validated predictably.

---

# Functional Testing

## Definition

Functional testing validates a complete capability from an externally meaningful perspective.

The test focuses on what the system does.

It does not primarily focus on how internal components collaborate.

---

# Functional Testing Objective

Functional tests answer:

> Does this capability produce the expected behavior for a meaningful scenario?

---

# Functional Boundary

Conceptually:

```text
Functional Request
       │
       ▼
Application Capability
       │
       ▼
Observable Functional Result
```

---

# Functional Test Scope

Functional tests may cross:

* application services;
* repositories;
* domain logic;
* plugin capabilities;
* configuration;
* runtime services.

They should remain focused on one coherent capability.

---

# Functional Test Examples

Examples include:

* creating a domain object through an application service;
* executing a CLI capability;
* invoking a plugin capability end-to-end within application boundaries;
* processing a valid workflow;
* validating business-visible error behavior.

---

# Functional Testing Perspective

Functional testing should prioritize externally meaningful behavior.

It should avoid overasserting internal implementation details.

---

# Functional Test Infrastructure

Functional tests may require broader infrastructure than integration tests.

However, infrastructure should remain minimal relative to the capability being validated.

---

# Functional Testing Success Criteria

Functional testing is effective when:

* capability behavior is validated;
* business-visible outcomes are clear;
* failures identify capability-level defects;
* tests remain understandable and reproducible.

---

# System Testing

## Definition

System testing validates the assembled FamilyOS system or a production-like system boundary.

It provides the broadest behavioral confidence among the primary testing levels.

---

# System Testing Objective

System tests answer:

> Does the assembled system operate correctly under representative conditions?

---

# System Boundary

Conceptually:

```text
User / External Actor
         │
         ▼
        CLI
         │
         ▼
Application
         │
         ▼
Runtime
         │
   ┌─────┼─────┐
   ▼     ▼     ▼
Plugins Data Integrations
         │
         ▼
Observable System Result
```

---

# System Test Scope

System testing may include:

* application startup;
* runtime initialization;
* plugin loading;
* configuration resolution;
* persistence;
* real service collaboration;
* representative end-to-end workflows.

---

# System Test Characteristics

System tests are generally:

* slower;
* more infrastructure-heavy;
* broader in scope;
* more expensive to diagnose;
* closer to production behavior.

They should therefore be used intentionally.

---

# System Test Environment

System testing may require a production-like environment.

This does not necessarily mean production.

The environment should reproduce relevant behavior while remaining controlled.

---

# System Test Examples

Examples include:

* starting FamilyOS and executing a complete CLI workflow;
* loading official plugins and resolving capabilities;
* validating a release candidate workflow;
* validating system startup with supported configuration;
* verifying persistence across an assembled runtime.

---

# System Testing Success Criteria

System testing is effective when:

* assembled behavior is validated;
* lifecycle-critical flows are covered;
* production-like integration defects are detectable;
* failures remain diagnosable.

---

# Testing Level Comparison

The canonical comparison is:

| Level       | Primary Focus       | Scope            | Speed       | Isolation | Real Dependencies          |
| ----------- | ------------------- | ---------------- | ----------- | --------- | -------------------------- |
| Unit        | Local behavior      | Small            | Highest     | Highest   | Minimal                    |
| Integration | Collaboration       | Medium           | High/Medium | Medium    | Relevant real integrations |
| Contract    | Boundary agreement  | Boundary-focused | High/Medium | High      | Contract-dependent         |
| Functional  | Capability behavior | Broad            | Medium      | Lower     | Multiple real components   |
| System      | Assembled behavior  | Largest          | Lowest      | Lowest    | Production-like            |

These characteristics are directional rather than absolute.

---

# Testing Level Selection

The correct level should be selected based on the behavior being validated.

The following decision flow may be used:

```text
Can isolated behavior prove the requirement?
        │
      YES
        │
        ▼
      Unit
        │
       NO
        ▼
Does real component collaboration need validation?
        │
      YES
        │
        ▼
   Integration
        │
       NO
        ▼
Is the primary concern a boundary contract?
        │
      YES
        │
        ▼
    Contract
        │
       NO
        ▼
Is the concern a complete capability?
        │
      YES
        │
        ▼
   Functional
        │
       NO
        ▼
Is assembled-system behavior required?
        │
      YES
        │
        ▼
     System
```

---

# Avoid Duplicate Assurance

The same behavior should not be redundantly tested at every level without a reason.

For example, a simple validation rule may be fully covered by unit tests.

Repeating the exact same assertion through integration, functional, and system tests may add cost without additional confidence.

Higher-level tests should validate additional behavior.

---

# Complementary Assurance

Different levels should complement each other.

Example:

```text
Unit
  validates calculation logic

Integration
  validates persistence interaction

Contract
  validates public interface

Functional
  validates complete application behavior

System
  validates assembled deployment behavior
```

Together these provide layered confidence.

---

# Testing Level Ownership

Ownership follows architectural responsibility.

A component owner is normally responsible for appropriate unit and integration testing.

Cross-component contract testing may require shared ownership.

System-level testing may belong to broader platform governance.

Ownership must remain explicit.

---

# Testing Levels And Risk

Risk influences required depth.

Higher-risk behavior may require evidence at multiple levels.

Examples include:

* security boundaries;
* data persistence;
* migrations;
* plugin compatibility;
* release-critical operations.

Risk-based testing should strengthen confidence without creating indiscriminate duplication.

---

# Critical Path Testing

Critical paths should normally include strong low-level tests plus selected higher-level validation.

Conceptually:

```text
Unit Evidence
    +
Integration Evidence
    +
Contract Evidence
    +
Functional/System Evidence
        │
        ▼
Stronger Confidence
```

The exact combination depends on risk and lifecycle policy.

---

# Regression Testing Across Levels

Regression is not a separate execution layer.

A regression test may exist at any testing level.

The correct level is the lowest level that reproduces the defect reliably.

Examples:

```text
Unit Regression
Integration Regression
Contract Regression
Functional Regression
System Regression
```

---

# Security Testing Across Levels

Security testing may also occur across multiple levels.

Examples:

* unit tests for validation rules;
* integration tests for authorization adapters;
* contract tests for security-sensitive APIs;
* functional tests for access-control behavior;
* system tests for complete security workflows.

Security testing objectives do not replace level semantics.

---

# Performance Testing Across Levels

Performance testing may target:

* local algorithm performance;
* component interaction;
* service throughput;
* complete system performance.

The testing level should still describe the scope of the behavior being measured.

---

# Compatibility Testing Across Levels

Compatibility may be validated at:

* unit level for version parsing;
* contract level for interface compatibility;
* integration level for runtime compatibility;
* system level for complete supported-version behavior.

---

# Migration Testing Across Levels

Migration validation often requires integration or system testing.

However, individual migration transformation logic may also have unit tests.

The level depends on the migration behavior being validated.

---

# Test Level Naming

Testing-level names must remain semantically stable.

Teams must not redefine terms locally.

For example:

```text
Integration Test
```

must not mean:

```text
Unit test with many mocks
```

Stable terminology is required for reliable reporting and governance.

---

# Test Level Metadata

Executable tests may eventually expose metadata describing their level.

Conceptually:

```text
level: unit
level: integration
level: contract
level: functional
level: system
```

Implementation details belong to tooling specifications.

The metadata must reflect actual semantics.

---

# Mixed-Level Tests

A test that spans multiple concerns should be classified by its dominant validation boundary.

If classification is unclear, the test may be too broad.

Mixed-level ambiguity should trigger design review.

---

# Test Suite Organization

Test suites should reflect testing levels where practical.

A conceptual structure is:

```text
tests/
├── unit/
├── integration/
├── contract/
├── functional/
└── system/
```

Repository-specific variations are acceptable.

Semantic clarity remains mandatory.

---

# Unit Suite Expectations

The unit suite should generally be:

* the fastest suite;
* executable frequently;
* highly deterministic;
* suitable for local development;
* suitable for parallel execution.

---

# Integration Suite Expectations

The integration suite should:

* validate real component boundaries;
* use controlled infrastructure;
* remain reproducible;
* expose setup failures clearly.

---

# Contract Suite Expectations

The contract suite should:

* validate stable contracts;
* expose compatibility failures clearly;
* support version-aware testing;
* remain independent of unrelated functionality.

---

# Functional Suite Expectations

The functional suite should:

* represent meaningful capabilities;
* avoid unnecessary system-wide scope;
* provide clear scenario-based diagnostics.

---

# System Suite Expectations

The system suite should:

* validate representative assembled behavior;
* remain limited to high-value flows;
* avoid becoming the primary source of all confidence;
* provide production-like assurance where required.

---

# Local Execution Expectations

Developers should normally run:

```text
Unit
```

frequently.

Depending on the change, local execution may also include:

```text
Integration
Contract
Functional
```

System tests may require heavier environments.

---

# Pull Request Expectations

Pull request validation may require:

```text
Unit
Integration
Contract
```

plus targeted functional tests.

Exact policy belongs to the testing profile and lifecycle gate.

---

# Release Expectations

Release validation may require broader evidence.

Possible required levels include:

```text
Unit
Integration
Contract
Functional
System
```

depending on the release profile.

---

# Plugin Testing Levels

Plugin testing follows the same model.

A plugin may have:

```text
Plugin Unit Tests
Plugin Integration Tests
Plugin Contract Tests
Plugin Functional Tests
Plugin System Tests
```

Official plugin policy may require a subset or all of these.

---

# Plugin Unit Tests

Plugin unit tests validate:

* local policies;
* rules;
* models;
* recipes;
* transformations;
* capability-local behavior.

---

# Plugin Integration Tests

Plugin integration tests validate:

* plugin registration;
* capability resolution;
* contribution resolution;
* runtime interaction;
* persistence interaction.

---

# Plugin Contract Tests

Plugin contract tests validate:

* manifests;
* metadata;
* capability interfaces;
* contribution contracts;
* SDK compatibility.

---

# Plugin Functional Tests

Plugin functional tests validate meaningful plugin capabilities.

Examples include executing an official plugin use case through application-level interfaces.

---

# Plugin System Tests

Plugin system tests validate the plugin inside the assembled FamilyOS runtime.

These tests should be reserved for behavior that cannot be proven at lower levels.

---

# Testing Level Evidence

Testing evidence must identify its level.

Example:

```text
Test Result
├── Test ID
├── Level
├── Outcome
├── Source Revision
└── Execution Context
```

Without level information, downstream interpretation may become ambiguous.

---

# Quality Consumption

The Quality Framework may evaluate testing evidence by level.

For example, quality policy may require stronger evidence for critical components.

Quality consumes test levels.

It does not redefine them.

---

# Compliance Consumption

The Plugin Compliance Framework may require specific test levels.

Example:

```text
Official Plugin Profile
        │
        ├── Unit required
        ├── Integration required
        └── Contract required
```

Compliance determines whether the required evidence exists.

Testing defines what those levels mean.

---

# Build Consumption

The Build Framework may require particular testing levels before artifact production.

Build policy must reference canonical testing semantics.

---

# Release Consumption

The Release Framework may require broader testing evidence before release.

Release gates must not invent alternative meanings for testing levels.

---

# Certification Consumption

Certification may require stronger level coverage and trusted execution provenance.

The testing-level semantics remain unchanged.

---

# Testing Level Governance

Changes to the meaning of a testing level are framework changes.

They must be governed.

Examples include:

* redefining integration scope;
* introducing a new primary level;
* changing contract testing semantics;
* changing system testing boundaries.

---

# Introducing New Testing Levels

A new primary testing level should only be introduced when existing levels cannot express a meaningful and recurring validation boundary.

New names should not be introduced merely for organizational preference.

---

# Specialized Testing Categories

FamilyOS may define specialized categories such as:

```text
Regression
Performance
Security
Compatibility
Migration
Resilience
Chaos
Property-Based
Mutation
Fuzz
```

These describe testing purposes or techniques.

They may exist within one or more primary levels.

---

# Level And Category Separation

For example:

```text
Security Integration Test
```

has:

```text
Category: Security
Level: Integration
```

Similarly:

```text
Regression Unit Test
```

has:

```text
Category: Regression
Level: Unit
```

This separation prevents terminology confusion.

---

# Testing Level Invariants

The Testing Framework establishes the following invariants:

1. Unit tests validate isolated behavior.
2. Integration tests validate real component collaboration.
3. Contract tests validate explicit boundaries.
4. Functional tests validate complete capabilities.
5. System tests validate assembled-system behavior.
6. Testing levels must not be redefined locally.
7. Higher-level tests must not replace appropriate lower-level tests without reason.
8. Tests should run at the lowest level that can prove the behavior.
9. A regression test may exist at any primary level.
10. Specialized testing categories do not replace primary level semantics.
11. Test evidence must identify its testing level where governed consumption requires it.
12. Plugin testing uses the same canonical testing levels.
13. Quality may consume level evidence but does not define level semantics.
14. Compliance may require level evidence but does not define level semantics.
15. Build and Release may consume level evidence but do not redefine it.
16. System testing must remain selective because of its cost.
17. Unit testing must remain fast and isolated.
18. Integration testing must preserve the real boundary being validated.
19. Contract testing must protect documented agreements.
20. Functional testing must remain capability-focused.

---

# Testing Level Selection Summary

The selection rule can be summarized as:

```text
Isolated behavior
      │
      ▼
Unit

Real collaboration
      │
      ▼
Integration

Boundary agreement
      │
      ▼
Contract

Complete capability
      │
      ▼
Functional

Assembled system
      │
      ▼
System
```

---

# Final Testing Level Principle

The governing testing-level principle is:

> Use the narrowest testing boundary that can provide trustworthy evidence, and move to broader levels only when the behavior requires broader reality.

This model allows FamilyOS to preserve fast feedback, strong diagnostics, meaningful integration assurance, and system-level confidence without turning every validation problem into an expensive end-to-end test.
