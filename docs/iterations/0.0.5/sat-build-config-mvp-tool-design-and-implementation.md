# SAT Tool Design and Implementation: The `sat-build-config` MVP Executable

```yaml
slug: sat-build-config-mvp-tool-design-and-implementation
```

## Overview

This document describes the minimal viable product (MVP) implementation of the `sat-build-config` tool. The tool is placed directly in the SAT tools root as an executable named:

```
tools/sat-build-config
```

This script is responsible for assembling a SAT archive configuration from core plugins, archive-level configuration, and CLI overrides. It performs no filesystem operations outside of writing the final YAML configuration to standard output or an explicitly provided file.

The MVP implementation focuses exclusively on:

- `core.schema` plugin
- `core.archive-identity` plugin
- archive-level configuration (`--config`)
- CLI overrides
- template expansion
- minimal validation

This provides a stable foundation for future SAT tooling (`sat-init-archive`, metadata plugins, language plugins, taxonomy plugins, and advanced schema enforcement).

---

## Tool Responsibilities

`sat-build-config` performs the following:

- Determines the SAT root directory automatically based on its own file location
- Loads required core plugins:
  - `core.schema`
  - `core.archive-identity`
- Reads each plugin’s `plugin.yml` and `etc/defaults.yml`
- Deep merges plugin configuration fragments
- Optionally merges an archive-level configuration file
- Applies CLI overrides
- Expands simple templates (e.g., `{{ archive_identity.id }}`)
- Validates core fields
- Emits a single YAML configuration document

It does **not** create an archive directory structure.
It does **not** execute plugins or initialize PARA directories.
Those responsibilities belong to `sat-init-archive`.

---

## Plugin File Requirements

Each plugin must contain:

```
plugin.yml
etc/defaults.yml
```

If either file is missing, `sat-build-config`:

1. Prints a message describing what is missing
2. Skips loading that file or plugin
3. Continues execution

For core plugins (`core.schema`, `core.archive-identity`) these files are required. Missing files in required plugins result in a clean error and exit.

---

## Directory Structure

`sat-build-config` expects the following SAT layout:

```
tools/
sat-build-config # < executable (Python script)
plugins/
core/
schema/
plugin.yml
etc/
defaults.yml
archive-identity/
plugin.yml
etc/
defaults.yml
```

Placement in `tools/sat-build-config` ensures:

- the tool can automatically derive the SAT root
- plugin discovery does not depend on the execution location
- installation is portable within the SAT ecosystem

---

## Core Plugin Defaults (MVP)

### core.schema

```yaml
defaults:
config_fragments:
schema_version: "1.0.0"
```

### core.archive-identity

```yaml
defaults:
config_fragments:
archive_identity:
id: "unnamed-archive"
label: "SAT Test Archive"
description: "A SAT archive initialized with default testing configuration."
archive_root: "../{{ archive_identity.id }}"
```

These defaults supply:

- a valid schema version
- a safe and testable archive identity
- a template-driven `archive_root`

---

## CLI Interface (MVP)

```bash
sat-build-config [options]
```

Supported flags:

```
--config <file> Optional archive-level configuration file
--archive-id <id> Override archive_identity.id
--archive-label <label> Override archive_identity.label
--archive-description <desc>Override archive_identity.description
--archive-root <path> Override archive_identity.archive_root
--output <file> Write configuration to file instead of stdout
```

---

## Template Expansion

The MVP supports only a single template:

```
{{ archive_identity.id }}
```

This is currently used to automatically expand:

```
archive_root: "../{{ archive_identity.id }}"
```

which becomes:

```
../universalcake.com
```

when the archive id is overridden with:

```
--archive-id universalcake.com
```

---

## Minimal Validation

The MVP rejects configurations missing any of the following:

- `schema_version`
- `archive_identity.id`
- `archive_identity.archive_root`

This ensures that `sat-init-archive` always receives a valid configuration.

---

## Final MVP Executable

Below is the complete code for the MVP single-file executable.

Create:

```bash
nano sat-build-config
```

Content:


