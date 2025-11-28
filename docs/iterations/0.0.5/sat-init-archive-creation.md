# sat-init-archive creation

```bash
title_slug: sat-init-archive-creation
```

Here’s a real, runnable MVP for `tools/sat-init-archive`, parallel to `sat-build-config`.

Create: 

```bash
nano sat-init-archive
```

Save this as:

```bash
sat-init-archive
chmod +x sat-init-archive
```

No markdown fences in the actual file, just the script:

```python
#!/usr/bin/env python3
"""
sat-init-archive (MVP)

Executable placed at:
    tools/sat-init-archive

Consumes a SAT configuration file (from sat-build-config) and creates
a minimal archive root on disk:

  <archive_root>/
    config/
      archive.yml

MVP: no language roots, no PARA structure, no plugin installation.
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
    print("[sat-init-archive] ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)


# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------

def load_yaml_file(path: Path) -> Dict[str, Any]:
    """Load a YAML file and ensure it is a mapping."""
    if not path.exists():
        print(f"[sat-init-archive] ERROR: config file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as exc:
        print(f"[sat-init-archive] ERROR: failed to read YAML from {path}: {exc}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict):
        print(f"[sat-init-archive] ERROR: YAML in {path} is not a mapping.", file=sys.stderr)
        sys.exit(1)
    return data


def ensure_dict(value: Any) -> Dict[str, Any]:
    """Normalize non-dict values to dicts."""
    return value if isinstance(value, dict) else {}


def dir_non_empty(path: Path) -> bool:
    """Return True if directory exists and contains at least one entry."""
    if not path.exists():
        return False
    if not path.is_dir():
        return True  # treat non-directory as "non-empty"/unsafe
    try:
        return any(path.iterdir())
    except PermissionError:
        # If we cannot list, consider it non-empty to be safe.
        return True


# ------------------------------------------------------------
# Core logic
# ------------------------------------------------------------

def validate_config(config: Dict[str, Any]) -> None:
    """Minimal validation for fields needed to initialize an archive."""
    schema_version = config.get("schema_version")
    if not schema_version:
        print("[sat-init-archive] ERROR: schema_version is missing or empty.", file=sys.stderr)
        sys.exit(1)

    ai = ensure_dict(config.get("archive_identity"))
    if not ai.get("id"):
        print("[sat-init-archive] ERROR: archive_identity.id is missing or empty.", file=sys.stderr)
        sys.exit(1)


def resolve_archive_root(config: Dict[str, Any], output_root: Optional[str]) -> Path:
    """Resolve the archive root from CLI override or configuration."""
    ai = ensure_dict(config.get("archive_identity"))

    if output_root:
        root_str = output_root
    else:
        root_str = ai.get("archive_root")

    if not root_str:
        print(
            "[sat-init-archive] ERROR: archive_identity.archive_root is missing and no --output-root was provided.",
            file=sys.stderr,
        )
        sys.exit(1)

    root = Path(root_str).expanduser().resolve()
    return root


def write_archive_config(root: Path, config: Dict[str, Any], dry_run: bool = False) -> None:
    """Write config/archive.yml with minimal fields."""
    ai = ensure_dict(config.get("archive_identity"))

    out_data: Dict[str, Any] = {
        "schema_version": config.get("schema_version"),
        "archive_identity": {
            "id": ai.get("id"),
            "label": ai.get("label"),
            "description": ai.get("description"),
            "archive_root": str(root),
        },
    }

    config_dir = root / "config"
    archive_yml = config_dir / "archive.yml"

    if dry_run:
        print(f"[sat-init-archive] DRY RUN: Would write {archive_yml}", file=sys.stderr)
        print(yaml.safe_dump(out_data, sort_keys=False, allow_unicode=True))
        return

    try:
        config_dir.mkdir(parents=True, exist_ok=True)
        with archive_yml.open("w", encoding="utf-8") as f:
            yaml.safe_dump(out_data, f, sort_keys=False, allow_unicode=True)
    except Exception as exc:
        print(f"[sat-init-archive] ERROR: Failed to write {archive_yml}: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"[sat-init-archive] Wrote {archive_yml}", file=sys.stderr)


def init_archive(config_path: Path, output_root: Optional[str], force: bool, dry_run: bool) -> None:
    """Main archive initialization routine."""
    # Load and validate config
    config = load_yaml_file(config_path)
    validate_config(config)

    # Resolve archive root
    root = resolve_archive_root(config, output_root)

    # Check directory state
    if root.exists():
        if root.is_file():
            print(
                f"[sat-init-archive] ERROR: {root} exists and is a file, cannot initialize archive here.",
                file=sys.stderr,
            )
            sys.exit(1)

        if dir_non_empty(root) and not force:
            print(
                f"[sat-init-archive] ERROR: {root} exists and is not empty. "
                f"Use --force to initialize anyway.",
                file=sys.stderr,
            )
            sys.exit(1)
    else:
        if dry_run:
            print(f"[sat-init-archive] DRY RUN: Would create archive root: {root}", file=sys.stderr)
        else:
            try:
                root.mkdir(parents=True, exist_ok=True)
                print(f"[sat-init-archive] Created archive root: {root}", file=sys.stderr)
            except Exception as exc:
                print(f"[sat-init-archive] ERROR: Failed to create archive root {root}: {exc}", file=sys.stderr)
                sys.exit(1)

    # Write minimal config/archive.yml
    write_archive_config(root, config, dry_run=dry_run)

    if not dry_run:
        print(f"[sat-init-archive] Archive initialized at: {root}", file=sys.stderr)


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sat-init-archive",
        description="Initialize a SAT archive root from an assembled configuration (MVP).",
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the assembled SAT configuration file (from sat-build-config).",
    )
    parser.add_argument(
        "--output-root",
        help="Override archive_identity.archive_root as the archive root path.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow initialization into an existing non-empty directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without modifying the filesystem.",
    )

    return parser.parse_args(argv)


def main(argv=None) -> None:
    args = parse_args(argv)
    config_path = Path(args.config)

    init_archive(
        config_path=config_path,
        output_root=args.output_root,
        force=args.force,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
```

