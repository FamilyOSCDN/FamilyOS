# Testing Framework

# 07 Integration Testing

## Overview

Integration testing validates that multiple FamilyOS components collaborate correctly across defined architectural boundaries.

While unit testing verifies isolated units of behavior, integration testing verifies the contracts, interactions, data flows, and lifecycle relationships that emerge when components are assembled.

Within FamilyOS, integration testing is a critical engineering capability because the platform is composed of multiple cooperating architectural elements, including:

* domain components;
* application services;
* repositories;
* adapters;
* plugins;
* capabilities;
* runtime services;
* configuration systems;
* event infrastructure;
* persistence mechanisms;
* external integrations.

Integration tests ensure that these components remain compatible as the platform evolves.

The objective is not merely to verify that components can communicate, but to verify that they communicate according to the architectural contracts defined by FamilyOS.

---

# Purpose

The purpose of integration testing is to validate interactions between components that have already been tested independently.

Integration testing provides confidence that:

* components collaborate correctly;
* architectural boundaries are respected;
* contracts between modules remain valid;
* data moves correctly across layers;
* adapters correctly implement their ports;
* repositories correctly interact with persistence mechanisms;
* plugins integrate correctly with the platform;
* capabilities are correctly registered and resolved;
* configuration is propagated correctly;
* events are produced and consumed correctly;
* infrastructure components behave correctly when assembled.

Integration testing therefore acts as the verification layer between isolated unit correctness and complete system behavior.

---

# Integration Testing Principles

FamilyOS integration testing follows several fundamental principles.

## Test Real Interactions

Integration tests should exercise meaningful interactions between real components whenever practical.

Excessive mocking can transform an integration test into a disguised unit test.

Mocks should therefore be used only at boundaries that are intentionally excluded from the integration scope.

---

## Validate Architectural Contracts

Integration tests must verify the contracts defined between architectural components.

Examples include:

* application service to repository contracts;
* domain service to infrastructure adapter contracts;
* plugin to runtime contracts;
* capability registration contracts;
* event publisher to event consumer contracts;
* configuration provider to application contracts.

A successful interaction that violates an architectural contract is not considered a valid integration.

---

## Keep Integration Scope Explicit

Every integration test must have a clearly defined integration boundary.

The test should identify:

* which components participate;
* which dependencies are real;
* which dependencies are substituted;
* which infrastructure is required;
* which contracts are being validated.

Uncontrolled integration scope creates tests that are difficult to understand, diagnose, and maintain.

---

## Prefer Deterministic Environments

Integration tests must produce reproducible results.

They should avoid uncontrolled dependencies on:

* external networks;
* public APIs;
* shared databases;
* local developer configuration;
* machine-specific state;
* execution order;
* current time;
* random external data.

Required infrastructure should be isolated and controlled whenever possible.

---

## Preserve Failure Locality

Integration tests should remain narrow enough that failures can be diagnosed efficiently.

A failing integration test should provide clear evidence about which interaction or contract has failed.

Tests that exercise the entire platform without clear boundaries belong to higher testing levels.

---

# Integration Testing Scope

Integration testing covers interactions between two or more architectural components.

Typical FamilyOS integration targets include:

```text
Application Service
        │
        ▼
Repository Port
        │
        ▼
Repository Adapter
        │
        ▼
Persistence
```

Other examples include:

```text
Plugin
  │
  ▼
Capability Registry
  │
  ▼
Runtime
```

and:

```text
Domain Event
     │
     ▼
Event Publisher
     │
     ▼
Event Bus
     │
     ▼
Event Consumer
```

The exact integration boundary depends on the behavior under test.

---

# Layer Integration

FamilyOS follows architectural separation between domain, application, infrastructure, runtime, presentation, and plugin concerns.

Integration tests must verify that these layers collaborate correctly without weakening their boundaries.

## Domain and Application Integration

Tests may verify that application services correctly orchestrate domain behavior.

Typical concerns include:

* command handling;
* use-case execution;
* domain object creation;
* domain validation;
* domain event production;
* repository interaction.

The domain itself should remain independent from infrastructure concerns.

---

## Application and Infrastructure Integration

Application components frequently depend on ports implemented by infrastructure adapters.

Integration tests should verify that those adapters satisfy the expected contracts.

Examples include:

* repository implementations;
* file storage adapters;
* configuration providers;
* event publishers;
* notification adapters;
* serialization adapters.

The test should focus on compatibility between the application-facing contract and its concrete implementation.

---

## Runtime Integration

Runtime integration tests verify that runtime components correctly assemble and execute platform capabilities.

These tests may validate:

