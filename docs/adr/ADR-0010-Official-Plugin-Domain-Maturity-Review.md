# ADR-0010 — Official Plugin Domain Maturity Review

## Status

Accepted

## Date

2026-08-03

## Context

FamilyOS Phase 2 introduces official domain plugins.

The first official plugins:

- RFC-0010 — Security Plugin
- RFC-0011 — Health Plugin

have established the initial architecture for domain extensions.

Before introducing additional official domains such as Finance, Education, Documents, and Communication, the platform requires a maturity review to ensure that plugin architecture rules are stable and reusable.

The goal is to transform implementation experience into explicit architectural constraints.

---

# Decision

FamilyOS official plugins must follow a standardized domain plugin architecture.

Every official plugin must provide:

1. Plugin metadata
2. Capabilities
3. Domain models
4. Validation layer
5. Generation recipes
6. Contributions
7. Runtime integration
8. Automated tests

---

# Official Plugin Structure

An official plugin follows a common structural foundation.

The mandatory structure is:

```text
plugins/builtin/<domain>/

├── capabilities/
├── validation/
├── recipes/
├── templates/
├── plugin.py
└── plugin.yaml
These elements define the minimum contract required for every official plugin:

plugin.yaml defines plugin metadata and loading information.
plugin.py provides the plugin implementation.
capabilities/ exposes domain capabilities.
validation/ contains domain validation services.
recipes/ provides generation recipes.
templates/ contains generated artifact templates.
Domain-Specific Extensions

A domain may introduce additional modules according to its own business concepts.

The following directories are optional and must only be created when required by the domain:

models/
profiles/
records/
metrics/
policies/
rules/
registries/

These modules represent domain-specific concepts without changing the official plugin contract.

Examples
Security Plugin

The Security domain extends the common structure with security-specific concepts:

security/

├── capabilities/
├── policies/
├── profiles/
├── rules/
├── validation/
├── recipes/
├── templates/
├── plugin.py
└── plugin.yaml

Security introduces policies and rules because they are core domain concepts.

Health Plugin

The Health domain extends the common structure with health-specific concepts:

health/

├── capabilities/
├── profiles/
├── records/
├── metrics/
├── validation/
├── recipes/
├── templates/
├── plugin.py
└── plugin.yaml

Health introduces profiles, records, and metrics because they represent fundamental health domain entities.

This separation establishes a stable rule:

Official Plugin Contract
        +
Domain-Specific Extensions
        =
Official FamilyOS Domain Plugin



---

# Plugin Runtime Contract

The `PluginRuntime` is the central execution boundary for official plugins.

It provides the runtime services required to load, activate, manage, and integrate plugins into the FamilyOS platform.

The runtime manages:

PluginRuntime

├── PluginRegistry
├── PluginCollection
├── CapabilityRegistry
├── ContributionRegistry
└── Lifecycle Management

---

# Plugin Activation Lifecycle

Plugin activation follows a controlled lifecycle:

Discovered

↓

Loaded

↓

Initialized

↓

Activated

↓

Registered

↓

Active

During activation, the runtime must:

1. Initialize the plugin lifecycle state.
2. Activate the plugin instance.
3. Register plugin capabilities.
4. Register plugin contributions.
5. Make the plugin available to runtime services.

The runtime is responsible for orchestration.

Plugins remain responsible for declaring their own capabilities and contributions.

---

# Capability Contract

Official plugins expose their domain capabilities through:

capabilities()

A capability represents a stable feature or service exposed by a plugin.

Capabilities must:

- have stable identifiers.
- expose descriptive metadata.
- be registered by the runtime.
- remain backward compatible once published.

Example:

familyos.health.profile

familyos.health.record

Capability identifiers are part of the plugin public contract and must not be changed without a compatibility strategy.

---

# Contribution Contract

Official plugins contribute executable platform extensions through:

contributions()

Contributions allow plugins to participate in FamilyOS workflows without modifying the core platform.

Supported contribution types include:

- GenerationContribution
- GenerationRecipeContribution
- TemplateContribution

---

# Generation Recipe Contract

Generation recipes must follow the common generation contract:

name

profile

build_artifacts(
    specification
)

A recipe is responsible for describing generated artifacts while remaining independent from the runtime execution process.

