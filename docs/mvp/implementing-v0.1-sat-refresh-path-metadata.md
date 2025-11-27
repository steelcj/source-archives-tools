---
Title: "Implementing the v0.1 sat-refresh-path-metadata Tool"
Description: "A complete guide and code listing for building the read-only v0.1 version of sat-refresh-path-metadata, including directory walking, derived metadata generation, and usage instructions."
Author: "Christopher Steel"
Date: "2025-11-25"
Last_Modified_Date: "2025-11-25"
License: "CC BY-SA 4.0"
Version: "1.0.0"
Tags:
  - "sovereign-archive-tools"
  - "metadata"
  - "development"
  - "sat"
  - "path-derivation"
Keywords:
  - "sat-refresh-path-metadata"
  - "archive-tools"
  - "metadata-regeneration"
  - "MVP"
  - "well-being-archive"
URL: "https://universalcake.com/tools/docs/develop/implementing-v0.1-sat-refresh-path-metadata"
Path: "tools/docs/develop/implementing-v0.1-sat-refresh-path-metadata.md"
Canonical: "https://universalcake.com/tools/docs/develop/implementing-v0.1-sat-refresh-path-metadata"
Sitemap: "true"
DC_Title: "Implementing the v0.1 sat-refresh-path-metadata Tool"
DC_Creator: "Christopher Steel"
DC_Subject: "Implementation of a read-only metadata regeneration tool for source archives"
DC_Description: "A step-by-step explanation and code for the first functional version of sat-refresh-path-metadata, enabling safe computation of derived metadata using archive directory structure."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
OG_Title: "Implementing the v0.1 sat-refresh-path-metadata Tool"
OG_Description: "A practical guide for implementing a read-only version of sat-refresh-path-metadata to compute archive path-based metadata."
OG_URL: "https://universalcake.com/tools/docs/develop/implementing-v0.1-sat-refresh-path-metadata"
Schema:
  "@context": "https://schema.org"
  "@type": "TechArticle"
  "name": "Implementing the v0.1 sat-refresh-path-metadata Tool"
  "description": "A complete development guide for the v0.1 version of sat-refresh-path-metadata, including code and usage examples."
  "author": "Christopher Steel"
  "contributor": "ChatGPT-5.1 (OpenAI)"
Video_Metadata: {}
---

# Implementing the v0.1 sat-refresh-path-metadata Tool

This document provides the full implementation of the **v0.1** version of `sat-refresh-path-metadata`, the first working tool in the Sovereign Archive Toolkit (sat).  
This version is intentionally **read-only** and focuses on building confidence in:

- Archive tree traversal  
- File discovery  
- Computing derived `Path`, `URL`, and `Canonical` values  
- Printing results without modifying any files  

This establishes a safe baseline before adding YAML parsing or write-back behavior.

# Overview of v0.1 Behavior

The v0.1 script:

- Walks the archive directory tree  
- Finds all Markdown files  
- Computes proposed:
  - `Path`
  - `URL`
  - `Canonical`
- Prints them in a clear, human-readable format  
- Excludes:
  - `config/`
  - `tools/`  
- Does not make any changes to files  

This is ideal for testing with a pilot archive.

# Full Script Listing: sat-refresh-path-metadata (v0.1 Read-Only)

Place this file at:

```
<archive-root>/tools/sat-refresh-path-metadata
```

Make it executable:

```bash
chmod +x tools/sat-refresh-path-metadata
```

````bash
#!/usr/bin/env bash
set -euo pipefail

# Sovereign Archive Toolkit (sat)
# v0.1: read-only path metadata planner
#
# This script walks the archive tree, finds Markdown files,
# and prints the "Path", "URL", and "Canonical" values it would
# assign based purely on file location.
#
# It does NOT modify any files yet.

show_help() {
  cat <<EOF
Usage: $(basename "$0") [--archive-root PATH]

Compute and print proposed Path/URL/Canonical metadata for all Markdown
files in an archive. This is a read-only v0.1 implementation.

Options:
  --archive-root PATH   Archive root directory (default: parent of this script)
  -h, --help            Show this help
EOF
}

ARCHIVE_ROOT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --archive-root)
      ARCHIVE_ROOT="${2:-}"
      shift 2
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      show_help
      exit 1
      ;;
  esac
