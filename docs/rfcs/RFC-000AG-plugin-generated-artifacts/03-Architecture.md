# Architecture

## Selected Model

FamilyOS adopts a recipe-based extension model.

Architecture:

Plugin

↓

Generation Contribution

↓

Recipe Reference

+

Recipe Extension

↓

Generation Recipe Registry

↓

Recipe Executor

↓

Artifact Definitions

↓

Generated Output


## Responsibilities

### Plugin

Responsible for:

- providing extensions,
- declaring generation capabilities.

### Generation Framework

Responsible for:

- recipe execution,
- artifact generation,
- validation,
- output creation.

## Forbidden Extension

Plugins must not provide custom generation engines.

The following model is rejected:

Plugin

↓

Custom Generation Strategy

↓

Direct Artifact Generation
