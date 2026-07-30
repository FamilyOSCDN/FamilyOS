# ADR-0005: Generation Catalog

## Status

Accepted

## Date

2026-07-30

## Context

The FamilyOS Domain Generation Framework provides multiple generation capabilities.

These capabilities are implemented through:

- generation presets
- generation recipes
- generation strategies

Generation presets provide a user-oriented abstraction over technical recipes.

However, users and external tools need a way to discover available generation capabilities without knowing internal implementation details.

Direct exposure of recipes would create coupling between:

- CLI commands
- user workflows
- internal generation implementation

The framework requires a stable discovery layer capable of describing:

- available generation presets
- their purpose
- associated recipes

## Decision

Introduce a **Generation Catalog** as the official discovery layer of the FamilyOS Generation Framework.

The Generation Catalog exposes discoverable generation capabilities through catalog entries.

Each catalog entry contains:

- a generation preset
- a human-readable description
- the recipes associated with that preset

The catalog becomes the boundary between user-facing discovery and internal generation implementation.

## Architecture

The generation discovery flow becomes:

User
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

### Generation Catalog

Responsible for:

- exposing available generation capabilities
- providing descriptions
- allowing discovery by applications and CLI interfaces

### Generation Preset

Responsible for:

- representing user intent
- defining a generation level

Examples:

- minimal
- standard
- complete

### Generation Recipe

Responsible for:

- describing technical generation operations
- mapping to concrete generation implementations

## Rationale

The Generation Catalog provides:

- a stable discovery API
- separation between user experience and implementation
- future plugin extensibility
- easier CLI and tooling integration

Plugins can later contribute their own catalog entries without changing the core generation framework.

## Consequences

Positive consequences:

- users no longer need to know recipe names
- CLI can expose available capabilities dynamically
- generation features become discoverable
- plugins can extend generation capabilities

Trade-offs:

- introduces an additional abstraction layer
- catalog lifecycle must remain synchronized with available generation features

## Future Extensions

The Generation Catalog can evolve to support:

- plugin-contributed generation entries
- capability metadata
- compatibility information
- documentation generation
- API exposure
