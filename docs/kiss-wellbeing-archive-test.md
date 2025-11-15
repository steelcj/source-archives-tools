# KISS Wellbeing Archive Test

## Purpose

This document describes the minimal steps required to create a well-being source archive using the development version of source-archives-tools.  
The canonical language will be English (en-CA).  
All work takes place in the development directory:

```
~/projects/archives/dev/
```

## Pick your projects root and archive path

```bash
PROJECTS_ROOT=~/projects/archives/dev
mkdir -p "$PROJECTS_ROOT"
cd "$PROJECTS_ROOT"
```

Select a path for the well-being archive:

```bash
ARCHIVE_ROOT="$PROJECTS_ROOT/wellbeing-source-archive"
echo "$ARCHIVE_ROOT"
```

Resulting top-level structure:

```
~/projects/archives/dev/
    wellbeing-source-archive/
```

## Clone tools

```bash
cd "$PROJECTS_ROOT"
git clone git@github.com:steelcj/source-archives-tools.git tools
cd tools
git checkout dev
git status
git branch
```

Make the initialization script executable:

```bash
chmod +x scripts/init-archive.sh
```

## Plan the wellbeing archive

```bash
./scripts/init-archive.sh \
  --root-dir "$ARCHIVE_ROOT" \
  --canonical en-CA \
  --also fr-CA \
  --taxonomy wellbeing-lattice-v0
```

Example plan output:

```
=== Source Archive Initialization Plan ===

  Archive root : /home/initial/projects/archives/dev/wellbeing-source-archive
  Canonical    : en-CA
  Other langs  : fr-CA
  Taxonomy     : wellbeing-lattice-v0

This script will:
  - Create base directories:
      /home/initial/projects/archives/dev/wellbeing-source-archive/
      /home/initial/projects/archives/dev/wellbeing-source-archive/config/
      /home/initial/projects/archives/dev/wellbeing-source-archive/taxonomy/

  - Create minimal config files:
      /home/initial/projects/archives/dev/wellbeing-source-archive/config/project.yml
      /home/initial/projects/archives/dev/wellbeing-source-archive/config/languages.yml
      /home/initial/projects/archives/dev/wellbeing-source-archive/config/structure.yml

  - Create locale roots for each language (using raw BCP 47 tags as placeholders):
      /home/initial/projects/archives/dev/wellbeing-source-archive/en-ca/
      /home/initial/projects/archives/dev/wellbeing-source-archive/fr-ca/

PLAN ONLY: No changes have been made. Re-run with --apply to create these paths.
```

## Apply the plan

```bash
./scripts/init-archive.sh \
  --root-dir "$ARCHIVE_ROOT" \
  --canonical en-CA \
  --also fr-CA \
  --taxonomy wellbeing-lattice-v0 \
  --apply
```

Expected structure:

```
=== Source Archive Initialization Plan ===

  Archive root : /home/initial/projects/archives/dev/wellbeing-source-archive
  Canonical    : en-CA
  Other langs  : fr-CA
  Taxonomy     : wellbeing-lattice-v0

This script will:
  - Create base directories:
      /home/initial/projects/archives/dev/wellbeing-source-archive/
      /home/initial/projects/archives/dev/wellbeing-source-archive/config/
      /home/initial/projects/archives/dev/wellbeing-source-archive/taxonomy/

  - Create minimal config files:
      /home/initial/projects/archives/dev/wellbeing-source-archive/config/project.yml
      /home/initial/projects/archives/dev/wellbeing-source-archive/config/languages.yml
      /home/initial/projects/archives/dev/wellbeing-source-archive/config/structure.yml

  - Create locale roots for each language (using raw BCP 47 tags as placeholders):
      /home/initial/projects/archives/dev/wellbeing-source-archive/en-ca/
      /home/initial/projects/archives/dev/wellbeing-source-archive/fr-ca/

APPLY: Creating directories and minimal config...
Done. Archive initialized at: /home/initial/projects/archives/dev/wellbeing-source-archive
```

```bash
tree -L 2 "$ARCHIVE_ROOT"
```

output example

