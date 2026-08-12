# Validation

## Architecture Validation

The implementation must guarantee:

- existing plugins continue working,
- built-in recipes remain unchanged,
- plugin recipes are registered safely,
- duplicate recipe names are rejected.

## Technical Validation

Required checks:

- mypy
- ruff
- pytest

## Acceptance Criteria

A plugin must be able to:

1. expose a generation recipe,
2. register the recipe,
3. use the recipe through the generation framework,
4. generate artifacts using the standard pipeline.
