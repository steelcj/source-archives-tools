# PARA Taxonomy Plugin (taxonomy.para)

This document describes the initial implementation of the **PARA Taxonomy Plugin** for `source-archive-tools`. The plugin is responsible for applying the PARA directory structure beneath each locale root of a source archive.

The plugin is designed to be:

- **Declarative:** Reads YAML taxonomy definitions (either archive-local or plugin defaults).
- **Extensible:** Multiple taxonomies may coexist (e.g., PARA, civic-lattice).
- **Plugin-based:** Uses a consistent directory and manifest structure.
- **Archive-agnostic:** No dependency on MkDocs, Plone, or any static-site generator.

The implementation includes:

- Directory structure
- `plugin.yml` (manifest)
- `config/default.yml` (PARA mapping)
- `standard/para-notes.md`
- Working `plugin.py`

---

## Directory Structure

```
tools/
  plugins/
    taxonomy/
      para/
        docs/
          para-taxonomy-plugin-creation.md
        standard/
          para-notes.md
        config/
          default.yml
        plugin.py
        plugin.yml
```

## plugin.yml

Create P.A.R.A taxonomy plugin.yml manifest

```bashnano 
nano plugins/taxonomy/para/plugin.yml
```

Content:

```yaml
id: "taxonomy.para"
version: "0.1.0"
kind: "taxonomy"
entry_point: "tools.plugins.taxonomy.para.plugin:apply_taxonomy"
standard_dir: "standard"
config_dir: "config"
```

This manifest declares:

- The plugin’s identity (`taxonomy.para`)
- Its type (`taxonomy`)
- Where its executable logic lives
- How to find its standard definitions and local config

## config/default.yml

Create config/default.yml

```bash
nano plugins/taxonomy/para/config/default.yml
```

Content example:

```yaml
version: "0.1.0"
taxonomy_id: "para"

apply_mode: "under_locale_roots"

buckets:
  - id: "projects"
    path: "projects"
    subdirs:
      - "design"
      - "research"
      - "implementation"
      - "outputs"
      - "archive"

  - id: "areas"
    path: "areas"
    subdirs:
      - "content"
      - "creation"
      - "infra"
      - "sys"
      - "hw"
      - "well-being"
      - "graphics"
      - "governance"

  - id: "resources"
    path: "resources"
    subdirs:
      - "people"
      - "tools"
      - "templates"
      - "citations"
      - "brand"
      - "images"
      - "datasets"

  - id: "archives"
    path: "archives"
    subdirs:
      - "drafts"
      - "deprecated"
      - "snapshots"
      - "translations"
```

This file contains the plugin-level PARA definition. Archive-local definitions can override or extend this.

## standard/para-notes.md

```markdown
# PARA Taxonomy Notes

This directory contains conceptual notes and references for the PARA taxonomy.

- **Projects**: time-bound, outcome-oriented efforts  
- **Areas**: ongoing responsibilities and domains of attention  
- **Resources**: reference material and reusable assets  
- **Archives**: completed, inactive, or deprecated material  

The mapping of PARA concepts into concrete paths is defined in
`../config/default.yml`. Archive-local taxonomy files may extend or override these defaults.
```

## plugin.py

Create plugin.py

```bash
nano plugins/taxonomy/para/plugin.py
```

Content example:



