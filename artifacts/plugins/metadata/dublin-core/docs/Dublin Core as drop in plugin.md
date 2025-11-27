# Dublin Core as drop in plugin

Nice metaphor, and I think it maps really cleanly here.

Let me mirror your OS X–style “drop-in app bundle” onto a **single plugin-as-application** for **Dublin Core metadata**, and show:

- What the **plugin bundle** looks like inside `source-archive-tools` (SAT, the “OS”)
- What gets **installed into an archive** (the “desktop”)
- How it plays with the **bash tools you already have**



## Re-stating the metaphor in SAT terms

Your model:

- A plugin is like a **standalone app bundle**:
  - Contains everything it needs: code, defaults, templates, standards, tests, docs
  - The OS (SAT) only needs to know:
    - where it lives (path)
    - how to launch it (entrypoint / manifest)
- The archive is like a **desktop**, initially set up with:
  - sane defaults
  - a few apps already “installed” (copied in and ready)
  - space for the user to customize their environment over time

So in SAT:

- Plugins live under `plugins/`
- Each plugin is self-contained
- A `plugin.yml` at the root of the plugin is the “info.plist” / manifest

------

## 2. The Dublin Core plugin as an “app bundle” in SAT

Here’s one concrete layout for **Dublin Core** in `source-archive-tools`:

```text
source-archive-tools/
  plugins/
    metadata/
      dublin-core/
        plugin.yml
        bin/
          sat-dublin-core-validate      # CLI tool, uses this bundle
          sat-dublin-core-explain       # optional helper
        config/
          mapping.yml.example           # How DC_* maps to archive fields
          profiles.yml.example          # Optional: profiles or subsets
        standard/
          dcmi-terms.yml                # Canonical term list, IDs, notes
        templates/
          docs/
            dublin-core-metadata.md     # user-facing doc for archives
        lib/
          dublin_core_validator.py      # shared logic
          dublin_core_mapper.py
        tests/
          fixtures/
            sample-front-matter-1.yml
            sample-front-matter-2.yml
          scripts/
            run-validation-tests.sh
```

### What each part is for

- `plugin.yml`
   The manifest; tells SAT and archives how to install and run this plugin.
- `bin/`
   Executable entrypoints that user runs, e.g.:
  - `sat-dublin-core-validate` – checks that metadata in `.md` front matter respects DC expectations
  - `sat-dublin-core-explain` – optionally dumps a human-readable explanation of fields
- `config/`
   Archive-facing configuration:
  - `mapping.yml.example` – how your internal keys (`Title`, `Author`, `DC_License`, etc.) map to DC conceptual terms
  - `profiles.yml.example` – optional; “which DC terms are required/recommended/optional for this archive type”
- `standard/`
   Canonical, mostly read-only material:
  - `dcmi-terms.yml` – the official Dublin Core terms, IDs, descriptions (the “standard library” of DC)
- `templates/docs/`
   Maintainer documentation for the plugin that can be installed into an archive:
  - A “How to read and maintain Dublin Core metadata in this archive” page
- `lib/`
   Python (or other) code used by `bin/` scripts:
  - `dublin_core_validator.py` – the actual rules/checks
  - `dublin_core_mapper.py` – logic to map archive metadata to DC conceptual model
- `tests/`
   Self-contained test materials so the plugin is **self-verifying**:
  - fixtures with sample front matter
  - test scripts

Everything Dublin-Core-related lives **inside this bundle**.

SAT (the OS) just needs to know:

- “Where is the plugin bundle?” → `plugins/metadata/dublin-core/`
- “What does `plugin.yml` say to do?”

------

## 3. What `plugin.yml` would look like

Here is a more concrete `plugin.yml` for Dublin Core, in the spirit of your app metaphor:

```yaml
plugin_id: "metadata.dublin-core"
kind: "metadata-capsule"

description: "Dublin Core 1.1 metadata definitions, validation, and mappings for SAT archives."

entrypoints:
  cli:
    - id: "sat-dublin-core-validate"
      path: "bin/sat-dublin-core-validate"
    - id: "sat-dublin-core-explain"
      path: "bin/sat-dublin-core-explain"

install:
  # Runtime tools for the archive
  - src: "bin/sat-dublin-core-validate"
    dest: "tools/sat-dublin-core-validate"

  - src: "bin/sat-dublin-core-explain"
    dest: "tools/sat-dublin-core-explain"

  # Archive-facing configuration (editable by maintainers)
  - src: "config/mapping.yml.example"
    dest: "config/metadata/dublin-core/mapping.yml"

  - src: "config/profiles.yml.example"
    dest: "config/metadata/dublin-core/profiles.yml"

  # Standard terms, usually read-only
  - src: "standard/dcmi-terms.yml"
    dest: "config/metadata/dublin-core/standard/dcmi-terms.yml"

  # Documentation for archive maintainers
  - src: "templates/docs/dublin-core-metadata.md"
    dest: "docs/use/dublin-core-metadata.md"
```

