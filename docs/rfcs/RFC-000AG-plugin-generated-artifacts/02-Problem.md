# Problem Statement

## Current Limitation

The current plugin contribution system supports:

- generation presets,
- domain generation contributions.

However, plugins cannot yet contribute new generation recipes.

The GenerationRecipeRegistry currently contains only built-in recipes.

## Architectural Question

Should plugins:

1. replace generation strategies,
2. provide recipes,
3. directly generate artifacts?

## Constraints

Plugins must not:

- bypass the generation engine,
- write files directly,
- redefine core generation rules.

The framework must remain the owner of generation behavior.
