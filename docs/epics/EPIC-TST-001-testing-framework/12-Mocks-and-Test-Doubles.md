# Testing Framework

# 12 Mocks and Test Doubles

## Overview

Mocks and test doubles provide controlled substitutes for dependencies that should not participate directly in a specific FamilyOS test.

They allow tests to isolate behavior, control external conditions, reproduce difficult scenarios, and avoid unnecessary infrastructure.

However, test doubles can also create false confidence when they replace too much real behavior.

FamilyOS therefore treats mocks and test doubles as precision tools rather than default replacements for dependencies.

The objective is to use the smallest and most appropriate substitute necessary for the testing level while preserving the architectural behavior that the test is intended to validate.

---

# Purpose

The purpose of the FamilyOS mock and test-double strategy is to provide clear rules for replacing dependencies during automated testing.

This strategy helps ensure that:

* unit tests remain isolated and fast;
* external dependencies can be controlled;
* rare failure scenarios can be reproduced;
* nondeterministic behavior can be eliminated;
* architectural boundaries can be tested deliberately;
* integration behavior is not accidentally mocked away;
* tests remain understandable and maintainable.

Test doubles must support test intent rather than distort it.

---

# Test Double Definition

A test double is any controlled substitute used in place of a real dependency during testing.

The main categories used by FamilyOS are:

* dummy;
* stub;
* fake;
* spy;
* mock.

These categories describe different purposes and should not be treated as interchangeable terms.

---

# Test Double Taxonomy

The conceptual hierarchy is:

```text
Test Double
    │
    ├── Dummy
    ├── Stub
    ├── Fake
    ├── Spy
    └── Mock
```

The correct test double depends on what the test needs to control or observe.

---

# Dummy

A dummy is a value or object supplied only because an interface requires it.

The test does not interact meaningfully with the dummy.

Example:

```python
class DummyLogger:
    def info(self, message: str) -> None:
        pass
```

If the test does not care about logging behavior, a dummy logger may be sufficient.

Dummies should not accumulate hidden behavior.

---

# Stub

A stub returns predefined responses.

It is used when the test needs to control dependency output.

Example:

```python
class StubClock:
    def now(self) -> datetime:
        return datetime(2026, 8, 7, 12, 0, 0)
```

A stub is useful for controlling:

* time;
* configuration;
* external responses;
* deterministic identifiers;
* repository queries.

The test normally asserts behavior of the system under test rather than interactions with the stub.

---

# Fake

A fake is a lightweight but functional implementation of a dependency.

Examples include:

* in-memory repository;
* in-memory event bus;
* local fake capability registry;
* temporary storage adapter.

Example:

```python
class InMemoryFamilyRepository:
    def __init__(self) -> None:
        self._families: dict[FamilyId, Family] = {}

    def save(self, family: Family) -> None:
        self._families[family.id] = family

    def get(self, family_id: FamilyId) -> Family | None:
        return self._families.get(family_id)
```

Fakes are often more maintainable than large mock configurations because they model real behavior through a simplified implementation.

---

# Spy

A spy records interactions while still allowing controlled behavior.

Example:

```python
class SpyEventPublisher:
    def __init__(self) -> None:
        self.published: list[DomainEvent] = []

    def publish(self, event: DomainEvent) -> None:
        self.published.append(event)
```

A test can then assert:

```python
assert len(publisher.published) == 1
```

Spies are useful when interaction itself is part of the behavior being validated.

---

# Mock

A mock is a test double configured with explicit expectations about interactions.

Example:

```python
repository.save.assert_called_once_with(family)
```

Mocks are useful when the interaction contract is significant.

However, excessive interaction assertions create brittle tests.

Mocks should therefore be used selectively.

---

# Core Principle

The preferred rule is:

> Replace only the dependency that must be controlled, and preserve all behavior that belongs to the scope of the test.

This rule prevents test doubles from accidentally removing the behavior the test is supposed to validate.

---

# Test Double Selection

A useful selection model is:

```text
Need only placeholder?
        │
        └── Dummy

Need controlled return value?
        │
        └── Stub

Need lightweight real behavior?
        │
        └── Fake

Need interaction recording?
        │
        └── Spy

Need strict interaction expectations?
        │
        └── Mock
```

The simplest adequate test double should be preferred.

---

# Test Doubles and Unit Testing

