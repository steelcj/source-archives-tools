# Setup Testing for Dublin Core

## Ensure plugin path is import-safe

If your plugin directory is still named `dublin-core`, rename it so Python can import it:

```bash
mv plugins/metadata/dublin-core plugins/metadata/dublin_core
```

Make sure `__init__.py` files exist:

```bash
touch plugins/__init__.py
touch plugins/metadata/__init__.py
touch plugins/metadata/dublin_core/__init__.py
```

## Update `core/plugin_loader.py` to match this layout

Overwrite `core/plugin_loader.py` with this:

```bash
cat > core/plugin_loader.py << 'EOF'
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
EOF
```

Confirmation:

```bash
cat core/plugin_loader.py
```

## Create plugin self-test: `plugins/metadata/dublin_core/self_test.py`

```bash
cat > plugins/metadata/dublin_core/self_test.py << 'EOF'
from pathlib import Path
import yaml

from core.plugin_loader import load_plugin, load_plugin_config  # type: ignore


REPO_ROOT = Path(__file__).resolve().parents[3]
EXAMPLES_DIR = REPO_ROOT / "plugins" / "metadata" / "dublin_core" / "examples"


REQUIRED_FIELDS = ["DC_Title", "DC_Creator", "DC_Language", "DC_License"]


def run_self_tests() -> bool:
    plugin_id = "metadata.dublin-core"
    plugin_info = load_plugin(plugin_id)
    config = load_plugin_config(plugin_info)
    apply_fn = plugin_info["callable"]

    example_files = [
        "minimal.yml",
        "defaults.yml",
        "custom.yml",
        "complete.yml",
    ]

    all_ok = True

    for name in example_files:
        path = EXAMPLES_DIR / name
        if not path.exists():
            print(f"[FAIL] Example missing: {path}")
            all_ok = False
            continue

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        updated = apply_fn(data, config)

        # Basic checks: required fields present and not placeholder
        for field in REQUIRED_FIELDS:
            value = updated.get(field)
            if value in (None, "", "__REQUIRED_FIELD_MISSING__"):
                print(f"[FAIL] {name}: field {field} invalid ({value!r})")
                all_ok = False

        if all_ok:
            print(f"[OK] {name}")

    return all_ok


def main():
    ok = run_self_tests()
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
EOF
```

Confirmation:

```bash
cat plugins/metadata/dublin_core/self_test.py
```



## Create a CLI wrapper: `cli/sat-test-plugin`

```bash
cat > cli/sat-test-plugin << 'EOF'
#!/usr/bin/env python3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


def main():
    if len(sys.argv) < 2:
        print("Usage: sat-test-plugin <plugin-id>")
        sys.exit(1)

    plugin_id = sys.argv[1]

    if plugin_id == "metadata.dublin-core":
        from plugins.metadata.dublin_core import self_test
        ok = self_test.run_self_tests()
        if not ok:
            sys.exit(1)
        sys.exit(0)
    else:
        print(f"No self-test implemented for plugin: {plugin_id}")
        sys.exit(2)


if __name__ == "__main__":
    main()
EOF
```

Confirm:

```bash
cat cli/sat-test-plugin
```

Make executable:

```bash
chmod +x cli/sat-test-plugin
```

## Run the self-test for Dublin Core

From the repo root (`tools/`):

```bash
./cli/sat-test-plugin metadata.dublin-core
```

You should see `[OK] ...` lines for each example, or clear `[FAIL]` messages if something is off.

Example:

```bash
[OK] minimal.yml
[OK] defaults.yml
[OK] custom.yml
[OK] complete.yml
```

Ok, so now we have a fully self-testing Dublin Core plugin.

With:

- plugin manifest
- plugin implementation
- defaults config
- examples
- self-test wired through `sat-test-plugin`