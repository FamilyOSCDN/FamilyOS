# ADR-0004: Generation Presets

## Status

Accepted

## Date

2026-07-29

## Context

The FamilyOS Domain Generation Framework supports multiple generation recipes.

Recipes represent technical generation strategies and implementation details.

Current generation recipes include:

- domain documentation
- entity documentation
- aggregate documentation
- repository documentation
- service documentation
- full domain documentation

These recipes are required by the generation engine, but they expose internal implementation concepts.

Using recipes directly as the primary user interface creates a strong coupling between:

- CLI commands
- user workflows
- internal generation architecture

For example, exposing:

```bash
familyos create domain Person \
  --recipe full_domain_documentation
## Decision

Introduce **Generation Presets** as a user-facing abstraction layer.

A Generation Preset represents the desired generation level from the user's perspective.

Presets are resolved internally into one or more generation recipes.

The resolution flow is:

Generation Preset
|
v
Generation Preset Resolver
|
v
Generation Recipes
|
v
Generation Pipeline

The CLI should prefer presets for user interactions.

Recipes remain internal technical concepts.

## Preset Mapping

The FamilyOS Domain Generation Framework currently supports the following presets:

| Preset | Recipes |
|---|---|
| minimal | domain_documentation |
| standard | domain_documentation, entity_documentation, aggregate_documentation |
| complete | full_domain_documentation |

## Rationale

Generation Presets provide a stable abstraction between user intent and technical generation implementation.

Users define the expected generation level:

- minimal documentation
- standard domain model package
- complete domain documentation package

The framework decides internally which recipes must be executed.

This separation allows the generation architecture to evolve without changing the user-facing workflow.
## Consequences

### Positive consequences

Generation Presets provide:

- a stable user-facing API
- reduced coupling between CLI and internal architecture
- easier evolution of generation capabilities
- clearer intention-driven workflows

Users select a generation goal instead of individual technical artifacts.

The internal recipe composition can evolve without requiring changes in user commands.

### Negative consequences

The introduction of Generation Presets adds an additional abstraction layer.

The framework must maintain:

- preset definitions
- preset resolution rules
- preset contract tests

Changes to preset mappings require careful validation because presets represent a user-facing contract.

## Rules

The following rules apply:

1. Presets are user-facing concepts.
2. Recipes are internal generation implementation details.
3. CLI commands should prefer presets over direct recipe selection.
4. Changes to preset mappings require contract tests.
5. Presets must resolve deterministically.
6. Existing recipe-based generation remains supported for backward compatibility.

## Future Evolution

Future presets may introduce additional generation profiles, such as:

- enterprise
- documentation-only
- implementation-ready

New presets should extend the intention-based model without exposing internal recipe composition.

The Generation Preset framework should continue to provide a stable interface while allowing the Domain Generation Framework to evolve internally.