Unit tests are the primary context for test doubles.

They may replace:

* repositories;
* clocks;
* UUID generators;
* external services;
* event publishers;
* notification gateways;
* configuration providers.

Example:

```python
def test_service_publishes_family_created_event(
    repository,
    event_publisher,
):
    service = CreateFamilyService(
        repository=repository,
        event_publisher=event_publisher,
    )

    service.execute(CreateFamilyCommand(name="Example Family"))

    assert len(event_publisher.published) == 1
```

The substituted dependencies should isolate the behavior under test.

---

# Test Doubles and Integration Testing

Integration tests should use fewer substitutes.

The dependency being integrated must remain real.

For example, when testing:

```text
Application Service
        │
        ▼
Repository Adapter
        │
        ▼
Database
```

mocking the repository adapter would eliminate the integration under test.

Substitutions should exist only outside the defined integration boundary.

---

# Test Doubles and Functional Testing

Functional tests should generally interact with real application components.

Mocks should be limited to external or intentionally excluded boundaries.

For example:

```text
CLI
 │
 ▼
Application
 │
 ▼
Domain
 │
 ▼
Repository
```

should generally remain real in a CLI functional test.

A remote third-party API may be replaced with a controlled fake server.

---

# Test Doubles and System Testing

System tests should minimize substitution of internal FamilyOS components.

The objective of system testing is to validate representative platform assembly.

Replacing runtime, plugin registry, persistence, or internal capability mechanisms with mocks can invalidate the purpose of the test.

External systems may still be replaced with controlled equivalents.

---

# Architectural Boundaries

Test doubles should usually be introduced at explicit architectural boundaries.

Good substitution points include:

* ports;
* interfaces;
* protocols;
* adapters;
* external gateways;
* clocks;
* identifier providers.

This aligns test substitution with FamilyOS Clean Architecture principles.

---

# Ports and Adapters

A typical pattern is:

```text
Application
    │
    ▼
Port
    │
    ├── Production Adapter
    │
    └── Test Double
```

The application depends on the port.

Tests can provide a controlled implementation of the same contract.

This avoids coupling application logic to testing mechanisms.

---

# Repository Test Doubles

In-memory repositories are useful test fakes.

They should preserve the important semantics of the repository contract.

For example, if a production repository rejects duplicate identifiers, the in-memory fake should not silently accept them if tests depend on that behavior.

Fake implementations should not drift from the contracts they represent.

---

# Repository Mocking

Mock repositories may be appropriate when testing orchestration behavior.

Example:

```python
repository.get.return_value = family
```

However, when repository semantics matter, a fake or real repository implementation is preferable.

Mocks should not be used to simulate complex repository behavior across many tests.

---

# Clock Test Doubles

Time is a common nondeterministic dependency.

FamilyOS should prefer injectable clocks.

Example:

```python
class FixedClock:
    def __init__(self, current: datetime) -> None:
        self._current = current

    def now(self) -> datetime:
        return self._current
```

This avoids patching global time functions throughout the test suite.

---

# Identifier Test Doubles

Random identifier generation may also be substituted.

Example:

```python
class FixedIdGenerator:
    def new_id(self) -> str:
        return "family-001"
```

This makes outputs deterministic and easier to assert.

---

# Configuration Test Doubles

Components requiring configuration should receive explicit test configuration.

A stub configuration provider may be used when configuration loading itself is outside the test scope.

When configuration integration is the subject of the test, the real provider should be used instead.

---

# Event Publisher Doubles

Event publication may use a spy or fake.

Example:

```python
class RecordingEventPublisher:
    def __init__(self) -> None:
        self.events: list[DomainEvent] = []

    def publish(self, event: DomainEvent) -> None:
        self.events.append(event)
```

This allows assertions about published events without introducing a real event bus into unit tests.

---

# Event Bus Fakes

Integration or functional tests may use an in-memory event bus if the real distributed infrastructure is outside scope.

The fake should preserve relevant behavior such as:

* handler registration;
* event routing;
* delivery semantics;
* error propagation.

It should not pretend to validate network or broker behavior that it does not implement.

---

# External Service Stubs

External services should usually be substituted in normal automated tests.

Possible approaches include:

* stub clients;
* fake servers;
* protocol simulators;
* local sandbox services.

Example controlled responses may include:

