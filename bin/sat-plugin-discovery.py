#!/usr/bin/env python3
"""
sat-plugin-discovery (MVP)

Executable placed at:
    bin/sat-build-config

Discovers plugins under:
    plugins/

Automatically determines SAT root based on its own location.
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# ------------------------------------------------------------
# Import YAML safely
# ------------------------------------------------------------

try:
    import yaml
except ImportError:  # pragma: no cover
    print("[sat-build-config] ERROR: PyYAML is required (pip install pyyaml).", file=sys.stderr)
    sys.exit(1)


# ------------------------------------------------------------
# YAML helpers
# ------------------------------------------------------------

def load_yaml_file(path: Path) -> Dict[str, Any]:
    """
    Load YAML from a file path and ensure we return a dict.
    If the file does not exist, return {}.
    """
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as exc:  # pragma: no cover - defensive
        print(f"[sat-build-config] ERROR: failed to read YAML from {path}: {exc}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict):
        print(f"[sat-build-config] ERROR: YAML in {path} is not a mapping.", file=sys.stderr)
        sys.exit(1)
    return data


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep-merge two dictionaries.
    - For nested dicts, merge recursively.
    - For other values, 'override' wins.
    """
    result = dict(base)
    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def ensure_dict(value: Any) -> Dict[str, Any]:
    """Normalize non-dict values to dicts."""
    return value if isinstance(value, dict) else {}


# ------------------------------------------------------------
# Plugin loading helpers
# ------------------------------------------------------------

def load_core_plugin_defaults(sat_root: Path, plugin_rel: str, plugin_id: str, required=True):
    """
    Load defaults for a core plugin located at:
        bin/sat-build-config
        plugins/<plugin_rel>/
    """
    plugin_dir = sat_root / "plugins" / plugin_rel
    plugin_yml = plugin_dir / "plugin.yml"
    defaults_yml = plugin_dir / "etc" / "defaults.yml"

    # plugin.yml missing
    if not plugin_yml.exists():
        msg = f"[sat-build-config] {'ERROR' if required else 'WARN'}: Missing plugin.yml for {plugin_id} at {plugin_dir}"
        print(msg, file=sys.stderr)
        if required:
            sys.exit(1)
        return {}

    plugin_meta = load_yaml_file(plugin_yml)

    # Validate plugin id if present
    if "id" in plugin_meta and plugin_meta["id"] != plugin_id:
        print(
            f"[sat-build-config] ERROR: plugin id mismatch for {plugin_id}: "
            f"{plugin_meta['id']} != {plugin_id}",
            file=sys.stderr,
        )
        sys.exit(1)

    # defaults.yml missing
    if not defaults_yml.exists():
        msg = f"[sat-build-config] {'ERROR' if required else 'WARN'}: Missing defaults.yml for {plugin_id} at {defaults_yml}"
        print(msg, file=sys.stderr)
        if required:
            sys.exit(1)
        return {}

    defaults_data = load_yaml_file(defaults_yml)
    return ensure_dict(defaults_data.get("defaults", {}))


# ------------------------------------------------------------
# CLI and config building
# ------------------------------------------------------------

def build_config(output_path: Path, verbose: bool = False) -> None:
    """
    Build the SAT archive configuration at output_path.

    MVP behavior:
    - Start with an empty config dict.
    - Load defaults from core plugins (e.g., core.schema, core.archive-identity).
    - Write the merged config to output_path as YAML.
    """
    config: Dict[str, Any] = {}

    # SAT root = directory containing "bin/"
    sat_root = Path(__file__).resolve().parents[1]

    # Load core.schema
    schema = load_core_plugin_defaults(
        sat_root, "core/schema", "core.schema", required=True
    )
    config = deep_merge(config, schema)

    # Load core.archive-identity
    archive_id = load_core_plugin_defaults(
        sat_root, "core/archive-identity", "core.archive-identity", required=False
    )
    config = deep_merge(config, archive_id)

    # Additional plugins can be loaded here in the future

    # Write final config
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(config, f, sort_keys=False)

    if verbose:
        print(f"[sat-build-config] Wrote config to {output_path}")


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build SAT archive configuration (MVP)."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="config/archive.yml",
        help="Path to write the generated configuration file (default: config/archive.yml).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    output_path = Path(args.output)
    build_config(output_path=output_path, verbose=args.verbose)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
