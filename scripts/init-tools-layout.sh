#!/usr/bin/env bash
set -euo pipefail

# Initialize the source-archive-tools layout under ./tools
# Safe to re-run (idempotent): will not overwrite existing files.

ROOT_DIR="${1:-.}"

TOOLS_DIR="${ROOT_DIR}/tools"
PLUGINS_DIR="${TOOLS_DIR}/plugins"
CORE_DIR="${TOOLS_DIR}/core"
CLI_DIR="${TOOLS_DIR}/cli"

echo "Initializing tools layout under: ${TOOLS_DIR}"

mkdir -p "${CORE_DIR}"
mkdir -p "${CLI_DIR}"
mkdir -p "${PLUGINS_DIR}"

# -------------------------------------------------------------------
# Core: shared helpers / base classes
# -------------------------------------------------------------------
if [[ ! -f "${CORE_DIR}/__init__.py" ]]; then
  cat > "${CORE_DIR}/__init__.py" <<EOF
"""
core: shared utilities and base classes for source-archive-tools plugins.
"""
EOF
fi

if [[ ! -f "${CORE_DIR}/plugin_base.py" ]]; then
  cat > "${CORE_DIR}/plugin_base.py" <<EOF
"""
Base plugin interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

class Plugin(ABC):
    @abstractmethod
    def apply(self, context: Dict[str, Any]) -> None:
        """Apply this plugin to the given context (archive root, config, etc.)."""
        raise NotImplementedError
EOF
fi

# -------------------------------------------------------------------
# CLI: thin entrypoints (stubs for now)
# -------------------------------------------------------------------
if [[ ! -f "${CLI_DIR}/sat-apply-taxonomy" ]]; then
  cat > "${CLI_DIR}/sat-apply-taxonomy" <<'EOF'
#!/usr/bin/env python3
"""
CLI stub for applying taxonomy to a source archive.

Future:
  - read config/structure.yml
  - load taxonomy_from and taxonomy plugin
  - apply directories under each locale root.
"""
import sys

def main() -> int:
    print("sat-apply-taxonomy: not implemented yet (stub).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
EOF
  chmod +x "${CLI_DIR}/sat-apply-taxonomy"
fi

# -------------------------------------------------------------------
# Helper to create a plugin skeleton
# -------------------------------------------------------------------
create_plugin_skeleton() {
  local family="$1"   # e.g. metadata, taxonomy, generators
  local name="$2"     # e.g. dublin-core, para, radial-wheel

  local base="${PLUGINS_DIR}/${family}/${name}"
  mkdir -p "${base}/standard" "${base}/config"

  # plugin.py
  if [[ ! -f "${base}/plugin.py" ]]; then
    cat > "${base}/plugin.py" <<EOF
"""
${family}/${name} plugin.

- standard/: holds upstream or conceptual definitions
- config/:   holds source-archive-tools-specific mappings or defaults
"""

from typing import Any, Dict

from tools.core.plugin_base import Plugin


class ${family^}${name//-/_^}Plugin(Plugin):  # simple stub name
    def apply(self, context: Dict[str, Any]) -> None:
        # TODO: implement plugin logic
        root_dir = context.get("root_dir")
        print(f"[${family}.${name}] apply() called for root: {root_dir}")
EOF
  fi

  # plugin.yml
  if [[ ! -f "${base}/plugin.yml" ]]; then
    cat > "${base}/plugin.yml" <<EOF
id: "${family}.${name}"
version: "0.1.0"
kind: "${family}"
entry_point: "tools.plugins.${family}.${name}.plugin"
standard_dir: "standard"
config_dir: "config"
EOF
  fi

  # README stub
  if [[ ! -f "${base}/README.md" ]]; then
    cat > "${base}/README.md" <<EOF
# ${family}/${name} Plugin

- \`standard/\`: upstream or conceptual definitions.
- \`config/\`: source-archive-tools-specific mapping and defaults.
- \`plugin.py\`: executable adapter logic.
- \`plugin.yml\`: minimal manifest used by the plugin loader.
EOF
  fi
}

# Create some initial plugins
create_plugin_skeleton "metadata" "dublin-core"
create_plugin_skeleton "taxonomy" "para"
create_plugin_skeleton "generators" "radial-wheel"

echo "Done. tools layout initialized."