* success;
* authentication failure;
* timeout;
* rate limit;
* malformed response;
* service unavailable.

These allow deterministic testing of external interaction handling.

---

# Fake Servers

A local fake server is often preferable to mocking the HTTP client itself when protocol behavior matters.

This preserves more of the real stack:

```text
Application
    │
    ▼
HTTP Adapter
    │
    ▼
Local Fake Server
```

This can validate:

* serialization;
* headers;
* status handling;
* protocol semantics;
* retry behavior.

---

# Network Mocking

Low-level network mocking should be used cautiously.

It can become tightly coupled to implementation details.

Where possible, tests should substitute at the external service boundary rather than patching internal HTTP calls individually.

---

# Plugin Test Doubles

Plugins may require controlled substitutes for:

* capability providers;
* runtime services;
* repositories;
* external integrations.

Plugin tests should preserve the plugin contract being validated.

Mocking the plugin registration mechanism during a registration test would defeat the purpose of the test.

---

# Capability Test Doubles

A capability consumer may use a stub capability provider when testing consumer behavior.

A capability provider test should instead validate the real provider implementation.

This reflects the provider-consumer distinction.

---

# Runtime Test Doubles

Runtime internals should rarely be mocked broadly.

Instead, focused interfaces such as service registries or resource providers may be substituted in isolated tests.

Tests validating runtime assembly should use the real runtime.

---

# CLI Test Doubles

CLI unit tests may mock or fake underlying application services if parsing behavior is the only concern.

CLI functional tests should generally use real application services.

The substitution strategy must match the test level.

---

# Mocking Frameworks

Mocking libraries can reduce boilerplate.

Typical capabilities include:

* creating mocks;
* configuring return values;
* tracking calls;
* raising controlled exceptions;
* verifying interactions.

Use of a mocking framework does not remove the responsibility to choose an appropriate test-double strategy.

---

# autospec and Interface Safety

Where supported, mocks should be constrained to real interfaces.

Example:

```python
repository = create_autospec(FamilyRepository)
```

Interface-aware mocks help detect tests calling methods that do not exist on the production contract.

This reduces false confidence caused by unrestricted dynamic mocks.

---

# Strict Mocks

Strict mocks can help validate narrow interaction contracts.

However, they should not be the default.

A strict mock that requires exact call order or irrelevant method calls can make tests excessively brittle.

Strictness should correspond to an actual contract requirement.

---

# Interaction Assertions

Interaction assertions are appropriate when the interaction itself matters.

Examples include:

* event published exactly once;
* transaction committed;
* notification requested;
* repository save performed.

They should not be used for incidental implementation behavior.

---

# State vs Interaction Testing

FamilyOS should prefer state-based assertions when they provide sufficient confidence.

State-based:

```python
assert family.status == FamilyStatus.ACTIVE
```

Interaction-based:

```python
repository.save.assert_called_once()
```

The first proves a behavioral outcome.

The second proves an implementation interaction.

Interaction testing should be used when the interaction is itself part of the requirement.

---

# Overspecified Interaction Tests

This is fragile:

```python
service.validate.assert_called_once()
repository.get.assert_called_once()
mapper.convert.assert_called_once()
repository.save.assert_called_once()
event_bus.publish.assert_called_once()
```

Such tests often duplicate implementation structure rather than validate behavior.

Refactoring may break them even when observable behavior remains correct.

---

# Call Order Assertions

Call order should only be asserted when order is contractually meaningful.

Examples where order may matter:

* begin transaction before write;
* persist before publishing durable event;
* initialize before start;
* stop before resource release.

Otherwise, call order assertions should be avoided.

---

# Argument Assertions

Arguments passed to dependencies may form part of behavior.

Example:

```python
publisher.publish.assert_called_once_with(
    FamilyCreated(family_id="family-001")
)
```

Assertions should focus on meaningful values rather than internal object construction details.

---

# Exceptions From Test Doubles

Test doubles can reproduce dependency failures.

Example:

```python
repository.save.side_effect = RepositoryUnavailable()
```

This allows validation of application error handling.

Failure simulations should use realistic error categories defined by the actual dependency contract.

---

# Failure Scenario Testing

Useful scenarios include:

* timeout;
* temporary failure;
* permanent failure;
* invalid response;
* unavailable repository;
* event publication failure;
* duplicate registration;
* authorization rejection.

