#  para-taxonomy-plugin-translations

Yeah, this is a *fantastic* moment to introduce PARA translations.

- You’ve just stabilized `language_roots`.
- `para_roots` isn’t “in the wild” yet.
- Nothing downstream depends on the PARA shape, so we can choose a clean, factorized design without breaking anyone.

I’d keep the **dimensions separate** (like we did for language vs PARA) and add a **translation map by language id**, instead of stuffing everything into `para_roots`.

## Keep `para_roots` language-agnostic

Stick with the simple, structural definition:

```yaml
para_roots:
  - id: "projects"
    slug: "projects"
    label: "Projects" # optional: canonical label (e.g., en-ca)
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

Here:

- `id` = stable internal key (used in translations)
- `slug` = directory name (`<lang>/<slug>/`)
- `label` = canonical label (e.g., `en-ca`); nice for tooling that doesn’t care about i18n

## Add a separate `para_labels` translation map

Then add a **separate** config fragment that maps:

- `language_roots[].id` → language code (e.g., `en-ca`, `fr-qc`)
- `para_roots[].id` → translated label

Example inside `tools/plugins/taxonomy/para/etc/defaults.yml`:

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

    para_labels:
      en-ca:
        projects: "Projects"
        areas: "Areas"
        resources: "Resources"
        archives: "Archives"
      fr-qc:
        projects: "Projets"
        areas: "Domaines"
        resources: "Ressources"
        archives: "Archives"
```

This plays really nicely with your existing config:

- `language_roots[].id` → `en-ca` / `fr-qc`
- `para_roots[].id` → `projects` / `areas` / `resources` / `archives`
- `para_labels[language_id][para_id]` → label

No changes needed in `sat-build-config` or `sat-init-archive` — they already just merge whatever `config_fragments` the plugin provides.

## How consumers would use it later

Any consumer (MkDocs nav plugin, UI, docs generator) can now do:

```python
lang_id = "fr-qc"
para_id = "projects"
label = config["para_labels"][lang_id][para_id]
```

while still using:

```python
para_slug = next(p["slug"] for p in config["para_roots"] if p["id"] == para_id)
path = archive_root / lang_slug / para_slug
```

So:

- Structure comes from `para_roots` + `language_roots`
- UI strings come from `para_labels`

Very SAT-ish: dimensions are separate, cross-products are computed by tools.

## What I’d actually change right now

Just this:

1. Update `tools/plugins/taxonomy/para/etc/defaults.yml` to:

   - keep `para_roots` as above
   - add `para_labels` block like above

2. Re-run:

   ```bash
   ./sat-build-config
   ```

   And confirm you see:

   ```yaml
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
   para_labels:
     en-ca:
       projects: Projects
       areas: Areas
       resources: Resources
       archives: Archives
     fr-qc:
       projects: Projets
       areas: Domaines
       resources: Ressources
       archives: Archives
   ```

No need to touch `sat-init-archive` yet; translations are for navigation, UI, and docs, not for directory creation.

If you’d like, next we can sketch how a MkDocs nav generator (or SAT doc tool) would use `language_roots + para_roots + para_labels` to build localized nav trees.