------

### How to try it

From your SAT root (where `tools/` lives), with your working `sat-build-config`:

#### Generate a config

```bash
./sat-build-config \
  --archive-id universalcake.com \
  --archive-label "Universal Cake Source Archive" \
  --archive-description "Primary SAT archive for the Universal Cake ecosystem." \
  > archive-config.yml
```

##### Confirm our config contents

```bash
cat archive-config.yml
```

output example:

```bash
schema_version: 1.0.0
archive_identity:
  id: universalcake.com
  label: Universal Cake Source Archive
  description: Primary SAT archive for the Universal Cake ecosystem.
  archive_root: ../universalcake.com
```

#### Initialize the archive

```bash
./sat-init-archive --config archive-config.yml
```

Output example:

```bash
[sat-init-archive] Created archive root: /home/initial/projects/archives/dev/universalcake.com
[sat-init-archive] Wrote /home/initial/projects/archives/dev/universalcake.com/config/archive.yml
[sat-init-archive] Archive initialized at: /home/initial/projects/archives/dev/universalcake.com
```

#### Confirm your results

##### with ls

```bash
ls -al ../universalcake.com/
```

output example:

```bash
total 12
drwxrwxr-x 3 initial initial 4096 Nov 28 18:07 .
drwxrwxr-x 5 initial initial 4096 Nov 28 18:07 ..
drwxrwxr-x 2 initial initial 4096 Nov 28 18:07 config
```

##### using tree

```bash
tree ../universalcake.com/
```

You should end up with something like:

```text
../universalcake.com/
└── config
    └── archive.yml

2 directories, 1 file
```

##### using cat

```bash
cat ../universalcake.com/config/archive.yml
```

And `config/archive.yml` containing:

```yaml
schema_version: "1.0.0"
archive_identity:
  id: "universalcake.com"
  label: "Universal Cake Source Archive"
  description: "Primary SAT archive for the Universal Cake ecosystem."
  archive_root: "/absolute/path/to/../universalcake.com"
```

If you’d like, we can now:

- add creation of `en-ca/` and PARA dirs as the next step, or
- document this tool like we did for `sat-build-config` (design + usage doc), or
- start sketching language/metadata plugins so `sat-build-config` can emit more fields for `sat-init-archive` to act on.