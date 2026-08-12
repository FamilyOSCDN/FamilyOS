# RFC-0003 — Plugin Discovery & Distribution

# 08 — Package Format

This document defines the standard package format for FamilyOS plugins.

Goals:

- deterministic packaging;
- versioned format;
- metadata availability;
- integrity validation;
- support for future distribution channels.

A plugin package contains:

- plugin manifest;
- metadata;
- implementation artifacts;
- resources;
- dependencies;
- verification information.

The package format must remain independent from repository implementations.
