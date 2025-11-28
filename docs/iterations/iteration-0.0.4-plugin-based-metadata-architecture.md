---
Title: "Iteration 0.0.4 Plan: Plugin-Based Metadata Architecture for source-archive-tools"
Description: "A focused iteration plan for version 0.0.4 of source-archive-tools, defining a clean plugin-based architecture and implementing the first metadata plugin for Dublin Core."
Author: "Christopher Steel"
Date: "2025-11-27"
Last_Modified_Date: "2025-11-27"
License: "CC BY-SA 4.0"
Version: "0.0.4"
Tags:
- "source-archive-tools"
- "iteration-plan"
- "plugins"
- "metadata"
- "dublin-core"
Keywords:
- "iteration"
- "plugin-architecture"
- "dublin-core"
- "metadata"
- "repository-structure"
URL: "https://github.com/steelcj/source-archives-blob/main/docs/iterations/iteration-0.0.4-plugin-based-metadata-architecture.md"
Path: "docs/iterations/iteration-0.0.4-plugin-based-metadata-architecture.md"
Canonical: "https://github.com/steelcj/source-archives-blob/main/docs/iterations/iteration-0.0.4-plugin-based-metadata-architecture.md"
Sitemap: "false"
DC_Title: "Iteration 0.0.4 Plan: Plugin-Based Metadata Architecture for source-archive-tools"
DC_Creator: "Christopher Steel"
DC_Subject: "Iteration plan for establishing a plugin-based metadata architecture in the source-archive-tools repository, starting with a Dublin Core plugin."
DC_Description: "This document defines the goals, scope, directory structure, plugin architecture, and tasks for iteration 0.0.4 of source-archive-tools, focusing on a plugin-based metadata system and the first Dublin Core plugin."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
DC_Contributor: "ChatGPT-5 (OpenAI)"
DC_RightsHolder: "Christopher Steel"
OG_Title: "Iteration 0.0.4 Plan: Plugin-Based Metadata Architecture for source-archive-tools"
OG_Description: "A focused plan for implementing a plugin-based metadata architecture in source-archive-tools, beginning with a Dublin Core metadata plugin."
OG_URL: "https://github.com/steelcj/source-archives-blob/main/docs/iterations/iteration-0.0.4-plugin-based-metadata-architecture.md"
OG_Image: ""
Schema:
"@context": "https://schema.org"
"@type": "TechArticle"
"headline": "Iteration 0.0.4 Plan: Plugin-Based Metadata Architecture for source-archive-tools"
"author": "Christopher Steel"
"inLanguage": "en"
"license": "https://creativecommons.org/licenses/by-sa/4.0/"
"contributor": "ChatGPT-5 (OpenAI)"
Video_Metadata: ""
---

# Iteration 0.0.4 Plan: Plugin-Based Metadata Architecture for source-archive-tools

This document defines the plan for **iteration 0.0.4** of the `source-archive-tools` project.

The previous architecture has been archived into `artifacts/`, and the repository root is now a clean slate. Iteration 0.0.4 establishes a **plugin-based architecture** and implements the first **metadata plugin** for **Dublin Core**.

The emphasis is on a **single, working plugin path** rather than a full ecosystem. Future iterations can clone and extend this pattern.

# 0. Iteration Goal

Create a minimal but complete **plugin-based metadata architecture** for `source-archive-tools`, and implement a fully working **Dublin Core metadata plugin** that can be invoked via a CLI tool.

At the end of iteration 0.0.4, you should be able to:

- install or use the repository
- call a CLI entrypoint
- have it load the Dublin Core plugin
- read a test Markdown file with YAML metadata
- apply Dublin Core defaults/validation
- write back the updated metadata (or show a preview)

This iteration is intentionally narrow and foundational.

# 1. Target Repository Layout for 0.0.4

For iteration 0.0.4, the top-level structure will follow **Option A**:

```text
tools/
  core/
  plugins/
  cli/
  docs/
  artifacts/
  VERSION
```

The `artifacts/` directory preserves previous iterations and legacy content.
The new architecture will live under your `source-archive-tools` repository.

Nice. Direct and clean.

Next step: create the **Dublin Core plugin manifest**.

### Create `plugin.yml` for `metadata.dublin-core`

Create directories:

```bash
mkdir -p plugins/metadata/dublin-core/{standard,config}
```

Content: 

