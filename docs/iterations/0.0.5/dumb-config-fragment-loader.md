---
Title: "Designing a Dumb but Future-Proof Configuration System for SAT: Factorized Structure, Plugin Discovery, and Early Archive Layout Logic"
Description: "A clear guide explaining how to implement the first, intentionally simple version of SAT’s configuration generation system using plugin-based discovery, factorized structure descriptions, and deferring directory expansion to sat-init-archive."
Author: "Christopher Steel"
Date: "2025-11-28"
Last_Modified_Date: "2025-11-28"
License: "CC BY-SA 4.0"
Version: "1.0.0"
Tags:
  - "sat"
  - "source-archive-tools"
  - "configuration"
  - "plugin-system"
  - "archive-initialization"
Keywords:
  - "sat-build-config"
  - "plugins"
  - "defaults"
  - "taxonomy"
  - "language-roots"
URL: "https://universalcake.com/areas/projects/source-archive-tools/configuration/dumb-config-fragment-loader"
Path: "areas/projects/source-archive-tools/configuration/dumb-config-fragment-loader.md"
Canonical: "https://universalcake.com/areas/projects/source-archive-tools/configuration/dumb-config-fragment-loader"
Sitemap: "true"
DC_Title: "Designing a Dumb but Future-Proof Configuration System for SAT"
DC_Creator: "Christopher Steel"
DC_Subject: "A technical explanation of SAT’s initial configuration discovery model using dumb plugin-based config fragments"
DC_Description: "This guide outlines how sat-build-config can assemble factorized structural elements from plugins, without computing directory trees, enabling future-proof extensibility."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
Robots: "index, follow"
OG_Title: "Designing a Dumb but Future-Proof Configuration System for SAT"
OG_Description: "How sat-build-config can gather structural config fragments from plugins while staying simple and extensible."
OG_URL: "https://universalcake.com/areas/projects/source-archive-tools/configuration/dumb-config-fragment-loader"
Schema:
  "@context": "https://schema.org"
  "@type": "TechArticle"
  "headline": "Designing a Dumb but Future-Proof Configuration System for SAT"
  "contributor": "ChatGPT-5 (OpenAI)"
  "about": "SAT configuration design, plugin discovery, structural metadata"
Video_Metadata: ""
---

# Designing a Dumb but Future-Proof Configuration System for SAT

The initial version of SAT’s configuration system does not need to understand the complete structure of an archive. Instead, the simplest and most robust design is to keep two responsibilities cleanly separated:

1. **Describing structure** in the configuration  
2. **Expanding that structure** into actual filesystem directories (handled by another tool such as `sat-init-archive`)

SAT’s configuration generator (`sat-build-config`) should handle only the first part.

---

## Principle for the Dumb Version

The **dumb** version of `sat-build-config` should:

- **Not** compute directory trees.
- Simply assemble a **factorized set of structure descriptions**, including:
  - `archive_root` (via archive-identity or CLI)
  - `language_roots` (via the language plugin)
  - `para_roots` or future `taxonomy_roots` (via a taxonomy or PARA plugin)

A later tool (e.g., `sat-init-archive`) will use this information to build the full directory tree:

> For each language_root × each taxonomy_root → create directories.

This keeps the configuration simple, composable, and predictable.

---

## Dumb Plugin Discovery for Config Fragments

To keep `sat-build-config` generic, it should discover plugins by finding any plugin containing a file at:

```
etc/defaults.yml
```

This marks a plugin as a **config-contributing plugin**.

Example plugins:

- `plugins/core/schema/etc/defaults.yml`
- `plugins/core/language/etc/defaults.yml`
- `plugins/core/para/etc/defaults.yml`
- `plugins/metadata/some-plugin/etc/defaults.yml`

### Structure of `defaults.yml`

All config-contributing plugins follow the same structure:

```yaml
version: "0.1.0"

plugin:
  id: "core.schema"

defaults:
  config_fragments:
    schema_version: "1.0.0"
```

### Pseudo-code for the Dumb Loader