You’ll notice:

- SAT doesn’t need to know any of these specifics; they’re all inside `plugin.yml`.
- Installing the plugin into an archive is just:
  - Read `install` entries
  - Copy `src` (inside bundle) → `dest` (inside archive root)

------

## 4. What gets installed in the archive (“the desktop”)

If a user says during archive creation:

```bash
archive-init \
  --root-dir ~/archives/wellbeing-mvp \
  --canonical en-CA \
  --taxonomy para \
  --capsules tools.core-runtime,metadata.dublin-core
```

The “Dublin Core app” will deposit its files into the archive like this:

```text
~/archives/wellbeing-mvp/
  tools/
    sat-refresh-path-metadata           # from tools.core-runtime
    sat-fill-default-metadata           # from tools.core-runtime
    sat-check-archive                   # from tools.core-runtime
    sat-dublin-core-validate            # from metadata.dublin-core
    sat-dublin-core-explain             # from metadata.dublin-core

  config/
    metadata_defaults.yml               # from core-runtime capsule
    tools_manifest.yml                  # from core-runtime capsule

    metadata/
      dublin-core/
        mapping.yml                     # from plugin config
        profiles.yml                    # from plugin config
        standard/
          dcmi-terms.yml                # from plugin standard

  docs/
    use/
      dublin-core-metadata.md           # from plugin templates
```

From the **archive maintainer’s perspective**, this looks wonderfully boring:

- They run:
  - `./tools/sat-dublin-core-validate`
  - `./tools/sat-check-archive`
- They edit:
  - `config/metadata/dublin-core/mapping.yml`
  - `config/metadata/dublin-core/profiles.yml`
  - `config/metadata_defaults.yml`
- They read:
  - `docs/use/dublin-core-metadata.md`

They never have to think:

- “Wait, where in the SAT repo did this come from?”
- “Which pieces belong to Dublin Core vs other plugins?”

The plugin bundle in SAT took care of all that.

------

## 5. How this ties into the bash tools you already have

Right now you’ve automated:

- `sat-refresh-path-metadata`
   → computes Path/URL/Canonical and updates front matter
- `sat-fill-default-metadata`
   → fills in Author, License, DC_License, DC_RightsHolder from defaults
- `sat-check-archive`
   → orchestrates checks

Dublin Core plugin fits into this ecosystem as:

- A **semantic layer** that:
  - knows what DC fields exist
  - knows which are required, recommended, optional
  - validates that what’s in front matter is DC-compliant

Practically, you get flows like:

1. User moves content around
    → `sat-refresh-path-metadata --apply` tempers the path-based fields.
2. User wants a consistent author/license baseline
    → `sat-fill-default-metadata --apply` ensures all docs have identity/rights metadata.
3. User wants to verify DC consistency
    → `sat-dublin-core-validate` scans all `.md` and uses:
   - `config/metadata/dublin-core/mapping.yml`
   - `config/metadata/dublin-core/profiles.yml`
   - `config/metadata/dublin-core/standard/dcmi-terms.yml`
   - Your existing metadata layering model (Derived → Defaults → Overrides → Manual)
4. `sat-check-archive` could, in future, call:
   - `sat-refresh-path-metadata` (read-only)
   - `sat-fill-default-metadata` (read-only)
   - `sat-dublin-core-validate` (read-only)
      and produce a summary.

The important part:
 Dublin Core as a plugin is **self-contained**, but **sits happily in the same ecosystem** as your bash tools.

------

## 6. Customization over time

Back to your metaphor:
 The “app” lands with sane defaults, and the user can customize.

For Dublin Core, that looks like:

- Initially:
  - `mapping.yml` and `profiles.yml` are generated from `.example` files in the plugin.
- Over time:
  - The maintainer tweaks `mapping.yml` to reflect:
    - how `Title` in your archive maps to `dc:title`
    - which of your internal keys feed into `dc:creator`, `dc:subject`, etc.
  - The maintainer adjusts `profiles.yml` for:
    - strictness per content type (e.g. research vs blog)
    - which fields must exist before publication

The plugin doesn’t need to change.
 The archive just updates its `config` files.

------

If you’re good with this shape, a natural next step would be to:

- Sketch the **actual contents** of `mapping.yml.example` and `profiles.yml.example` for your wellbeing archive, or
- Draft the initial `plugin.yml` for `metadata.dublin-core` in exactly the SAT path you want to use.