```bash
cat > plugins/metadata/dublin-core/plugin.yml << 'EOF'
id: "metadata.dublin-core"
name: "Dublin Core Metadata Plugin"
version: "0.0.1"

type: "metadata"

entrypoints:
apply:
run: "plugin.py"
callable: "apply_metadata"

paths:
standard: "standard"
config: "config"
EOF
```

When that’s done, you can check it with:

```bash
cat plugins/metadata/dublin-core/plugin.yml
```

## Create the plugin implementation stub.

### Create `plugin.py` for `metadata.dublin-core`

```bash
cat > plugins/metadata/dublin-core/plugin.py << 'EOF'
from pathlib import Path
from typing import Dict, Any


PLUGIN_ID = "metadata.dublin-core"


def apply_metadata(doc_metadata: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
"""
Apply Dublin Core defaults and normalization to a document metadata dict.

:param doc_metadata: Existing document metadata (from YAML front matter).
:param config: Dublin Core plugin configuration (e.g., required fields, defaults).
:return: Updated metadata dict with Dublin Core fields applied.
"""
result = dict(doc_metadata) if doc_metadata is not None else {}

fields_cfg = config.get("fields", {}) if config else {}

for field_name, field_spec in fields_cfg.items():
default = field_spec.get("default")
required = field_spec.get("required", False)

if field_name not in result or result.get(field_name) in (None, "", []):
if default is not None:
result[field_name] = default
elif required and field_name not in result:
# Leave a placeholder for required-but-missing fields
result[field_name] = "__REQUIRED_FIELD_MISSING__"

return result
EOF
```

When done:

```bash
chmod +x plugins/metadata/dublin-core/plugin.py
```

## Create the Dublin Core config.

### Create `config/defaults.yml`

```bash
cat > plugins/metadata/dublin-core/config/defaults.yml << 'EOF'
fields:
DC_Title:
required: true

DC_Creator:
required: true
default: "Christopher Steel"

DC_Language:
required: true
default: "en"

DC_License:
required: true
default: "https://creativecommons.org/licenses/by-sa/4.0/"

DC_Contributor:
required: false
default: "ChatGPT-5 (OpenAI)"
EOF
```

Confirm:

```bash
cat plugins/metadata/dublin-core/config/defaults.yml
```



```bash
mkdir -p cli
```

## Create core directory

`core` will contain shared building blocks that plugins and CLI tools depend on, but **no project-specific behavior**.

Create structure:

```bash
mkdir -p core
```

### Create the core plugin loader

This is required before the CLI can call the plugin.

Create the plugin loader

```bash
cat > core/plugin_loader.py << 'EOF'
import yaml
from pathlib import Path
from importlib import import_module


PLUGIN_ROOT = Path("plugins")


def load_plugin(plugin_id: str):
"""
Load a plugin by its ID, e.g., "metadata.dublin-core".
Returns a dict with:
- manifest (plugin.yml contents)
- module (imported plugin.py)
"""
parts = plugin_id.split(".")
plugin_path = PLUGIN_ROOT.joinpath(*parts)

manifest_file = plugin_path / "plugin.yml"
if not manifest_file.exists():
raise FileNotFoundError(f"Plugin manifest not found: {manifest_file}")

with manifest_file.open("r") as f:
manifest = yaml.safe_load(f)

entry = manifest["entrypoints"]["apply"]
module_path = plugin_path / entry["run"]

# Convert path to importable module string
module_import = (
"tools.plugins."
+ ".".join(parts)
+ "."
+ entry["run"].replace(".py", "")
)

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

with config_path.open("r") as f:
return yaml.safe_load(f)
EOF
```

confirm:

```bash
cat core/plugin_loader.py
```

### Make core package importable

Create `core/__init__.py`:

```bash
touch core/__init__.py
```

### Create plugin package folders:

```bash
touch plugins/__init__.py
touch plugins/metadata/__init__.py
touch plugins/metadata/dublin-core/__init__.py
```

This ensures Python can import everything.

## Create our CLI tool sat-apply-metadata

