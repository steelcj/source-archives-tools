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