Test doubles make such scenarios easy to reproduce deterministically.

---

# Latency Simulation

Artificial latency should be used only when timing behavior is part of the test.

Unit tests should not sleep to simulate slow dependencies.

Instead, explicit timeout behavior should be modeled through controlled interfaces.

---

# Retry Testing

Retry behavior should be tested without real delays.

For example, a stub dependency can return:

```text
Call 1 -> Failure
Call 2 -> Failure
Call 3 -> Success
```

The test can validate retry logic deterministically.

Injected clocks or retry schedulers should eliminate unnecessary waiting.

---

# Side Effects

Test doubles should make side effects controllable.

Potential side effects include:

* filesystem writes;
* network calls;
* notifications;
* event publication;
* process execution.

Tests should isolate or replace these effects when they are outside the intended scope.

---

# Global Patching

Patching global functions should be minimized.

Examples include patching:

* `datetime.now`;
* global environment access;
* module-level repositories;
* global registries.

Dependency injection is generally preferable.

Global patching can create:

* hidden test dependencies;
* import-order problems;
* patch leaks;
* brittle tests.

---

# Monkeypatching

`monkeypatch` may be appropriate for process-level dependencies such as:

* environment variables;
* current working directory;
* selected imported functions.

It should not replace good architecture.

If large portions of the system require repeated monkeypatching, the dependency boundaries should be reconsidered.

---

# Dependency Injection

FamilyOS architecture should make testability possible through explicit dependency injection.

Example:

```python
class CreateFamilyService:
    def __init__(
        self,
        repository: FamilyRepository,
        clock: Clock,
        event_publisher: EventPublisher,
    ) -> None:
        self._repository = repository
        self._clock = clock
        self._event_publisher = event_publisher
```

Production and test implementations can then be supplied without invasive patching.

---

# Test-Specific Production Hooks

Production code should not contain special branches solely for tests.

Avoid patterns such as:

```python
if TEST_MODE:
    ...
```

Testability should come from architecture, interfaces, and dependency injection.

---

# Fake Implementation Quality

Fakes are production-like code used for testing and must remain reliable.

They should be:

* simple;
* typed;
* contract-compliant;
* deterministic;
* easy to inspect.

Complex fakes should receive their own focused tests where necessary.

---

# Contract Tests for Fakes

When a fake and production adapter implement the same port, both may execute the same contract suite.

For example:

```text
Repository Contract
       │
       ├── In-Memory Fake
       └── SQLite Adapter
```

This reduces semantic drift between test and production behavior.

---

# Do Not Mock What You Own Blindly

Internal FamilyOS components should not automatically be mocked merely because they can be.

If two internal components are simple and cheap to assemble, using them together may produce clearer and more reliable tests.

Mocking should solve a testing problem, not become a habit.

---

# Do Not Mock Value Objects

Simple domain value objects should generally be real.

Examples include:

* identifiers;
* money values;
* dates;
* names;
* statuses.

Mocking simple domain values reduces realism without meaningful isolation benefit.

---

# Do Not Mock Pure Functions

Pure functions are deterministic by nature.

They should normally be called directly.

Mocking them tends to test implementation wiring rather than behavior.

---

# Avoid Mock Chains

Deep chained mocks are a strong warning sign.

For example:

```python
client.session.api.user.get.return_value.name = "Alice"
```

This tightly couples the test to internal call structure.

A focused fake or explicit adapter stub is usually clearer.

---

# Mock Leakage

Mocks must not leak between tests.

Shared mutable mock state can cause:

* order-dependent failures;
* unexpected call counts;
* stale return values.

Mocks and spies should generally be created fresh for each test.

---

# Resetting Mocks

Resetting shared mocks can hide poor fixture design.

Creating fresh mocks per test is usually safer than maintaining long-lived mocks with repeated resets.

---

# Async Test Doubles

Asynchronous dependencies require async-compatible test doubles.

Example:

```python
async def send(self, message: Message) -> DeliveryResult:
    return DeliveryResult.success()
```

Tests should preserve async contracts rather than replacing them with incompatible synchronous substitutes.

---

# Async Mocking

Async mocks may validate awaited interactions.

Assertions may include:

```python
sender.send.assert_awaited_once_with(message)
```