```bash
cat > cli/sat-apply-metadata << 'EOF'
#!/usr/bin/env python3
import sys
from pathlib import Path
import yaml

# Allow imports from repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.core.plugin_loader import load_plugin, load_plugin_config# type: ignore


def load_front_matter(path: Path):
text = path.read_text(encoding="utf-8")
if not text.startswith("---"):
return {}, text

parts = text.split("---", 2)
if len(parts) < 3:
return {}, text

_, yaml_block, rest = parts
metadata = yaml.safe_load(yaml_block) or {}
content = rest.lstrip("\n")
return metadata, content


def write_front_matter(path: Path, metadata, content: str):
yaml_block = yaml.safe_dump(metadata, sort_keys=False).strip()
text = f"---\n{yaml_block}\n---\n\n{content}"
path.write_text(text, encoding="utf-8")


def main():
if len(sys.argv) < 2:
print("Usage: sat-apply-metadata <path> [--plugin <plugin-id>]")
sys.exit(1)

target = Path(sys.argv[1])
plugin_id = "metadata.dublin-core"

if "--plugin" in sys.argv:
idx = sys.argv.index("--plugin")
if idx + 1 < len(sys.argv):
plugin_id = sys.argv[idx + 1]

if not target.exists():
print(f"Error: {target} does not exist")
sys.exit(1)

plugin_info = load_plugin(plugin_id)
config = load_plugin_config(plugin_info)
apply_fn = plugin_info["callable"]

metadata, content = load_front_matter(target)
updated = apply_fn(metadata, config)

write_front_matter(target, updated, content)

print(f"Metadata updated using plugin {plugin_id} for {target}")


if __name__ == "__main__":
main()
EOF
```

Confirm:

```bash
cat cli/sat-apply-metadata
```

Make executable:

```bash
chmod +x cli/sat-apply-metadata
```

### Quick test from repo root

```bash
chmod +x cli/sat-apply-metadata
```

# Began creating plugin metadata/dublin-core testing and examples here




Planned files:

```text
core/
__init__.py
plugin_base.py# base classes / interfaces for plugins
plugin_loader.py# discovers and loads plugins
metadata_types.py # (optional) shared metadata structures
```



Initial scope for iteration 0.0.4:

- `plugin_base.py`
- `plugin_loader.py`
- `__init__.py`

## 1.2 plugins

`plugins` contains all plugin implementations, organized by type and name.

For this iteration:

```text
plugins/
metadata/
dublin-core/
standard/
config/
plugin.py
plugin.yml
README.md# optional but recommended
```

The **Dublin Core** plugin will be the first and only plugin in this iteration.

## 1.3 cli

`cli` contains entrypoints that users can run.

For this iteration:

```text
cli/
sat-apply-metadata
```

Note: `sat` refers to **Source Archive Tools**

This may be:

- a Python script (with a shebang), or
- a thin wrapper that calls a Python module (preferred long-term)

The CLI will accept:

- a path to a file or directory
- optional arguments such as `--plugin dublin-core`
- and will internally use `core.plugin_loader` to load and run the plugin.

# 2. Plugin Architecture Requirements

This iteration defines the **minimal plugin contract** for metadata plugins.

## 2.1 Directory structure for a metadata plugin

Each metadata plugin (e.g., Dublin Core) follows:

```text
plugins/metadata/<plugin-id>/
standard/
config/
plugin.py
plugin.yml
README.md # optional
```

For Dublin Core:

```text
plugins/metadata/dublin-core/
standard/
dublin-core-standard.md# human-readable summary (optional)
dublin-core-fields.yml # machine-readable field list (optional)
config/
defaults.yml # default values and mappings
plugin.py# implementation
plugin.yml # manifest describing the plugin
README.md# short description and usage notes
```

## 2.2 plugin.yml (plugin manifest)

The `plugin.yml` file declares the plugin in a way the loader can understand.

Minimal example:

```yaml
id: "metadata.dublin-core"
name: "Dublin Core Metadata Plugin"
version: "0.0.1"

type: "metadata"

entrypoints:
apply:
run: "plugin.py"
callable: "apply_metadata"

paths:
standard: "standard"
config: "config"
```

The goal for 0.0.4 is to define a **simple, readable manifest** that `plugin_loader.py` can parse and act on.

## 2.3 plugin.py (implementation)

`plugin.py` must expose at least one callable with a predictable signature, for example:

```python
def apply_metadata(doc_metadata: dict, config: dict) -> dict:
"""
Takes existing document metadata (YAML as dict) and a plugin config dict.
Returns updated metadata dict with Dublin Core fields applied/normalized.
"""
```

Iteration 0.0.4 will define:

- the function name (e.g., `apply_metadata`)
- the expected arguments
- the return value format

# 3. Dublin Core Plugin Scope (0.0.4)

The Dublin Core plugin is the **reference implementation** for metadata plugins in this project.

## 3.1 Responsibilities

For this iteration, the Dublin Core plugin will:

