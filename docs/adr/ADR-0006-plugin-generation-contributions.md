# ADR-0006: Plugin Generation Contributions

## Status

Accepted

## Date

2026-07-30

## Context

The FamilyOS platform provides a Plugin SDK allowing extensions to contribute capabilities to the framework.

The Domain Generation Framework currently provides:

- generation presets
- generation catalog
- generation recipes
- generation strategies

These capabilities are currently defined by the core application.

However, FamilyOS domains and future extensions require the ability to introduce new generation capabilities without modifying the core framework.

Examples:

- security documentation generation
- health domain documentation
- finance domain packages
- custom enterprise domain templates

A plugin contribution mechanism is required to allow extensions to participate in generation discovery.

## Decision

Introduce Plugin Generation Contributions as an extension point of the Generation Framework.

Plugins may contribute:

- generation presets
- generation catalog entries
- generation recipes
- generation strategies

The core framework remains responsible for orchestration and execution.

Plugins provide capabilities through well-defined contribution contracts.

## Architecture

The extension flow becomes:

Plugin
|
v
Plugin Contribution
|
v
Generation Catalog
|
v
Generation Preset
|
v
Generation Recipe
|
v
Generation Strategy
|
v
Generated Artifacts

## Responsibilities

### Core Framework

Responsible for:

- managing generation lifecycle
- resolving presets
- executing recipes
- generating artifacts

### Plugin

Responsible for:

- declaring additional capabilities
- providing generation metadata
- registering custom generation components

## Rationale

This approach provides:

- extensibility without modifying core code
- separation between platform and extensions
- dynamic discovery of capabilities
- alignment with the existing Plugin SDK architecture

## Consequences

Positive consequences:

- plugins can extend generation features
- new domains can provide specialized generators
- CLI discovery becomes extensible

Trade-offs:

- contribution contracts must remain stable
- plugin compatibility must be managed

## Future Extensions

Future versions may support:

- plugin-owned templates
- plugin generation permissions
- generation capability versioning
- marketplace-distributed generation packages