```python
"""
taxonomy/para plugin.

Applies a PARA taxonomy under each locale root, based on a YAML config
(either archive-local or the plugin's own config/default.yml).

Expected context keys:
  - root_dir: str, path to the archive root
  - languages: list[dict], each with at least {"slug": "...", "bcp_47_tag": "..."}
  - dry_run: bool (optional), if True, only print actions
  - taxonomy_config_path: str (optional), path to archive-local taxonomy YAML
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required for taxonomy.para plugin.") from exc


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML at {path} must be a mapping.")
    return data


def _resolve_taxonomy_config(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Priority:
      1. context['taxonomy_config_path'] if provided
      2. plugin-level config/default.yml
    """
    root_dir = Path(context["root_dir"])
    plugin_dir = Path(__file__).resolve().parent

    # Archive-local override, if explicitly provided
    config_path_str: Optional[str] = context.get("taxonomy_config_path")
    if config_path_str:
        config_path = Path(config_path_str)
        if not config_path.is_absolute():
            config_path = root_dir / config_path
        if not config_path.is_file():
            raise FileNotFoundError(f"taxonomy_config_path not found: {config_path}")
        return _load_yaml(config_path)

    # Fallback to plugin config/default.yml
    default_path = plugin_dir / "config" / "default.yml"
    if not default_path.is_file():
        raise FileNotFoundError(f"PARA default taxonomy config not found at {default_path}")
    return _load_yaml(default_path)


def _ensure_dir(path: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"[PLAN] mkdir -p {path}")
        return
    path.mkdir(parents=True, exist_ok=True)
    print(f"[APPLY] ensured directory: {path}")


def apply_taxonomy(context: Dict[str, Any]) -> None:
    """
    Entry point for taxonomy.para plugin.

    Example context:
      {
        "root_dir": "/path/to/archive",
        "languages": [
          {"bcp_47_tag": "en-CA", "slug": "en-ca"},
          {"bcp_47_tag": "fr-CA", "slug": "fr-ca"},
        ],
        "dry_run": True,
        "taxonomy_config_path": "taxonomy/archive-taxonomy-para.yml",
      }
    """
    root_dir = Path(context["root_dir"]).resolve()
    dry_run: bool = bool(context.get("dry_run", False))

    languages: List[Dict[str, Any]] = context.get("languages", [])
    if not languages:
        raise ValueError("taxonomy.para: context['languages'] is required and must be non-empty.")

    taxonomy = _resolve_taxonomy_config(context)

    if taxonomy.get("taxonomy_id") != "para":
        raise ValueError(
            f"taxonomy.para: expected taxonomy_id 'para', got {taxonomy.get('taxonomy_id')!r}"
        )

    apply_mode = taxonomy.get("apply_mode", "under_locale_roots")
    if apply_mode != "under_locale_roots":
        raise ValueError(
            f"taxonomy.para: unsupported apply_mode {apply_mode!r} (expected 'under_locale_roots')."
        )

    buckets = taxonomy.get("buckets", [])
    if not isinstance(buckets, list) or not buckets:
        raise ValueError("taxonomy.para: taxonomy 'buckets' must be a non-empty list.")

    print(f"[taxonomy.para] root_dir={root_dir}")
    print(f"[taxonomy.para] dry_run={dry_run}")
    print(f"[taxonomy.para] languages={languages!r}")

    for lang in languages:
        slug = lang.get("slug")
        if not slug:
            raise ValueError(f"taxonomy.para: language entry missing 'slug': {lang!r}")

        locale_root = root_dir / slug
        _ensure_dir(locale_root, dry_run=dry_run)

        for bucket in buckets:
            bucket_path = bucket.get("path")
            if not bucket_path:
                raise ValueError(f"taxonomy.para: bucket missing 'path': {bucket!r}")

            bucket_root = locale_root / bucket_path
            _ensure_dir(bucket_root, dry_run=dry_run)

            subdirs = bucket.get("subdirs", [])
            if not isinstance(subdirs, list):
                raise ValueError(f"taxonomy.para: 'subdirs' must be a list in bucket {bucket!r}")

            for sub in subdirs:
                sub_root = bucket_root / sub
                _ensure_dir(sub_root, dry_run=dry_run)
```

---

## Next Optional Steps

If desired, I can now produce:

- A companion **archive-local taxonomy override file** (`taxonomy/archive-taxonomy-para.yml`)
- A working **CLI loader** (`tools/cli/sat-apply-taxonomy`) that:
  - Reads `config/languages.yml`
  - Reads `config/structure.yml`
  - Loads taxonomy plugin automatically
  - Calls `apply_taxonomy(context)`
- A README for the entire taxonomy plugin system

Just tell me what you want next.