- accept an existing metadata dict (from YAML)
- ensure that core Dublin Core fields exist
- apply reasonable defaults when values are missing (where safe)
- normalize field names (e.g., `DC_Title`, `DC_Creator`, `DC_Subject`, etc.)
- return an updated metadata dict suitable for writing back into the document

It does **not** need to:

- validate every possible DC variant
- support multiple languages
- handle complex inheritance or layering
- integrate with APA7 or CAP

Those will be later iterations.

## 3.2 Inputs and outputs

**Input:**

- A Python `dict` representing YAML metadata for a document.
- A configuration dict loaded from `config/defaults.yml`.

**Output:**

- A Python `dict` representing updated metadata, with a coherent set of Dublin Core fields.

## 3.3 Minimal config/defaults.yml

Example structure:

```yaml
fields:
DC_Title:
required: true
DC_Creator:
required: true
default: "Christopher Steel"
DC_Language:
required: true
default: "en"
DC_License:
required: true
default: "https://creativecommons.org/licenses/by-sa/4.0/"
```

Iteration 0.0.4 will define the specific fields and defaults to be supported initially.

# 4. Core Module Responsibilities (core)

## 4.1 plugin_base.py

`plugin_base.py` will define one or more base classes or interfaces, for example:

- `BasePlugin`
- `MetadataPlugin(BasePlugin)`

Goals for this iteration:

- provide a minimal base class that Dublin Core can inherit from
- define attributes like `id`, `name`, `version`, `type`
- provide a simple logging or error interface (even if minimal)

## 4.2 plugin_loader.py

`plugin_loader.py` is responsible for:

- discovering plugins under `plugins/`
- reading their `plugin.yml` files
- instantiating plugin classes or loading callables
- providing a simple API, for example:

```python
from tools.core.plugin_loader import load_plugin

plugin = load_plugin("metadata.dublin-core")
updated_metadata = plugin.apply_metadata(doc_metadata, config)
```

Iteration 0.0.4 requirements:

- load **one** plugin reliably (Dublin Core)
- handle missing plugins with a clear error
- read basic fields from `plugin.yml`

# 5. CLI Tool: sat-apply-metadata

## 5.1 Purpose

The CLI is the human entrypoint for the plugin system.
For iteration 0.0.4, it only needs to:

- take an input file path
- optionally accept a `--plugin` argument (default: `metadata.dublin-core`)
- load the plugin using `plugin_loader`
- read YAML metadata from the input file
- pass the metadata to the plugin
- print or write the updated metadata

## 5.2 Basic usage (target behavior)

Example:

```bash
cli/sat-apply-metadata --plugin metadata.dublin-core docs/example.md
```

Expected behavior (for this iteration):

- reads `docs/example.md`
- parses YAML front matter
- applies Dublin Core rules
- prints the updated metadata to stdout, or writes back to the file (behavior is to be decided in this iteration)

# 6. Out of Scope for Iteration 0.0.4

To keep the iteration focused and achievable, the following items are explicitly **out of scope**:

- APA7 plugin
- CAP plugin
- Schema.org metadata plugin
- taxonomy plugins (e.g., PARA)
- archive creation or initialization tools
- generators (e.g., radial wheels)
- multi-language support for metadata
- integration with external systems (MkDocs, Plone, etc.)
- advanced configuration hierarchies and layering

These will be addressed in follow-up iterations once the core plugin path is stable.

# 7. Definition of Done for Iteration 0.0.4

Iteration 0.0.4 is considered complete when:

- `core/plugin_base.py` and `core/plugin_loader.py` exist and are usable.
- `plugins/metadata/dublin-core/` exists with:
- `plugin.yml`
- `plugin.py`
- `config/defaults.yml`
- (optionally) a minimal `standard/` reference
- a CLI script `cli/sat-apply-metadata` exists and can:
- accept a file path
- load the Dublin Core plugin via the loader
- read metadata from a test document
- apply the plugin
- output updated metadata (stdout or in-place update)
- at least one test document (for example under `docs/examples/`) demonstrates the end-to-end behavior.
- this iteration plan is stored in the repository at:

```text
docs/iterations/iteration-0.0.4-plugin-based-metadata-architecture.md
```

and reflects the implemented reality.

## License

This document, *Iteration 0.0.4 Plan: Plugin-Based Metadata Architecture for source-archive-tools*, by **Christopher Steel**, with AI assistance from **ChatGPT-5 (OpenAI)**, is licensed under the Creative Commons Attribution-ShareAlike 4.0 License.

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
