# source-archives-tools

Simple initialization and planning tools for working with **source archives**.
This early test harness focuses on:

* **English-only** tooling (for now)
* **No multilingual UI yet**
* **Minimal Bash scripts** implementing plan/apply
* **Expandable design** for future Python, standards-driven, multilingual versions

The goal of this phase is to verify core concepts, filesystem behaviour, and minimal configuration file production.

---

## Tools Installation

Source archives may be created in different canonical languages, but the **tools themselves** remain language-agnostic and English-only during this phase.

Choose your desired top-level directory for projects:

```bash
# English
PROJECTS_ROOT=~/projects/source-archives
# French
#PROJECTS_ROOT=~/projets/archives-sources
```

### Create the projects root

```bash
mkdir -p "$PROJECTS_ROOT"
cd "$PROJECTS_ROOT"
```

### Clone the tools repository

```bash
# English, tools folder
git clone git@github.com:<org>/source-archives-tools.git tools
# French, outils folder
# git clone git@github.com:<org>/source-archives-tools.git 
```

### Structure Created

```bash
tools/
  ├── scripts/   # init, plan, validate (early versions)
  ├── standards/ # BCP 47, accessibility...
  ├── templates/ # examples
  └── docs/      # how-tos and notes
```

This structure mirrors the longer term goals:

* **scripts/** - executable utilities
* **standards/** - reusable definitions (languages, metadata, accessibility)
* **templates/** - taxonomy presets (lattice)
* **docs/** - human-facing documentation

## Language Standards Example (future expansion)

While the KISS Bash tools do not use these files yet, the following structure prepares for Phase 2 (Python multilingual tooling):

```bash
nano standards/languages.yml
```

Example:

```yaml
# standards/languages.yml
version: 0.1.0
description: "Supported languages for source archive tooling."

languages:
  - name: "French (Québec)"
    bcp_47_tag: "fr-CA"
    default_slug: "fr-ca"
    direction: "ltr"

  - name: "English (Canada)"
    bcp_47_tag: "en-CA"
    default_slug: "en-ca"
    direction: "ltr"

  # Future example:
  # - name: "Spanish (Latin America)"
  #   bcp_47_tag: "es-419"
  #   default_slug: "es-la"
  #   direction: "ltr"
```

This file describes **standards**, not configuration.
Actual project configuration lives under `config/` inside each initialized archive.

---

## The `scripts/init-archive.sh` Tool (KISS Version)

This is a simple, English-only archive initializer.
It accepts:

* `--root-dir` — where the new archive will be created
* `--canonical` — BCP 47 tag of the canonical language, e.g., `fr-CA`
* `--also` — optional extra languages
* `--taxonomy` — taxonomy ID (default: `example-civic-lattice`)
* `--apply` — actually creates files (otherwise prints a plan)

Make it executable:

```bash
chmod +x scripts/init-archive.sh
```

---

## Archives Planning Example

Shows what an archive structure will look like

### Plan English canonical archive example

Command to plan a bilingual (English and French) archive

```bash
./scripts/init-archive.sh \
  --root-dir "~/projets/source-archives/civic-lattice/civic-archive" \
  --canonical en-CA \
  --also fr-CA \
  --taxonomy example-civic-lattice
```

#### Output example

```bash
=== Source Archive Initialization Plan ===

  Archive root : /home/initial/projets/source-archives/civic-lattice/civic-archive
  Canonical    : en-CA
  Other langs  : fr-CA
  Taxonomy     : example-civic-lattice

This script will:
  - Create base directories:
      /home/initial/projets/source-archives/civic-lattice/civic-archive/
      /home/initial/projets/source-archives/civic-lattice/civic-archive/config/
      /home/initial/projets/source-archives/civic-lattice/civic-archive/taxonomy/

  - Create minimal config files:
      /home/initial/projets/source-archives/civic-lattice/civic-archive/config/project.yml
      /home/initial/projets/source-archives/civic-lattice/civic-archive/config/languages.yml
      /home/initial/projets/source-archives/civic-lattice/civic-archive/config/structure.yml

  - Create locale roots for each language (using raw BCP 47 tags as placeholders):
      /home/initial/projets/source-archives/civic-lattice/civic-archive/en-ca/
      /home/initial/projets/source-archives/civic-lattice/civic-archive/fr-ca/

PLAN ONLY: No changes have been made. Re-run with --apply to create these paths.
```

### Plan French canonical archive example

Command to plan a bilingual (English and French) archive

```bash
./scripts/init-archive.sh \
  --root-dir "~/projets/archives-sources/treillis-civiques/exemple-treillis-civique" \
  --canonical fr-CA \
  --also en-CA \
  --taxonomy example-civic-lattice
```

#### Output example:

```bash
=== Source Archive Initialization Plan ===

  Archive root : /home/initial/projets/archives-sources/treillis-civiques/exemple-treillis-civique
  Canonical    : fr-CA
  Other langs  : en-CA
  Taxonomy     : example-civic-lattice

This script will:
  - Create base directories:
      .../exemple-treillis-civique/
      .../exemple-treillis-civique/config/
      .../exemple-treillis-civique/taxonomy/

  - Create minimal config files:
      config/project.yml
      config/languages.yml
      config/structure.yml

  - Create locale roots:
      .../exemple-treillis-civique/fr-ca/
      .../exemple-treillis-civique/en-ca/

PLAN ONLY: No changes have been made.
```

---



## Archive Creation Examples

Apply the configurations and create real files.

## Create English Canonical Archive

```bash
./scripts/init-archive.sh \
  --root-dir "~/projets/archives-sources/treillis-civiques/exemple-treillis-civique" \
  --canonical en-CA \
  --also fr-CA \
  --apply
```

### Create French Canonical Archive

```bash
./scripts/init-archive.sh \
  --root-dir "~/projets/archives-sources/treillis-civiques/exemple-treillis-civique" \
  --canonical fr-CA \
  --also en-CA \
  --apply
```

Then verify:

```bash
tree ~/projets/archives-sources/treillis-civiques/exemple-treillis-civique
```

Example result:

```
exemple-treillis-civique/
├── config
│   ├── languages.yml
│   ├── project.yml
│   └── structure.yml
├── en-ca
├── fr-ca
└── taxonomy
```

## Migrate to ROADMAP.md

* A Python-based multilingual setup tool
* Standards-aware validation (`bcp_47_valid`, `direction`, canonical rules)
* Taxonomy builders using templates
* Optional UI for selecting canonical language and project type
