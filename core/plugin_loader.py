import yaml
from pathlib import Path
from importlib import import_module


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins"


def load_plugin(plugin_id: str):
    """
    Load a plugin by its ID, e.g., "metadata.dublin-core".
    Returns a dict with:
      - manifest (plugin.yml contents)
      - module (imported plugin.py)
      - callable (entrypoint function)
      - paths (standard, config)
    """
    raw_parts = plugin_id.split(".")  # e.g. ["metadata", "dublin-core"]

    # Use underscore-safe names for both filesystem and imports
    sanitized_parts = [p.replace("-", "_") for p in raw_parts]

    # Filesystem path: plugins/metadata/dublin_core/...
    plugin_path = PLUGIN_ROOT.joinpath(*sanitized_parts)

    manifest_file = plugin_path / "plugin.yml"
    if not manifest_file.exists():
        raise FileNotFoundError(f"Plugin manifest not found: {manifest_file}")

    with manifest_file.open("r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f) or {}

    entry = manifest["entrypoints"]["apply"]
    run_file = entry["run"]  # e.g. "plugin.py"

    # Import path: plugins.metadata.dublin_core.plugin
    module_import = "plugins." + ".".join(sanitized_parts) + "." + run_file.replace(".py", "")

    module = import_module(module_import)

    return {
        "manifest": manifest,
        "module": module,
        "callable": getattr(module, entry["callable"]),
        "paths": {
            "standard": plugin_path / manifest["paths"]["standard"],
            "config": plugin_path / manifest["paths"]["config"],
        },
    }


def load_plugin_config(plugin_info: dict):
    """Load plugin config YAML."""
    config_path = plugin_info["paths"]["config"] / "defaults.yml"

    if not config_path.exists():
        return {}

    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