* service registration;
* dependency resolution;
* lifecycle hooks;
* plugin discovery;
* capability registration;
* runtime initialization;
* runtime shutdown;
* configuration loading.

Runtime integration is particularly important because many FamilyOS components are dynamically assembled.

---

# Repository Integration Testing

Repository integration tests validate concrete repository implementations against their defined interfaces and expected semantics.

They should verify behaviors such as:

* entity persistence;
* entity retrieval;
* updates;
* deletion;
* query behavior;
* transaction behavior;
* identity preservation;
* serialization;
* error handling.

A repository integration test should not merely prove that a database operation succeeds.

It should prove that the repository implementation behaves according to the domain and application contract.

---

# Persistence Integration

Persistence integration testing validates interactions with actual persistence technologies or controlled equivalents.

Depending on the implementation, this may include:

* relational databases;
* document stores;
* local files;
* structured configuration stores;
* caches;
* embedded databases.

Tests must ensure isolation between executions.

Persistent state should be created specifically for the test and removed or reset afterward.

Shared mutable test databases should be avoided whenever possible.

---

# Plugin Integration Testing

Plugins are a major architectural extension mechanism in FamilyOS.

Integration testing must verify that plugins correctly interact with the platform.

Typical plugin integration scenarios include:

* plugin discovery;
* plugin metadata loading;
* plugin validation;
* plugin registration;
* capability exposure;
* contribution registration;
* runtime activation;
* dependency resolution;
* plugin lifecycle execution;
* plugin shutdown.

For official plugins, integration tests should additionally verify compliance with platform contracts and plugin certification requirements.

---

# Capability Integration Testing

Capabilities expose platform functionality through explicit contracts.

Integration tests should verify:

* capability registration;
* capability discovery;
* capability resolution;
* invocation;
* input validation;
* output compatibility;
* error propagation;
* lifecycle behavior.

Capability integration tests are especially important when implementations are provided dynamically by plugins.

---

# Contribution Integration Testing

FamilyOS plugins may contribute platform artifacts such as:

* policies;
* rules;
* recipes;
* templates;
* commands;
* services;
* capabilities.

Integration tests should verify that these contributions are:

1. discovered;
2. validated;
3. registered;
4. accessible;
5. executable when applicable.

Tests should also verify rejection of malformed or incompatible contributions.

---

# Configuration Integration Testing

Configuration often crosses multiple architectural layers.

Integration tests should verify that configuration:

* loads from supported sources;
* follows precedence rules;
* is validated;
* reaches the intended components;
* supports defaults;
* rejects invalid values;
* produces predictable errors.

Configuration tests must not depend on uncontrolled developer-machine configuration.

Temporary or explicitly constructed configuration sources should be preferred.

---

# Event Integration Testing

Event-driven interactions require dedicated integration validation.

Tests should verify:

* event creation;
* event publication;
* event routing;
* event consumption;
* payload compatibility;
* handler execution;
* failure behavior;
* ordering assumptions where defined.

Event integration tests should avoid arbitrary sleeps or timing assumptions.

Where asynchronous behavior exists, deterministic synchronization mechanisms should be used.

---

# CLI Integration Testing

CLI integration tests validate interactions between command-line entry points and underlying application or runtime components.

They may verify:

* command registration;
* argument parsing;
* option propagation;
* application service invocation;
* exit codes;
* output formatting;
* error reporting.

CLI integration tests should focus on the integration boundary rather than duplicating complete end-to-end scenarios.

---

# External Service Integration

Some FamilyOS components may integrate with external services.

Direct use of live external services in the normal integration test suite should be avoided unless explicitly required.

Reasons include:

* network instability;
* service availability;
* rate limits;
* authentication complexity;
* cost;
* unpredictable data;
* third-party changes.

Preferred approaches include:

* local service implementations;
* protocol-compatible test services;
* controlled sandbox environments;
* deterministic fake servers;
* contract fixtures.

Live external integration tests should be explicitly classified and isolated from the default test suite.

---

# Integration Test Doubles

Test doubles remain useful in integration testing, but their use must preserve the interaction being tested.

Possible doubles include:

* fakes;
* stubs;
* controlled adapters;
* fake external services;
* deterministic clocks;
* test configuration providers.

A dependency should not be mocked when that dependency is part of the integration contract under test.

For example, when testing a repository implementation, mocking the repository itself would invalidate the purpose of the test.

---

# Integration Fixtures

Integration fixtures establish controlled environments for component interaction.

Fixtures may provide:

* temporary directories;
* isolated databases;
* configured runtimes;
* plugin registries;
* capability registries;
* repository implementations;
* event buses;
* test configuration;
* seeded data.

