# Decision

## Decision

FamilyOS plugins may contribute generation recipes.

The Generation Framework remains responsible for execution.

## New Extension Concept

A plugin may expose:

GenerationRecipeContribution

containing:

- a GenerationRecipe implementation.

## Existing Contribution Model

The existing ContributionRegistry remains the central extension mechanism.

New contribution types are resolved through the existing registry.

## Rationale

This approach provides:

- loose coupling,
- plugin isolation,
- reusable recipes,
- controlled extensibility.