```bash
home/initial/projects/archives/dev/wellbeing-source-archive
├── config
│   ├── languages.yml
│   ├── project.yml
│   └── structure.yml
├── en-ca
├── fr-ca
└── taxonomy
```

## Add archive-wide configuration tools (KISS: one directory)

All supplemental scripts, templates, and hooks live in this folder:

```
wellbeing-source-archive/config/
```

Create the substructure:

```bash
mkdir -p "$ARCHIVE_ROOT/config"/{templates,scripts,hooks}
```

Create placeholder files:

```bash
touch "$ARCHIVE_ROOT/config/templates"/{document-template.yaml,program-template.yaml,practice-card-template.yaml}
touch "$ARCHIVE_ROOT/config/scripts"/{generate-cards.py,extract-bibliography.py,sync-translations.py,validate-metadata.py}
touch "$ARCHIVE_ROOT/config/hooks"/{pre-commit,pre-push}
```

## Create the P.A.R.A structure for en-ca

```bash
cd "$ARCHIVE_ROOT"

mkdir -p en-ca/{projects,areas,resources,archives}
mkdir -p en-ca/areas/{body,mind,others,models,research}
mkdir -p en-ca/areas/body/{physiology,sleep,somatics,chronic-illness,autonomic-regulation}
mkdir -p en-ca/areas/mind/{emotional-regulation,memory-and-learning,meditation,trauma-science,identity-and-agency}
mkdir -p en-ca/areas/mind/meditation/{satipatthana,loving-kindness,body-scanning}
mkdir -p en-ca/areas/others/{relationships,community,ecological-wellbeing,communication-models}
mkdir -p en-ca/areas/models/{triadic-body-mind-others,biopsychosocial,integrative-health,ecological-self,satipatthana-model}
mkdir -p en-ca/areas/research/{neuroscience,psychology,contemplative-science,social-science,open-science}

mkdir -p en-ca/resources/{thriving,frameworks,glossary,worksheets,checklists,diagrams}
mkdir -p en-ca/resources/diagrams/{mermaid,svg}

mkdir -p en-ca/archives/{version-history,bibliographies,notes,deprecated}

mkdir -p en-ca/projects/{ace-recovery,personal-transformation,comparative-models-wellbeing,wellbeing-cards,learning-science-tools}
```

```bash

```



## Create the French skeleton

```bash
mkdir -p fr-ca/{projets,domaines,ressources,archives}
mkdir -p fr-ca/domaines/{corps,esprit,autres,modeles,recherche}
mkdir -p fr-ca/ressources
mkdir -p fr-ca/archives
```

## Sanity checks

```bash
tree -L 2 "$ARCHIVE_ROOT"
```

Expected:

```
tree -L 2 "$ARCHIVE_ROOT"
/home/initial/projects/archives/dev/wellbeing-source-archive
├── config
│   ├── hooks
│   ├── languages.yml
│   ├── project.yml
│   ├── scripts
│   ├── structure.yml
│   └── templates
├── en-ca
│   ├── archives
│   ├── areas
│   ├── projects
│   └── resources
├── fr-ca
│   ├── archives
│   ├── domaines
│   ├── projets
│   └── ressources
└── taxonomy

16 directories, 3 files
```

The well-being archive is now fully scaffolded using the KISS convention of a single configuration directory.

```bash
tree -L 3 "$ARCHIVE_ROOT"
```

```bash
/home/initial/projects/archives/dev/wellbeing-source-archive
├── config
│   ├── hooks
│   │   ├── pre-commit
│   │   └── pre-push
│   ├── languages.yml
│   ├── project.yml
│   ├── scripts
│   │   ├── extract-bibliography.py
│   │   ├── generate-cards.py
│   │   ├── sync-translations.py
│   │   └── validate-metadata.py
│   ├── structure.yml
│   └── templates
│       ├── document-template.yaml
│       ├── practice-card-template.yaml
│       └── program-template.yaml
├── en-ca
│   ├── archives
│   │   ├── bibliographies
│   │   ├── deprecated
│   │   ├── notes
│   │   └── version-history
│   ├── areas
│   │   ├── body
│   │   ├── mind
│   │   ├── models
│   │   ├── others
│   │   └── research
│   ├── projects
│   │   ├── ace-recovery
│   │   ├── comparative-models-wellbeing
│   │   ├── learning-science-tools
│   │   ├── personal-transformation
│   │   └── wellbeing-cards
│   └── resources
│       ├── checklists
│       ├── diagrams
│       ├── frameworks
│       ├── glossary
│       ├── thriving
│       └── worksheets
├── fr-ca
│   ├── archives
│   ├── domaines
│   │   ├── autres
│   │   ├── corps
│   │   ├── esprit
│   │   ├── modeles
│   │   └── recherche
│   ├── projets
│   └── ressources
└── taxonomy

41 directories, 12 files
```

