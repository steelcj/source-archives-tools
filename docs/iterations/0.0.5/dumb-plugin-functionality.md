# dumb-plugin-functionality

## Principle for the dumb version

For now:

- `sat-build-config` **does not compute the full directory tree**.
- It just **assembles simple, factorized config pieces**:
  - `archive_root` (from archive-identity / CLI)
  - `language_roots` (from core.language)
  - `para_roots` or `taxonomy_roots` (from a future PARA/taxonomy plugin)

Then **something else** (e.g. `sat-init-archive`) will do:

> For each language_root × each taxonomy_root → create directories.

That keeps `sat-build-config` “dumb” but very useful.

------

## 2. Dumb plugin discovery for config fragments

First, let’s teach `sat-build-config` to discover *any* plugin that ships `etc/defaults.yml` with `config_fragments`.

### Filesystem convention

Any directory under `plugins/**` that has:

```text
etc/defaults.yml
```

is considered a “config-contributing plugin”.

Example:

- `plugins/core/schema/etc/defaults.yml`
- `plugins/core/language/etc/defaults.yml`
- (later) `plugins/core/para/etc/defaults.yml`
- (later) `plugins/metadata/some-plugin/etc/defaults.yml`

### Shape of `defaults.yml`

We already have this pattern:

```yaml
version: "0.1.0"

plugin:
  id: "core.schema"

defaults:
  config_fragments:
    schema_version: "1.0.0"
```

We’ll reuse it.

### Pseudo-code for the dumb loader

In `sat-build-config`:

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

        config = deep_merge(config, fragments)  # your existing merge strategy

    return config
```

Now `sat-build-config` can do:

```python
config = {}
config.update(load_all_plugin_config_fragments(Path("plugins")))
# then apply archive overrides, CLI params, etc.
```

No knowledge of “language”, “schema”, or “taxonomy” baked in.

------

## Dumb language plugin

### just describe the languages

#### Create structure

```bash
mkdir -p plugins/language/etc
```

#### Create defaults.yml

```bash
nano plugins/language/etc/defaults.yml
```

#### Add the content

For `plugins/core/language/etc/defaults.yml`:

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
#      - slug: "fr-qc"
#        bcp_47_tag: "fr-CA"
#        canonical: false
```

### Test language

```bash
./sat-build-config
```



After plugin discovery and merge, your config (simplified) might look like:

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

Notice: we didn’t try to say anything yet about `en-ca/projects`, `fr-qc/areas`, etc. We just described the *language dimension*.

------

## 4. How to handle PARA / taxonomy (still dumb)

You’re right: it *feels* tricky when you start thinking:

- `root/`
  - `en-ca/`
    - `projects/`
    - `areas/`
    - `resources/`
    - `archives/`
  - `fr-qc/`
    - `projects/`
    - `areas/`
    - `resources/`
    - `archives/`

But that complexity belongs in the *expansion step* (e.g. `sat-init-archive`), not in the dumb config generator.

So for taxonomy/PARA, we do the same trick:
 **just describe the taxonomy roots, factorized and language-agnostic.**

Example: `plugins/core/para/etc/defaults.yml`:

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

Now the *dumb* final config from `sat-build-config` has three main pieces:

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

Still very dumb, but *complete enough* that another tool can do:

```python
for lang in config["language_roots"]:
    for para in config["para_roots"]:
        create_dir(
            archive_root / lang["slug"] / para["slug"]
        )
```

So we’ve cleanly separated:

- **sat-build-config** → produce a *factored* description of structure.
- **sat-init-archive / other tools** → expand those factors into actual directories.

------

## 5. Why this helps when things get more complex later

When you eventually layer on:

- nested taxonomies
- language-specific overrides (e.g. para labels differing in each language)
- special cases like `global/` resources

your config can still stay factorized:

- `language_roots` stays about languages
- `para_roots` stays about PARA
- maybe later `special_roots`, `global_roots`, etc.

You don’t have to ever encode the full cross-product tree in config; that’s always computed by whatever tool needs it.

------

If you’re good with this direction, the very next small step is:

1. Implement `load_all_plugin_config_fragments(...)` in `sat-build-config` (dumb discovery).
2. Add `plugins/core/language/etc/defaults.yml` as above.
3. Optionally add `plugins/core/para/etc/defaults.yml` so we have both dimensions in config.

We can sketch those concrete `defaults.yml` files and the merge function in more detail next if you’d like.