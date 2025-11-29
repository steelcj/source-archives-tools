# sat-tree-mvp

Yeah, I think you’re absolutely right: sat-tree is going to end up doing a *lot* for you long-term, so it’s good to start small and keep `sat-init-archive` boring and safe.

Here’s a **sat-tree MVP** that plugs into what you already have today.

------

## sat-tree MVP: what it does

For now, this tool will:

1. **Read `config/archive.yml`** (the one written by `sat-init-archive`).
2. **Figure out which directories “should” exist**, based on:
   - `archive_identity.archive_root`
   - `language_roots[*].slug`
   - `para_roots[*].slug` (if present)
3. **Check the filesystem** and:
   - Report missing directories
   - Optionally **create missing directories** (`--create-missing`)
4. Respect `--dry-run` (only prints what it *would* do).

No content, no docs, no fancy tree output yet. Just: “what should exist?”, “what exists?”, and “do you want me to fix it?”.

------

## sat-tree MVP script

Drop this in `tools/sat-tree` and make it executable:

```python
#!/usr/bin/env python3
"""
sat-tree (MVP)

Executable placed at:
    tools/sat-tree

Consumes a SAT archive configuration file (typically config/archive.yml)
and compares the *expected* directory structure derived from the config
to the *actual* filesystem state.

MVP behavior:
  - Reads:
      - schema_version
      - archive_identity.archive_root
      - language_roots[*].slug (if any)
      - para_roots[*].slug (if any)
  - Computes expected directories:
      <archive_root>/
      <archive_root>/<language_slug>/
      <archive_root>/<language_slug>/<para_slug>/  (if para_roots present)
  - Reports missing directories.
  - Optionally creates missing directories with --create-missing.
  - Supports --dry-run to show actions without modifying the filesystem.

Does NOT:
  - Remove extra directories
  - Generate content or docs
  - Handle deeper taxonomy levels (yet)
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print("[sat-tree] ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)


# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------

def load_yaml_file(path: Path) -> Dict[str, Any]:
    """Load a YAML file and ensure it is a mapping."""
    if not path.exists():
        print(f"[sat-tree] ERROR: config file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as exc:
        print(f"[sat-tree] ERROR: failed to read YAML from {path}: {exc}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict):
        print(f"[sat-tree] ERROR: YAML in {path} is not a mapping.", file=sys.stderr)
        sys.exit(1)
    return data


def ensure_dict(value: Any) -> Dict[str, Any]:
    """Normalize non-dict values to dicts."""
    return value if isinstance(value, dict) else {}


# ------------------------------------------------------------
# Expected structure computation
# ------------------------------------------------------------

def compute_expected_dirs(config: Dict[str, Any]) -> List[Path]:
    """
    Compute the list of directories that *should* exist based on the config.

    - archive_root
    - archive_root/<language_slug>          (if language_roots)
    - archive_root/<language_slug>/<para_slug>  (if para_roots)
    """
    ai = ensure_dict(config.get("archive_identity"))
    root_str = ai.get("archive_root")

    if not root_str:
        print("[sat-tree] ERROR: archive_identity.archive_root is missing in config.", file=sys.stderr)
        sys.exit(1)

    archive_root = Path(root_str).expanduser().resolve()

    expected: List[Path] = [archive_root]

    language_roots = config.get("language_roots") or []
    para_roots = config.get("para_roots") or []

    has_languages = isinstance(language_roots, list) and len(language_roots) > 0
    has_para = isinstance(para_roots, list) and len(para_roots) > 0

    if has_languages:
        for lang in language_roots:
            if not isinstance(lang, dict):
                continue
            lang_slug = lang.get("slug")
            if not lang_slug:
                continue
            lang_dir = archive_root / lang_slug
            expected.append(lang_dir)

            if has_para:
                for para in para_roots:
                    if not isinstance(para, dict):
                        continue
                    para_slug = para.get("slug")
                    if not para_slug:
                        continue
                    expected.append(lang_dir / para_slug)

    return sorted(set(expected))


def find_missing_dirs(expected: List[Path]) -> List[Path]:
    """Return the subset of expected paths that do not currently exist."""
    missing = [p for p in expected if not p.exists()]
    return missing


# ------------------------------------------------------------
# Core logic
# ------------------------------------------------------------

def apply_tree_actions(expected: List[Path], create_missing: bool, dry_run: bool) -> None:
    """Report and optionally create missing directories."""
    missing = find_missing_dirs(expected)

    if not missing:
        print("[sat-tree] All expected directories are present.", file=sys.stderr)
        return

    print("[sat-tree] Missing directories:", file=sys.stderr)
    for p in missing:
        print(f"  - {p}", file=sys.stderr)

    if not create_missing:
        print("[sat-tree] Use --create-missing to create these directories.", file=sys.stderr)
        return

    # Create missing directories
    for p in missing:
        if dry_run:
            print(f"[sat-tree] DRY RUN: Would create {p}", file=sys.stderr)
            continue

        try:
            p.mkdir(parents=True, exist_ok=True)
            print(f"[sat-tree] Created {p}", file=sys.stderr)
        except Exception as exc:
            print(f"[sat-tree] ERROR: Failed to create {p}: {exc}", file=sys.stderr)
            sys.exit(1)


def run_sat_tree(config_path: Path, create_missing: bool, dry_run: bool) -> None:
    """Main sat-tree routine."""
    config = load_yaml_file(config_path)
    expected_dirs = compute_expected_dirs(config)

    print("[sat-tree] Expected directory structure:", file=sys.stderr)
    for p in expected_dirs:
        print(f"  - {p}", file=sys.stderr)

    apply_tree_actions(expected_dirs, create_missing=create_missing, dry_run=dry_run)


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sat-tree",
        description="Inspect and optionally repair a SAT archive directory tree based on its configuration.",
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the SAT archive configuration file (e.g., config/archive.yml).",
    )
    parser.add_argument(
        "--create-missing",
        action="store_true",
        help="Create any missing directories that are expected by the config.",
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

    run_sat_tree(
        config_path=config_path,
        create_missing=args.create_missing,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
```

