# RFC-0003 — Plugin Discovery & Distribution

# 19 — Testing

The plugin distribution system requires multiple testing levels.

Unit tests:

- domain objects;
- resolvers;
- validators.

Integration tests:

- repositories;
- installation workflow;
- lifecycle operations.

End-to-end tests:

- CLI plugin commands;
- complete installation scenarios.

Quality gates:

- Ruff;
- MyPy;
- Pytest.
