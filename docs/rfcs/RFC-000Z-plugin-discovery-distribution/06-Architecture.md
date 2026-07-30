# RFC-000Z — Plugin Discovery & Distribution

# 06 — Architecture

The architecture introduces dedicated layers:

- discovery;
- repository;
- package;
- resolution;
- installation;
- verification;
- lifecycle.

Core components:

- PluginDiscoveryService;
- PluginRepository;
- PluginPackage;
- PluginResolver;
- PluginInstaller;
- PluginVerifier;
- PluginLifecycleManager.

Distribution remains separated from runtime execution.