------

## How to use the MVP

Assuming you’ve already done:

```bash
./sat-build-config > /tmp/archive.yml
./sat-init-archive --config /tmp/archive.yml
```

Your archive has `config/archive.yml` inside it.

Now you can:

### Inspect what sat-tree thinks should exist

```bash
./sat-tree --config ../unnamed-archive/config/archive.yml --dry-run
```

Output example:

```bash
[sat-tree] Expected directory structure:
  - /home/initial/projects/archives/dev/unnamed-archive
  - /home/initial/projects/archives/dev/unnamed-archive/en-ca
  - /home/initial/projects/archives/dev/unnamed-archive/en-ca/archives
  - /home/initial/projects/archives/dev/unnamed-archive/en-ca/areas
  - /home/initial/projects/archives/dev/unnamed-archive/en-ca/projects
  - /home/initial/projects/archives/dev/unnamed-archive/en-ca/resources
  - /home/initial/projects/archives/dev/unnamed-archive/fr-qc
  - /home/initial/projects/archives/dev/unnamed-archive/fr-qc/archives
  - /home/initial/projects/archives/dev/unnamed-archive/fr-qc/areas
  - /home/initial/projects/archives/dev/unnamed-archive/fr-qc/projects
  - /home/initial/projects/archives/dev/unnamed-archive/fr-qc/resources
[sat-tree] Missing directories:
  - /home/initial/projects/archives/dev/unnamed-archive/en-ca/archives
  - /home/initial/projects/archives/dev/unnamed-archive/en-ca/areas
  - /home/initial/projects/archives/dev/unnamed-archive/en-ca/projects
  - /home/initial/projects/archives/dev/unnamed-archive/en-ca/resources
  - /home/initial/projects/archives/dev/unnamed-archive/fr-qc/archives
  - /home/initial/projects/archives/dev/unnamed-archive/fr-qc/areas
  - /home/initial/projects/archives/dev/unnamed-archive/fr-qc/projects
  - /home/initial/projects/archives/dev/unnamed-archive/fr-qc/resources
```

### # Create any missing dirs (e.g., after adding PARA)

```bash
./sat-tree --config ../unnamed-archive/config/archive.yml --create-missing
```

Output example:

```bash
[sat-tree] Created /home/initial/projects/archives/dev/unnamed-archive/en-ca/archives
[sat-tree] Created /home/initial/projects/archives/dev/unnamed-archive/en-ca/areas
[sat-tree] Created /home/initial/projects/archives/dev/unnamed-archive/en-ca/projects
[sat-tree] Created /home/initial/projects/archives/dev/unnamed-archive/en-ca/resources
[sat-tree] Created /home/initial/projects/archives/dev/unnamed-archive/fr-qc/archives
[sat-tree] Created /home/initial/projects/archives/dev/unnamed-archive/fr-qc/areas
[sat-tree] Created /home/initial/projects/archives/dev/unnamed-archive/fr-qc/projects
[sat-tree] Created /home/initial/projects/archives/dev/unnamed-archive/fr-qc/resources
```

Right now this will:

- Show you the expected root, language dirs, and PARA dirs (if `para_roots` are present in config).
- Create missing dirs if you ask it to, but never delete anything.

When you’re ready, we can evolve `sat-tree` to:

- Flag *extra* directories that don’t match the config
- Print a prettier “tree” view
- Go deeper than language/PARA (later taxonomy levels)
- Work as a migration tool when PARA or language roots change.