Fixtures should be:

* deterministic;
* minimal;
* reusable where appropriate;
* isolated between tests;
* automatically cleaned up.

Fixture design is further defined by the FamilyOS test data and fixture strategy.

---

# Test Isolation

Integration tests must remain isolated from one another.

A test must not depend on state created by another test.

Isolation mechanisms may include:

* temporary directories;
* isolated database instances;
* transaction rollback;
* unique identifiers;
* independent runtime instances;
* fixture-level cleanup.

Tests should be executable:

* individually;
* in arbitrary order;
* repeatedly;
* in parallel when supported.

---

# Integration Test Structure

Integration tests should follow the same behavioral clarity expected from unit tests.

A typical structure is:

```python
def test_repository_persists_and_restores_entity(repository):
    entity = create_test_entity()

    repository.save(entity)

    restored = repository.get(entity.id)

    assert restored == entity
```

The test should make the integration contract visible.

Implementation details unrelated to the contract should remain hidden behind fixtures or helpers.

---

# Directory Organization

Integration tests should be clearly separated from unit and higher-level tests.

A typical FamilyOS structure is:

```text
tests/
├── unit/
├── integration/
├── functional/
├── system/
├── contract/
└── regression/
```

Integration tests may mirror the source architecture:

```text
tests/integration/
├── application/
├── repositories/
├── persistence/
├── runtime/
├── plugins/
├── capabilities/
├── configuration/
├── events/
└── cli/
```

The exact structure may evolve with the platform, but test classification must remain explicit.

---

# Naming Conventions

Integration test names should describe the interaction and expected result.

Preferred patterns include:

```text
test_<component>_<interaction>_<expected_result>
```

Examples:

```text
test_repository_save_makes_entity_retrievable
test_plugin_registration_exposes_capability
test_event_publication_invokes_registered_handler
test_runtime_startup_registers_builtin_plugins
test_configuration_provider_applies_environment_override
```

Names should communicate the integration contract rather than internal implementation mechanics.

---

# Markers and Classification

Integration tests should be identifiable through directory structure, test metadata, or test markers.

For example:

```python
@pytest.mark.integration
def test_plugin_registration_exposes_capability():
    ...
```

Classification allows the engineering workflow to execute different testing levels independently.

Typical execution strategies may include:

```bash
pytest tests/integration
```

or:

```bash
pytest -m integration
```

The exact commands are governed by the FamilyOS testing toolchain configuration.

---

# Execution Strategy

Integration tests are generally more expensive than unit tests.

They should therefore be executed strategically.

Recommended execution points include:

* local development when affected integrations change;
* pre-commit or pre-push workflows where practical;
* pull request validation;
* continuous integration pipelines;
* release validation;
* plugin certification.

Critical integration tests may be included in mandatory quality gates.

---

# Performance Expectations

Integration tests should remain efficient enough to provide useful engineering feedback.

Slow tests should be investigated for:

* unnecessary infrastructure startup;
* excessive fixture creation;
* uncontrolled I/O;
* external dependencies;
* redundant initialization;
* oversized test datasets.

Performance optimization must not compromise test realism or architectural validity.

---

# Failure Diagnostics

Integration test failures should provide enough information to identify the failing boundary.

Useful diagnostics may include:

* participating components;
* expected contract behavior;
* actual result;
* relevant configuration;
* generated identifiers;
* adapter errors;
* event traces;
* runtime lifecycle state.

Diagnostic output must never expose secrets or sensitive data.

---

# Negative Integration Testing

Integration testing must also verify failure scenarios.

Examples include:

* invalid configuration;
* unavailable adapters;
* malformed plugin metadata;
* incompatible capabilities;
* rejected contributions;
* persistence failures;
* duplicate registration;
* event handler failures;
* lifecycle initialization errors.

Negative tests ensure that architectural boundaries fail predictably and safely.

---

# Integration Test Anti-Patterns

The following patterns should be avoided.

## Mocking Every Dependency

This removes the integration behavior that the test is intended to validate.

---

## Testing the Entire Platform

An integration test should have a bounded scope.

Complete platform workflows belong to functional or system testing.

---

## Shared Mutable State

Tests that depend on shared databases, files, registries, or runtime instances create order-dependent failures.

---

## External Network Dependency

Normal integration tests should not require uncontrolled network access.

---

## Arbitrary Waiting

Using fixed sleeps to wait for asynchronous behavior creates slow and unreliable tests.

---

## Hidden Environment Dependencies

Tests must not depend on developer-specific environment variables, installed services, or filesystem state.

---

