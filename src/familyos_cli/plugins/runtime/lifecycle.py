from __future__ import annotations


class Lifecycle:
    """Standard plugin lifecycle events."""

    INITIALIZE = "initialize"
    SHUTDOWN = "shutdown"

    BEFORE_GENERATE = "before_generate"
    AFTER_GENERATE = "after_generate"
