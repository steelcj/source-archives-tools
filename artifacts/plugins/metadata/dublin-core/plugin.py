"""
metadata/dublin-core plugin.

- standard/: holds upstream or conceptual definitions
- config/:   holds source-archive-tools-specific mappings or defaults
"""

from typing import Any, Dict

from tools.core.plugin_base import Plugin


class Metadatadublin_^corePlugin(Plugin):  # simple stub name
    def apply(self, context: Dict[str, Any]) -> None:
        # TODO: implement plugin logic
        root_dir = context.get("root_dir")
        print(f"[metadata.dublin-core] apply() called for root: {root_dir}")