```python
from pathlib import Path
import yaml

def load_all_plugin_config_fragments(plugins_root: Path) -> dict:
    config = {}

    # 1. Collect all defaults.yml paths
    defaults_files = sorted(plugins_root.glob("**/etc/defaults.yml"))

    # Optional: ensure core plugins first by simple path-based rule
    core_files = [p for p in defaults_files if "/core/" in str(p)]
    other_files = [p for p in defaults_files if "/core/" not in str(p)]
    ordered_files = core_files + other_files

    for defaults_file in ordered_files:
        data = yaml.safe_load(defaults_file.read_text()) or {}
        fragments = (
            data.get("defaults", {})
                .get("config_fragments", {})
            or {}
        )

        config = deep_merge(config, fragments)

    return config
```

Now main config assembly becomes:

```python
config = {}
config.update(load_all_plugin_config_fragments(Path("plugins")))
# then apply archive-local overrides, CLI parameters, etc.
```

This keeps `sat-build-config` fully decoupled from specific plugin types.

---

## Dumb Language Plugin: Describing the Language Dimension

### Create it

```bash
nano plugins/core/language/etc/defaults.yml
```



Example `plugins/core/language/etc/defaults.yml`:

###

```yaml
version: "0.1.0"

plugin:
  id: "core.language"

defaults:
  config_fragments:
    language_roots:
      - slug: "en-ca"
        bcp_47_tag: "en-CA"
        canonical: true
      - slug: "fr-qc"
        bcp_47_tag: "fr-CA"
        canonical: false
```

After plugin discovery and merging:

```yaml
schema_version: "1.0.0"
language_roots:
  - slug: "en-ca"
    bcp_47_tag: "en-CA"
    canonical: true
  - slug: "fr-qc"
    bcp_47_tag: "fr-CA"
    canonical: false
archive_identity:
  id: "unnamed-archive"
  label: "SAT Test Archive"
  description: "A SAT archive initialized with default testing configuration."
  archive_root: "../unnamed-archive"
```

This describes the **language dimension** without defining directory trees.

---

## Handling PARA / Taxonomy (Still Dumb)

The apparent complexity of language × taxonomy directory trees belongs in the expansion step, not the configuration generator.

Therefore, taxonomy plugins should also produce **factorized** configuration only.

Example `plugins/core/para/etc/defaults.yml`:

```yaml
version: "0.1.0"

plugin:
  id: "core.para"

defaults:
  config_fragments:
    para_roots:
      - id: "projects"
        slug: "projects"
        label: "Projects"
      - id: "areas"
        slug: "areas"
        label: "Areas"
      - id: "resources"
        slug: "resources"
        label: "Resources"
      - id: "archives"
        slug: "archives"
        label: "Archives"
```

Now the combined dumb config contains:

```yaml
archive_identity:
  archive_root: "../unnamed-archive"

language_roots:
  - slug: "en-ca"
    bcp_47_tag: "en-CA"
    canonical: true
  - slug: "fr-qc"
    bcp_47_tag: "fr-CA"
    canonical: false

para_roots:
  - id: "projects"
    slug: "projects"
    label: "Projects"
  - id: "areas"
    slug: "areas"
    label: "Areas"
  - id: "resources"
    slug: "resources"
    label: "Resources"
  - id: "archives"
    slug: "archives"
    label: "Archives"
```

This structure can now be expanded by:

```python
for lang in config["language_roots"]:
    for para in config["para_roots"]:
        create_dir(archive_root / lang["slug"] / para["slug"])
```

`sat-build-config` never needs to handle this.

---

## Why This Approach Scales

When SAT eventually includes:

- nested taxonomies
- language-specific overrides
- shared global directories
- metadata structure stacks

the configuration remains **factorized**:

- `language_roots` = language dimension  
- `para_roots` = taxonomy dimension  
- `archive_identity` = what archive this is  
- future sections = new dimensions  

The expansion step always builds the cross-product tree.

SAT does not need to encode the full filesystem in configuration.

---

## License

This document, *Designing a Dumb but Future-Proof Configuration System for SAT*, by **Christopher Steel**, with AI assistance from **ChatGPT-5 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)