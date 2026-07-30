"""Plugin installation services."""

from .installed_plugin import InstalledPlugin
from .plugin_installer import PluginInstaller

__all__ = [
    "InstalledPlugin",
    "PluginInstaller",
]
