# RFC-000Z — Plugin Discovery & Distribution

# 07 — Domain Model

Main domain concepts:

## Aggregates

- PluginPackage
- PluginInstallation

## Entities

- PluginRepository

## Value Objects

- PluginIdentifier
- PluginVersion
- PluginDependency
- PluginChecksum
- PluginSource

The model follows FamilyOS DDD principles and keeps distribution separated from execution.