## Duplicate Unit Coverage

Integration tests should validate interactions, not repeat every isolated behavior already covered by unit tests.

---

# Integration Testing and Continuous Integration

Integration tests are a core component of the FamilyOS CI strategy.

The CI pipeline should be able to:

1. establish the required controlled environment;
2. execute integration tests;
3. capture diagnostics;
4. report failures;
5. enforce required quality gates;
6. preserve relevant test artifacts when necessary.

Integration test failures affecting mandatory architectural contracts must block promotion of the affected change.

---

# Integration Testing and Plugin Certification

Official FamilyOS plugins require stronger integration guarantees.

Certification may require validation of:

* plugin discovery;
* metadata compatibility;
* registration;
* capability exposure;
* contribution loading;
* lifecycle behavior;
* runtime compatibility;
* failure isolation.

The exact certification requirements are defined by the plugin certification architecture and applicable governance documents.

---

# Relationship With Unit Testing

Unit testing and integration testing serve complementary purposes.

Unit testing answers:

> Does this component behave correctly in isolation?

Integration testing answers:

> Do these components collaborate correctly according to their contracts?

Strong unit coverage does not eliminate the need for integration testing.

Likewise, integration testing should not replace focused unit testing.

---

# Relationship With Contract Testing

Contract testing validates the formal compatibility expectations between providers and consumers.

Integration testing validates actual collaboration between concrete components.

Contract tests may therefore detect compatibility violations without assembling all participating components, while integration tests confirm that concrete implementations function correctly together.

Both testing levels are required where architectural contracts are significant.

---

# Relationship With Functional and System Testing

Integration tests validate bounded component interactions.

Functional tests validate user-visible or business-level functionality.

System tests validate the behavior of the assembled platform.

The progression can be represented as:

```text
Unit
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

Each level increases the scope of the tested system while generally increasing execution cost.

---

# Relationship With Regression Testing

Integration tests become part of the regression suite when they protect previously validated integration behavior.

A defect involving an integration boundary should normally result in a regression test at the most appropriate testing level.

This ensures that the same integration failure cannot silently reappear.

---

# Quality Requirements

FamilyOS integration tests must be:

* deterministic;
* isolated;
* maintainable;
* architecturally meaningful;
* reproducible;
* appropriately scoped;
* diagnosable;
* secure;
* automation-friendly.

Tests that repeatedly produce nondeterministic results must be treated as engineering defects.

---

# Governance

Integration testing practices are governed by the FamilyOS Testing Framework.

Changes affecting integration testing conventions, classification, execution strategy, or mandatory quality gates must remain consistent with:

* Engineering Foundation;
* Testing Framework;
* Quality Framework;
* Plugin Architecture;
* Runtime Architecture;
* applicable ADRs;
* applicable RFCs.

Major changes to integration testing architecture should be documented through the appropriate engineering governance mechanism.

---

# Evolution Strategy

The FamilyOS integration testing strategy is expected to evolve with the platform.

Future improvements may include:

* automated infrastructure provisioning;
* ephemeral test environments;
* database containerization;
* richer plugin integration harnesses;
* capability compatibility matrices;
* event testing utilities;
* integration coverage metrics;
* distributed integration testing;
* improved CI parallelization;
* automated integration certification.

Evolution must preserve deterministic execution, architectural clarity, and developer feedback quality.

---

# Validation Checklist

An integration testing implementation is considered aligned with this framework when:

* [ ] integration boundaries are explicitly defined;
* [ ] real component interactions are tested;
* [ ] architectural contracts are validated;
* [ ] integration tests are separated from unit tests;
* [ ] tests are deterministic;
* [ ] tests are isolated;
* [ ] persistent state is controlled;
* [ ] external dependencies are controlled;
* [ ] fixtures are automatically cleaned up;
* [ ] plugin integrations are validated where applicable;
* [ ] capability integrations are validated where applicable;
* [ ] event interactions are validated where applicable;
* [ ] negative integration scenarios are covered;
* [ ] failures provide useful diagnostics;
* [ ] tests can execute independently;
* [ ] CI can execute integration tests automatically;
* [ ] mandatory integration failures block applicable quality gates.

---

# Final Principle

Integration testing protects the architectural relationships that allow FamilyOS to operate as a coherent platform.

The fundamental rule is:

> Components are not considered integrated because they can communicate; they are integrated only when they collaborate correctly through explicit, validated, and stable contracts.

By maintaining deterministic, isolated, contract-focused integration tests, FamilyOS can evolve its architecture, runtime, plugins, and infrastructure while preserving confidence that independently developed components continue to function correctly together.
