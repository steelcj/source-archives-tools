# para-taxonomy-plugin

## Create the PARA taxonomy plugin skeleton

From your SAT root (where `tools/` lives):

```bash
mkdir -p plugins/taxonomy/para/{docs,etc,examples,templates,meta}
mkdir -p plugins/taxonomy/para/docs
mkdir -p plugins/taxonomy/para/etc
mkdir -p plugins/taxonomy/para/examples
mkdir -p plugins/taxonomy/para/templates
mkdir -p plugins/taxonomy/para/meta
```

Confirmation:

```bash
tree plugins/taxonomy/para
```

```bash
plugins/taxonomy/para
├── docs
├── etc
├── examples
├── meta
└── templates

6 directories, 0 files
```

You don’t *need* all those directories for the MVP, but it keeps the layout consistent with your “self-contained plugin bundle” idea.



## Add `etc/defaults.yml` for PARA roots

Create:

```bash
nano plugins/taxonomy/para/etc/defaults.yml
```

Content:

```yaml
version: "0.1.0"

plugin:
  id: "taxonomy.para"

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

Key points:

* `id` = stable internal identifier for the PARA root.
* `slug` = directory name (will be used later for `<lang>/<slug>/`).
* `label` = human-readable text (for docs, UIs, etc.).

Because `sat-build-config` already does:

```python
defaults_files = sorted(plugins_root.glob("**/etc/defaults.yml"))
...
fragments = data.get("defaults", {}).get("config_fragments", {}) or {}
config = deep_merge(config, fragments)
```

this plugin will be picked up automatically.

---

## 3. (Optional but nice) Add a plugin manifest

Create:

```bash
nano plugins/taxonomy/para/plugin.yml
```

Content:

```yaml
id: "taxonomy.para"
name: "PARA Taxonomy Plugin"
version: "0.1.0"

paths:
  docs: "./docs"
  examples: "./examples"
  templates: "./templates"
  metadata: "./meta"

defaults:
  etc: "./etc"
```

This isn’t required for config generation right now, but it future-proofs you for plugin discovery, docs, etc.

---

## 4. Check `sat-build-config` output

Now re-run:

```bash
./sat-build-config
```

You should see something like:

```yaml
schema_version: 1.0.0
archive_identity:
  id: unnamed-archive
  label: SAT Test Archive
  description: A SAT archive initialized with default testing configuration.
  archive_root: ../unnamed-archive
language_roots:
- id: en-ca
  slug: en-ca
  label: English (Canada)
  bcp_47_tag: en-CA
  canonical: true
- id: fr-qc
  slug: fr-qc
  label: Français (Québec)
  bcp_47_tag: fr-CA
  canonical: false
para_roots:
- id: projects
  slug: projects
  label: Projects
- id: areas
  slug: areas
  label: Areas
- id: resources
  slug: resources
  label: Resources
- id: archives
  slug: archives
  label: Archives
```

If `para_roots` appears at the bottom, you’re golden: the plugin is live.

---

## 5. Next tiny step (when you’re ready): teach `sat-init-archive` about PARA

You don’t have to do this immediately, but when you *are* ready, it’s just:

* read `para_roots` from the config
* for each `<language_root.slug> × <para_root.slug>` create a directory

Something like:

```python
def create_para_roots(root: Path, config: Dict[str, Any], dry_run: bool = False) -> None:
    para_roots = config.get("para_roots") or []
    language_roots = config.get("language_roots") or []

    if not isinstance(para_roots, list):
        print("[sat-init-archive] WARN: para_roots is not a list; skipping PARA directories.", file=sys.stderr)
        return
    if not isinstance(language_roots, list):
        print("[sat-init-archive] WARN: language_roots is not a list; skipping PARA directories.", file=sys.stderr)
        return

    for lang in language_roots:
        if not isinstance(lang, dict):
            continue
        lang_slug = lang.get("slug")
        if not lang_slug:
            continue

        lang_root = root / lang_slug

        for para in para_roots:
            if not isinstance(para, dict):
                continue
            para_slug = para.get("slug")
            if not para_slug:
                continue

            para_dir = lang_root / para_slug

            if dry_run:
                if para_dir.exists():
                    print(f"[sat-init-archive] DRY RUN: PARA dir already exists: {para_dir}", file=sys.stderr)
                else:
                    print(f"[sat-init-archive] DRY RUN: Would create PARA dir: {para_dir}", file=sys.stderr)
                continue

            try:
                para_dir.mkdir(parents=True, exist_ok=True)
                print(f"[sat-init-archive] Ensured PARA dir: {para_dir}", file=sys.stderr)
            except Exception as exc:
                print(f"[sat-init-archive] ERROR: Failed to create PARA dir {para_dir}: {exc}", file=sys.stderr)
                sys.exit(1)
```

…then call `create_para_roots(root, config, dry_run)` after `create_language_roots`.

But you can park that for later; right now, the only thing you *need* is the `plugins/taxonomy/para` plugin itself, and we just designed that.