## Scripted Walkthough up to this point

```bash
#!/usr/bin/env bash
set -euo pipefail

ARCHIVE_ROOT="${1:-}"

if [ -z "$ARCHIVE_ROOT" ]; then
  echo "Usage: $0 /absolute/path/to/wellbeing-source-archive"
  exit 1
fi

if [ ! -d "$ARCHIVE_ROOT" ]; then
  echo "Archive root does not exist: $ARCHIVE_ROOT"
  exit 1
fi

echo "Using archive root: $ARCHIVE_ROOT"

cd "$ARCHIVE_ROOT"

echo "Creating config subdirectories..."
mkdir -p config/{templates,scripts,hooks}

echo "Creating template placeholders..."
touch config/templates/document-template.yaml
touch config/templates/program-template.yaml
touch config/templates/practice-card-template.yaml

echo "Creating script placeholders..."
touch config/scripts/generate-cards.py
touch config/scripts/extract-bibliography.py
touch config/scripts/sync-translations.py
touch config/scripts/validate-metadata.py

echo "Creating hook placeholders..."
touch config/hooks/pre-commit
touch config/hooks/pre-push

echo "Creating en-ca P.A.R.A. structure..."
mkdir -p en-ca/{projects,areas,resources,archives}

mkdir -p en-ca/areas/{body,mind,others,models,research}
mkdir -p en-ca/areas/body/{physiology,sleep,somatics,chronic-illness,autonomic-regulation}
mkdir -p en-ca/areas/mind/{emotional-regulation,memory-and-learning,meditation,trauma-science,identity-and-agency}
mkdir -p en-ca/areas/mind/meditation/{satipatthana,loving-kindness,body-scanning}
mkdir -p en-ca/areas/others/{relationships,community,ecological-wellbeing,communication-models}
mkdir -p en-ca/areas/models/{triadic-body-mind-others,biopsychosocial,integrative-health,ecological-self,satipatthana-model}
mkdir -p en-ca/areas/research/{neuroscience,psychology,contemplative-science,social-science,open-science}

mkdir -p en-ca/resources/{thriving,frameworks,glossary,worksheets,checklists,diagrams}
mkdir -p en-ca/resources/diagrams/{mermaid,svg}

mkdir -p en-ca/archives/{version-history,bibliographies,notes,deprecated}

mkdir -p en-ca/projects/{ace-recovery,personal-transformation,comparative-models-wellbeing,wellbeing-cards,learning-science-tools}

echo "Creating fr-ca skeleton..."
mkdir -p fr-ca/{projets,domaines,ressources,archives}
mkdir -p fr-ca/domaines/{corps,esprit,autres,modeles,recherche}
mkdir -p fr-ca/ressources
mkdir -p fr-ca/archives

echo "Done."
```

Use from anywhere

```bash
bash /path/to/kiss-wellbeing-post-init.sh \
  "$HOME/projects/archives/dev/wellbeing-source-archive"
```

## Ready to commit

Perfect. Here’s your ultra-minimal “close up shop” workflow.

In the root of your tools repo:

```bash
git status
```

Confirm the README you edited shows as modified.

Then:

```bash
git add README.md
git commit -m "Add KISS wellbeing archive walkthrough and automation script reference"
git push
```

If you’re on a feature branch:

```bash
git push -u origin <your-branch-name>
```

If you’re committing straight to `dev` (totally fine for this stage):

```bash
git push
```

That’s it — development session safely wrapped.

Sleep mode engaged.