As with synchronous mocks, these assertions should only represent meaningful behavior.

---

# Generator and Stream Doubles

Stream-based interfaces may require controlled iterators or async generators.

Test doubles should model:

* item delivery;
* completion;
* failure;
* empty streams.

They should avoid arbitrary timing unless timing is part of the contract.

---

# Context Manager Doubles

Dependencies implementing context-manager contracts should be substituted with context-manager-compatible doubles.

The fake should preserve lifecycle semantics such as acquire and release.

---

# Transaction Test Doubles

Transactions may be represented with spies or fakes when testing orchestration.

Important behaviors may include:

* commit;
* rollback;
* atomic boundaries.

When database transaction behavior itself is being validated, a real transactional environment is required.

---

# Security-Sensitive Doubles

Security-related test doubles require particular care.

Mocks should not accidentally bypass important authorization or validation behavior in tests claiming to validate security.

Security tests should keep real security logic inside the test scope.

---

# Authentication Doubles

A stub identity provider may be appropriate when testing downstream application behavior.

Tests validating authentication itself must use the real authentication implementation or representative protocol integration.

---

# Authorization Doubles

Authorization should not be mocked in tests asserting that protected behavior is correctly enforced.

In those scenarios, real authorization policies belong inside the test boundary.

---

# Test Double Location

Reusable test doubles may reside in dedicated test support packages.

Example:

```text
tests/
├── support/
│   ├── fakes/
│   ├── spies/
│   ├── stubs/
│   └── factories/
├── unit/
├── integration/
└── functional/
```

Test doubles specific to a single test module should remain local when practical.

---

# Naming Conventions

Names should identify the double type and contract.

Examples:

```text
FakeFamilyRepository
StubClock
SpyEventPublisher
DummyLogger
FakeCapabilityRegistry
StubNotificationGateway
```

Clear naming makes substitution explicit.

---

# Generic Mock Variables

Generic names such as:

```text
mock1
service_mock
obj
fake
```

should be avoided when they obscure the dependency role.

Prefer:

```text
repository
event_publisher
notification_gateway
```

or explicit class names when reusable implementations exist.

---

# Test Double Factories

Factories may simplify creation of configurable doubles.

They should not introduce excessive abstraction.

For example:

```python
gateway = NotificationGatewayStub.success()
```

and:

```python
gateway = NotificationGatewayStub.failure(
    NotificationUnavailable()
)
```

can improve readability when such scenarios recur frequently.

---

# Mock Configuration Duplication

Repeated complex mock setup indicates that a reusable fake or test helper may be more appropriate.

For example, repeated blocks of ten mock return-value assignments should trigger consideration of a focused fake implementation.

---

# Test Readability

A test using doubles should make three things clear:

1. what dependency is substituted;
2. what behavior it provides;
3. what outcome is expected.

Example:

```python
repository = FakeFamilyRepository()
publisher = SpyEventPublisher()

service = CreateFamilyService(
    repository=repository,
    event_publisher=publisher,
)

family = service.create("Example Family")

assert repository.get(family.id) == family
assert len(publisher.published) == 1
```

The intent remains visible.

---

# Test Double Anti-Patterns

The following practices should be avoided.

## Mock Everything

If every collaborator is mocked, the test may verify only its own mock configuration.

---

## Mock the Subject Under Test

The component whose behavior is being validated must not be replaced by a mock.

---

## Mock Internal Details

Private helper methods should normally not be mocked.

---

## Mock Across the Integration Boundary

An integration test should not substitute the component it intends to integrate.

---

## Deep Mock Chains

They create fragile coupling to implementation structure.

---

## Excessive Call Assertions

Not every method invocation is part of the contract.

---

## Reimplementing Production Logic in Stubs

A stub should not duplicate complex production behavior.

---

## Unrealistic Fakes

A fake that violates the real contract can create false confidence.

---

## Persistent Shared Mocks

Mock state must remain isolated.

---

## Global Patch Dependence

Large-scale patching often signals missing dependency boundaries.

---

# Relationship With Test Data and Fixtures

Fixtures may provide test doubles.

For example:

```python
@pytest.fixture
def repository():
    return FakeFamilyRepository()
```

Fixture design should not hide whether a dependency is real or substituted when that distinction matters.

---

# Relationship With Unit Testing

Unit tests make the greatest use of test doubles.