```python
#!/usr/bin/env python3
"""
sat-build-config (MVP)

Executable placed at:
    tools/sat-build-config

Discovers plugins under:
    tools/plugins/

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
except ImportError:
    print("[sat-build-config] ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)

# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------

def load_yaml_file(path: Path) -> Optional[Dict[str, Any]]:
    """Load a YAML file safely."""
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as exc:
        print(f"[sat-build-config] ERROR: reading YAML file {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursive merge of dictionaries."""
    for key, val in override.items():
        if (
            key in base
            and isinstance(base[key], dict)
            and isinstance(val, dict)
        ):
            base[key] = deep_merge(base[key], val)
        else:
            base[key] = val
    return base


def ensure_dict(value: Any) -> Dict[str, Any]:
    """Normalize non-dict values to dicts."""
    return value if isinstance(value, dict) else {}

# ------------------------------------------------------------
# Plugin loading
# ------------------------------------------------------------

def load_core_plugin_defaults(sat_root: Path, plugin_rel: str, plugin_id: str, required=True):
    """
    Load defaults for a core plugin located at:
        tools/plugins/<plugin_rel>/
    """
    plugin_dir = sat_root / "tools" / "plugins" / plugin_rel
    plugin_yml = plugin_dir / "plugin.yml"
    defaults_yml = plugin_dir / "etc" / "defaults.yml"

    # plugin.yml missing
    if not plugin_yml.exists():
        msg = f"[sat-build-config] {'ERROR' if required else 'WARN'}: Missing plugin.yml for {plugin_id} at {plugin_dir}"
        print(msg, file=sys.stderr)
        if required:
            sys.exit(1)
        return {}

    plugin_meta = load_yaml_file(plugin_yml) or {}
    if plugin_meta.get("id") != plugin_id:
        print(
            f"[sat-build-config] WARN: plugin id mismatch for {plugin_dir}. "
            f"Expected '{plugin_id}', got '{plugin_meta.get('id')}'.",
            file=sys.stderr,
        )

    # defaults.yml missing
    if not defaults_yml.exists():
        msg = f"[sat-build-config] {'ERROR' if required else 'WARN'}: Missing etc/defaults.yml for {plugin_id}"
        print(msg, file=sys.stderr)
        if required:
            sys.exit(1)
        return {}

    data = load_yaml_file(defaults_yml) or {}
    defaults = data.get("defaults", {})
    fragments = defaults.get("config_fragments", {})

    if not isinstance(fragments, dict):
        print(
            f"[sat-build-config] WARN: config_fragments for {plugin_id} is not a dict; ignoring.",
            file=sys.stderr,
        )
        return {}

    return fragments

# ------------------------------------------------------------
# Template expansion
# ------------------------------------------------------------

def expand_templates(config: Dict[str, Any]) -> None:
    """MVP: expand ../{{ archive_identity.id }}"""
    ai = ensure_dict(config.get("archive_identity"))
    archive_id = ai.get("id")

    if not archive_id:
        return

    root = ai.get("archive_root")
    if isinstance(root, str) and "{{ archive_identity.id }}" in root:
        ai["archive_root"] = root.replace("{{ archive_identity.id }}", str(archive_id))

    config["archive_identity"] = ai

# ------------------------------------------------------------
# Validation
# ------------------------------------------------------------

def validate_config(config: Dict[str, Any]) -> None:
    errors = []
    if not config.get("schema_version"):
        errors.append("Missing: schema_version")

    ai = ensure_dict(config.get("archive_identity"))
    if not ai.get("id"):
        errors.append("Missing: archive_identity.id")
    if not ai.get("archive_root"):
        errors.append("Missing: archive_identity.archive_root")

    if errors:
        print("[sat-build-config] ERROR: invalid configuration:", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        sys.exit(1)

# ------------------------------------------------------------
# Core build function
# ------------------------------------------------------------

def build_config(args) -> Dict[str, Any]:
    config: Dict[str, Any] = {}

    # SAT root = directory containing "tools/"
    sat_root = Path(__file__).resolve().parents[1]

    # Load core.schema
    schema = load_core_plugin_defaults(
        sat_root, "core/schema", "core.schema", required=True
    )
    config = deep_merge(config, schema)

    # Load core.archive-identity
    archive_id = load_core_plugin_defaults(
        sat_root, "core/archive-identity", "core.archive-identity", required=True
    )
    config = deep_merge(config, archive_id)

    # Optional: archive-level config
    if args.config:
        cfg_path = Path(args.config)
        archive_cfg = load_yaml_file(cfg_path)
        if archive_cfg is None:
            print(f"[sat-build-config] ERROR: --config file not found: {cfg_path}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(archive_cfg, dict):
            print(f"[sat-build-config] ERROR: --config must be a YAML mapping", file=sys.stderr)
            sys.exit(1)
        config = deep_merge(config, archive_cfg)

    # CLI overrides
    ai = ensure_dict(config.get("archive_identity"))

    if args.archive_id:
        ai["id"] = args.archive_id
    if args.archive_label:
        ai["label"] = args.archive_label
    if args.archive_description:
        ai["description"] = args.archive_description
    if args.archive_root:
        ai["archive_root"] = args.archive_root

    config["archive_identity"] = ai

    # Expand templates
    expand_templates(config)

    # Validate
    validate_config(config)

    return config

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(
        prog="sat-build-config",
        description="Assemble the SAT archive configuration (MVP)."
    )

    p.add_argument("--config", help="Archive-level config file")
    p.add_argument("--archive-id", help="Override archive_identity.id")
    p.add_argument("--archive-label", help="Override archive_identity.label")
    p.add_argument("--archive-description", help="Override archive_identity.description")
    p.add_argument("--archive-root", help="Override archive_identity.archive_root")
    p.add_argument("--output", "-o", help="Write YAML output to file")

    return p.parse_args()

def main():
    args = parse_args()
    config = build_config(args)

    yaml_text = yaml.safe_dump(config, sort_keys=False, allow_unicode=True)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(yaml_text, encoding="utf-8")
    else:
        sys.stdout.write(yaml_text)

if __name__ == "__main__":
    main()
```

and make it executable:

```bash
chmod +x sat-build-config
```