done

# If archive root not given, assume this script lives in <archive-root>/tools/
if [[ -z "${ARCHIVE_ROOT}" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  ARCHIVE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
fi

if [[ ! -d "${ARCHIVE_ROOT}" ]]; then
  echo "Error: archive root does not exist: ${ARCHIVE_ROOT}" >&2
  exit 1
fi

echo "sat-refresh-path-metadata v0.1 (read-only)"
echo "Archive root: ${ARCHIVE_ROOT}"
echo

# Find all Markdown files, excluding tools/ and config/
while IFS= read -r -d '' file; do
  # Compute path relative to archive root
  rel="${file#${ARCHIVE_ROOT}/}"

  # Proposed Path: full relative path including extension
  proposed_path="${rel}"

  # Proposed URL: leading slash + relative path, without .md extension
  no_ext="${rel%.md}"
  proposed_url="/${no_ext}"

  # Canonical mirrors URL for v0.1
  proposed_canonical="${proposed_url}"

  echo "FILE: ${rel}"
  echo "  Path      -> ${proposed_path}"
  echo "  URL       -> ${proposed_url}"
  echo "  Canonical -> ${proposed_canonical}"
  echo

done < <(find "${ARCHIVE_ROOT}" -type f -name '*.md' \
           ! -path "${ARCHIVE_ROOT}/tools/*" \
           ! -path "${ARCHIVE_ROOT}/config/*" \
           -print0)
````

# How to Run It

From the pilot archive root:

```bash
./tools/sat-refresh-path-metadata
```

or explicitly:

```bash
./tools/sat-refresh-path-metadata --archive-root ~/archives/wellbeing-mvp
```

You will see output like:

```
FILE: en-ca/areas/well-being/projects/wellbeing-overview.md
  Path      -> en-ca/areas/well-being/projects/wellbeing-overview.md
  URL       -> /en-ca/areas/well-being/projects/wellbeing-overview
  Canonical -> /en-ca/areas/well-being/projects/wellbeing-overview
```

This confirms:

- Directory walking works  
- Paths resolve properly  
- URL derivation logic is sound  
- Canonical behaves predictably  

# Next Steps

Once this behavior is validated with your pilot archive, the next two stages will be:

## 1. Add YAML reading (still read-only)
- Load front matter  
- Compare old vs proposed values  
- Print differences only 

update tools/sat-refresh-path-metadata

```bash
#!/usr/bin/env bash
set -euo pipefail

# Sovereign Archive Toolkit (sat)
# v0.2: read-only path metadata diff
#
# - Walks the archive tree
# - Finds Markdown files
# - Computes proposed Path/URL/Canonical from file location
# - Reads existing YAML front matter (if present)
# - Prints old -> new for Path/URL/Canonical
#
# Still DOES NOT modify any files.

show_help() {
  cat <<EOF
Usage: $(basename "$0") [--archive-root PATH]

Compute and print proposed Path/URL/Canonical metadata for all Markdown
files in an archive, showing old -> new differences from YAML front
matter when present. This is a read-only v0.2 implementation.

Options:
  --archive-root PATH   Archive root directory (default: parent of this script)
  -h, --help            Show this help
EOF
}

ARCHIVE_ROOT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --archive-root)
      ARCHIVE_ROOT="${2:-}"
      shift 2
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      show_help
      exit 1
      ;;
  esac
done

# If archive root not given, assume this script lives in <archive-root>/tools/
if [[ -z "${ARCHIVE_ROOT}" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  ARCHIVE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
fi

if [[ ! -d "${ARCHIVE_ROOT}" ]]; then
  echo "Error: archive root does not exist: ${ARCHIVE_ROOT}" >&2
  exit 1
fi

echo "sat-refresh-path-metadata v0.2 (read-only, diff mode)"
echo "Archive root: ${ARCHIVE_ROOT}"
echo

# Helper: extract a YAML scalar value from front matter by key name
# Expects "Key: value" style lines between the first two '---' delimiters.
extract_yaml_field() {
  local key="$1"
  local file="$2"

  # awk:
  # - Start only after first '---'
  # - Stop after second '---'
  # - Match lines starting with "Key:"
  awk -v k="$key" '
    BEGIN { in_yaml = 0 }
    /^---[ \t]*$/ {
      if (in_yaml == 0) {
        in_yaml = 1
      } else if (in_yaml == 1) {
        in_yaml = 2
      }
      next
    }
    in_yaml == 1 && $0 ~ "^" k ":" {
      # strip "Key:" and leading spaces
      sub("^" k ":[ \t]*", "", $0)
      print $0
      exit
    }
  ' "$file"
}

# Find all Markdown files, excluding tools/ and config/
while IFS= read -r -d '' file; do
  rel="${file#${ARCHIVE_ROOT}/}"

  # Proposed Path: full relative path including extension
  proposed_path="${rel}"

  # Proposed URL: leading slash + relative path, without .md extension
  no_ext="${rel%.md}"
  proposed_url="/${no_ext}"

  # For now, Canonical mirrors URL
  proposed_canonical="${proposed_url}"

  # Existing metadata from YAML (if any)
  existing_path="$(extract_yaml_field "Path" "$file" || true)"
  existing_url="$(extract_yaml_field "URL" "$file" || true)"
  existing_canonical="$(extract_yaml_field "Canonical" "$file" || true)"

  echo "FILE: ${rel}"

  if [[ -n "$existing_path" ]]; then
    echo "  Path:      ${existing_path}  ->  ${proposed_path}"
  else
    echo "  Path:      (none)            ->  ${proposed_path}"
  fi

  if [[ -n "$existing_url" ]]; then
    echo "  URL:       ${existing_url}   ->  ${proposed_url}"
  else
    echo "  URL:       (none)            ->  ${proposed_url}"
  fi

  if [[ -n "$existing_canonical" ]]; then
    echo "  Canonical: ${existing_canonical} ->  ${proposed_canonical}"
  else
    echo "  Canonical: (none)            ->  ${proposed_canonical}"
  fi

  echo

done < <(find "${ARCHIVE_ROOT}" -type f -name '*.md' \
           ! -path "${ARCHIVE_ROOT}/tools/*" \
           ! -path "${ARCHIVE_ROOT}/config/*" \
           -print0)
```

run with

```bash
./tools/sat-refresh-path-metadata
```

Output example:

```bash
sat-refresh-path-metadata v0.2 (read-only, diff mode)
Archive root: /home/initial/archives/wellbeing-mvp

FILE: en-ca/resources/research/aces-and-health.md
  Path:      "TODO"  ->  en-ca/resources/research/aces-and-health.md
  URL:       "TODO"   ->  /en-ca/resources/research/aces-and-health
  Canonical: "TODO" ->  /en-ca/resources/research/aces-and-health

FILE: en-ca/resources/practices/basic-grounding.md
  Path:      "TODO"  ->  en-ca/resources/practices/basic-grounding.md
  URL:       "TODO"   ->  /en-ca/resources/practices/basic-grounding
  Canonical: "TODO" ->  /en-ca/resources/practices/basic-grounding

FILE: en-ca/areas/well-being/resources/wellbeing-dimensions.md
  Path:      "TODO"  ->  en-ca/areas/well-being/resources/wellbeing-dimensions.md
  URL:       "TODO"   ->  /en-ca/areas/well-being/resources/wellbeing-dimensions
  Canonical: "TODO" ->  /en-ca/areas/well-being/resources/wellbeing-dimensions

FILE: en-ca/areas/well-being/projects/wellbeing-overview.md
  Path:      "TODO"  ->  en-ca/areas/well-being/projects/wellbeing-overview.md
  URL:       "TODO"   ->  /en-ca/areas/well-being/projects/wellbeing-overview
  Canonical: "TODO" ->  /en-ca/areas/well-being/projects/wellbeing-overview
```

If that looks and feels right to you on this small pilot, the step *after* this will be:

- Add a `--write` / `--apply` mode that actually updates the front matter, leaving everything else intact.



## 2. Add safe write-back mode
- Only after thorough testing  
- Preserve all non-derived metadata  
- Commit-friendly atomic writes  

# License

This document, *Implementing the v0.1 sat-refresh-path-metadata Tool*, by **Christopher Steel**, with AI assistance from **ChatGPT-5.1 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