They should prefer:

* simple fakes;
* deterministic stubs;
* focused spies;
* mocks only when interaction verification is meaningful.

---

# Relationship With Integration Testing

Integration tests should preserve real behavior inside their declared integration boundary.

Substitutions belong outside that boundary.

---

# Relationship With Functional Testing

Functional tests should use real internal application components and substitute only intentionally excluded dependencies.

---

# Relationship With System Testing

System tests should minimize internal substitution.

External production services may be replaced with representative controlled environments.

---

# Relationship With Contract Testing

Test doubles implementing formal ports should satisfy the same contracts as production implementations where practical.

Contract testing can validate fake correctness.

---

# Relationship With Regression Testing

Mocks and fakes can help reproduce historical failures deterministically.

However, the regression test must still represent the real failure condition closely enough to provide durable protection.

---

# Relationship With Architecture

Heavy mocking often reveals architectural coupling.

If a component requires extensive patching to test, FamilyOS should evaluate whether responsibilities or dependencies are poorly separated.

Testing difficulty can therefore act as an architecture quality signal.

---

# Quality Requirements

FamilyOS test doubles must be:

* explicit;
* deterministic;
* appropriately scoped;
* contract-aware;
* easy to understand;
* isolated;
* maintainable.

They must not create artificial confidence by replacing the behavior being validated.

---

# Review Requirements

Code review should examine test-double usage for:

* unnecessary mocking;
* overspecified interactions;
* invalid fake semantics;
* hidden dependencies;
* excessive global patching;
* duplicated mock configuration;
* incorrect test-level boundaries.

Tests should be reviewed for behavioral value, not merely execution success.

---

# Quality Gates

Test-double misuse may indirectly affect quality gates when it creates insufficient validation.

Critical areas should not rely solely on mocked verification when representative integration or functional validation is required.

Plugin certification, release validation, and security-sensitive workflows may require real implementations at defined boundaries.

---

# Governance

Mocks and test-double practices are governed by the FamilyOS Testing Framework and architectural principles.

Relevant sources include:

* Engineering Foundation;
* Testing Framework;
* Quality Framework;
* Application Architecture;
* Plugin Architecture;
* Runtime Architecture;
* applicable ADRs;
* applicable RFCs.

Testability should result from sound architecture rather than production-code exceptions for tests.

---

# Evolution Strategy

FamilyOS test-double infrastructure may evolve as the platform matures.

Future improvements may include:

* shared fake repositories;
* reusable event spies;
* standardized fixed clocks;
* deterministic identifier providers;
* official capability test doubles;
* external service simulators;
* runtime test harnesses;
* contract verification for fakes;
* stricter mock linting;
* automated detection of unused or overspecified mocks.

Evolution should reduce duplication while preserving test clarity and architectural accuracy.

---

# Validation Checklist

A FamilyOS test-double strategy is aligned with this framework when:

* [ ] the simplest adequate test double is used;
* [ ] test-double type and purpose are clear;
* [ ] unit tests remain isolated where appropriate;
* [ ] integration boundaries are not mocked away;
* [ ] functional tests retain real internal behavior;
* [ ] system tests minimize internal substitution;
* [ ] fakes respect applicable production contracts;
* [ ] deterministic clocks are used for time-sensitive tests;
* [ ] external services can be controlled safely;
* [ ] interaction assertions represent meaningful requirements;
* [ ] implementation details are not overspecified;
* [ ] deep mock chains are avoided;
* [ ] global patching is minimized;
* [ ] dependency injection enables substitution;
* [ ] production code contains no unnecessary test-only branches;
* [ ] test doubles remain isolated between tests;
* [ ] reusable fakes are appropriately maintained;
* [ ] security behavior is not mocked away in security validation;
* [ ] test doubles remain understandable during review;
* [ ] mocks do not replace the subject under test;
* [ ] test-double usage matches the declared testing level.

---

# Final Principle

Mocks and test doubles exist to control test boundaries, not to manufacture passing tests.

The fundamental rule is:

> Substitute only what must be controlled, and never substitute away the behavior that gives the test its meaning.

By applying test doubles deliberately and aligning them with architectural boundaries, FamilyOS can preserve fast unit testing, deterministic failure simulation, realistic integration validation, and trustworthy evidence across the complete testing strategy.
