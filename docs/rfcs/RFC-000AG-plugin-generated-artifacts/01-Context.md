# RFC-000AG — Plugin Generated Artifacts

## Context

FamilyOS provides two major extension systems:

- Plugin Ecosystem
- Generation Framework

The Plugin Ecosystem allows external capabilities to be integrated through contributions.

The Generation Framework provides:

- Generation Catalog
- Generation Recipes
- Artifact Definitions
- Generation Pipeline

The objective of this RFC is to define how plugins can participate in artifact generation without replacing the core generation engine.

## Current Architecture

Current flow:

Plugin

↓

Plugin Contribution

↓

Generation Contribution

↓

Generation Catalog

↓

Generation Recipe

↓

Artifact Definition

↓

Generated Output

## Goal

Allow plugins to extend generated artifacts while preserving:

- framework ownership,
- generation consistency,
- validation rules,
- backward compatibility.
