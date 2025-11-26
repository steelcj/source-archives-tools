---
Title: "Implementing sat-fill-default-metadata v0.1 for Archive-Wide Identity and Rights Defaults"
Description: "A read-only implementation of sat-fill-default-metadata v0.1 that loads archive-wide metadata defaults and shows how they would be applied to documents without modifying any files."
Author: "Christopher Steel"
Date: "2025-11-25"
Last_Modified_Date: "2025-11-25"
License: "CC BY-SA 4.0"
Version: "1.0.0"
Tags:
  - "metadata"
  - "defaults"
  - "sat"
  - "sovereign-archives"
  - "tooling"
Keywords:
  - "sat-fill-default-metadata"
  - "metadata defaults"
  - "archive tooling"
  - "identity metadata"
  - "license metadata"
URL: "https://universalcake.com/tools/docs/develop/implementing-sat-fill-default-metadata-v0-1"
Path: "tools/docs/develop/implementing-sat-fill-default-metadata-v0-1.md"
Canonical: "https://universalcake.com/tools/docs/develop/implementing-sat-fill-default-metadata-v0-1"
Sitemap: "true"
DC_Title: "Implementing sat-fill-default-metadata v0.1 for Archive-Wide Identity and Rights Defaults"
DC_Creator: "Christopher Steel"
DC_Subject: "Implementation of a read-only metadata defaults tool for Sovereign Archives"
DC_Description: "This document provides a full v0.1 implementation of sat-fill-default-metadata, a read-only tool that loads archive-wide defaults from metadata_defaults.yml and reports how they would be applied to each document."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
OG_Title: "Implementing sat-fill-default-metadata v0.1 for Archive-Wide Identity and Rights Defaults"
OG_Description: "A practical guide and code listing for sat-fill-default-metadata v0.1, enabling safe, read-only inspection of archive-wide metadata defaults."
OG_URL: "https://universalcake.com/tools/docs/develop/implementing-sat-fill-default-metadata-v0-1"
Schema:
  "@context": "https://schema.org"
  "@type": "TechArticle"
  "name": "Implementing sat-fill-default-metadata v0.1 for Archive-Wide Identity and Rights Defaults"
  "description": "A complete v0.1 implementation of the sat-fill-default-metadata tool for the Sovereign Archive Toolkit, focusing on archive-wide identity and rights metadata defaults."
  "author": "Christopher Steel"
  "contributor": "ChatGPT-5.1 (OpenAI)"
Video_Metadata: {}
---

# Implementing sat-fill-default-metadata v0.1 for Archive-Wide Identity and Rights Defaults

This document defines and implements **`sat-fill-default-metadata` v0.1**, a **read-only** tool in the Sovereign Archive Toolkit (SAT) that:

- Loads archive-wide metadata defaults from `config/metadata_defaults.yml`
- Walks all Markdown documents in an archive
- Reads existing YAML front matter fields
- Shows how default metadata **would** be applied
- Does **not** modify any files

This tool covers the **Defaults layer** in the metadata hierarchy:

1. Derived  
2. Defaults  
3. Overrides  
4. Manual  

and focuses specifically on **identity and rights** metadata (Author, License, and Dublin Core identity fields).

## Assumptions and Scope for v0.1

To keep v0.1 safe, simple, and useful:

- The tool is **read-only** (no write-back).
- It operates on the following metadata fields:
  - `Author`
  - `License`
  - `DC_Creator`
  - `DC_License`
  - `DC_RightsHolder`
- It loads defaults from `config/metadata_defaults.yml` using a simple, stable YAML pattern.
- It **never assumes overwrite**; it only shows what it would fill if the fields are missing.
- It shares the same archive-root detection pattern as `sat-refresh-path-metadata`.

## Expected metadata_defaults.yml Structure

The tool expects a `config/metadata_defaults.yml` file shaped like this (MVP):

```yaml
version: "0.1.0"

defaults:
  authors:
    - "Christopher Steel"
  dc_creators:
    - "Christopher Steel"

  license: "CC BY-SA 4.0"
  license_id: "cc-by-sa-4.0"
  dc_license: "https://creativecommons.org/licenses/by-sa/4.0/"
  dc_rights_holder: "Christopher Steel"

  dc_language_from_locale: true

  tags: []
  keywords: []

  allow_overwrite_existing: false

authors:
  - id: "christopher-steel"
    name: "Christopher Steel"
    role: "Primary author and content steward"
  - id: "guest-author"
    name: "Guest Author"
    role: "Contributor"

licenses:
  - id: "cc-by-sa-4.0"
    label: "Creative Commons Attribution-ShareAlike 4.0"
    url: "https://creativecommons.org/licenses/by-sa/4.0/"

keyword_sets: []
```

For v0.1, the tool uses:

- `defaults.authors` → default Author(s) (picks the first value for simple scalar comparison)
- `defaults.dc_creators` → default DC_Creator(s) (also first value for display)
- `defaults.license`
- `defaults.dc_license`
- `defaults.dc_rights_holder`

Other keys are reserved for future iterations.

## Tool Behavior: High-Level Summary

For each Markdown file:

1. Compute its path relative to the archive root.
2. Read YAML front matter and extract:
   - `Author`
   - `License`
   - `DC_Creator`
   - `DC_License`
   - `DC_RightsHolder`
3. Load the archive-wide defaults (once per run).
4. For each field:
   - If the field is **missing or empty**, show:  
     `Field: (none) -> <default>`
   - If the field is **already set**, show:  
     `Field: <existing> (unchanged)`
5. Print a summary block per file.

No modifications to files are made.

## sat-fill-default-metadata v0.1 Script

Place this script at:

```
<archive-root>/tools/sat-fill-default-metadata
```

and make it executable:

```bash
chmod +x tools/sat-fill-default-metadata
```

### Full Script

```bash
#!/usr/bin/env bash
set -euo pipefail

# Sovereign Archive Toolkit (sat)
# sat-fill-default-metadata v0.1
#
# Read-only tool:
# - Loads archive-wide metadata defaults from config/metadata_defaults.yml
# - Walks Markdown files
# - Reads YAML front matter
# - Shows how Author / License / DC_* defaults would be applied
# - Does NOT modify any files

show_help() {
  cat <<EOF
Usage: $(basename "$0") [--archive-root PATH] [--defaults PATH]

Read-only inspection of archive-wide metadata defaults for Markdown files.

Options:
  --archive-root PATH   Archive root directory (default: parent of this script)
  --defaults PATH       Path to metadata_defaults.yml
                        (default: ARCHIVE_ROOT/config/metadata_defaults.yml)
  -h, --help            Show this help
EOF
}

ARCHIVE_ROOT=""
DEFAULTS_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --archive-root)
      ARCHIVE_ROOT="${2:-}"
      shift 2
      ;;
    --defaults)
      DEFAULTS_FILE="${2:-}"
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

# Defaults file
if [[ -z "${DEFAULTS_FILE}" ]]; then
  DEFAULTS_FILE="${ARCHIVE_ROOT}/config/metadata_defaults.yml"
fi

if [[ ! -f "${DEFAULTS_FILE}" ]]; then
  echo "Error: metadata defaults file not found: ${DEFAULTS_FILE}" >&2
  exit 1
fi

echo "sat-fill-default-metadata v0.1 (read-only)"
echo "Archive root : ${ARCHIVE_ROOT}"
echo "Defaults file: ${DEFAULTS_FILE}"
echo

########################################
# Load defaults from metadata_defaults.yml
########################################

DEFAULT_AUTHOR=""
DEFAULT_DC_CREATOR=""
DEFAULT_LICENSE=""
DEFAULT_DC_LICENSE=""
DEFAULT_DC_RIGHTS_HOLDER=""

# Simple YAML extraction for this specific structure.
# We assume:
# defaults:
#   authors:
#     - "Name"
#   dc_creators:
#     - "Name"
#   license: "..."
#   dc_license: "..."
#   dc_rights_holder: "..."

load_defaults() {
  local file="$1"

  # First author in defaults.authors
  DEFAULT_AUTHOR="$(
    awk '
      /^defaults:/ { in_def=1; next }
      in_def && /^authors:/ { in_auth=1; next }
      in_auth && /^ *- / {
        gsub(/^- *"/, "", $0)
        gsub(/"$/, "", $0)
        print $0
        exit
      }
      in_auth && /^[^ ]/ { in_auth=0 }
    ' "$file"
  )"

  # First dc_creator in defaults.dc_creators
  DEFAULT_DC_CREATOR="$(
    awk '
      /^defaults:/ { in_def=1; next }
      in_def && /^dc_creators:/ { in_dc=1; next }
      in_dc && /^ *- / {
        gsub(/^- *"/, "", $0)
        gsub(/"$/, "", $0)
        print $0
        exit
      }
      in_dc && /^[^ ]/ { in_dc=0 }
    ' "$file"
  )"

  # Scalar license
  DEFAULT_LICENSE="$(
    awk '
      /^defaults:/ { in_def=1; next }
      in_def && /^ *license:/ {
        sub(/^ *license:[ \t]*/, "", $0)
        gsub(/"/, "", $0)
        print $0
        exit
      }
    ' "$file"
  )"

  # Scalar dc_license
  DEFAULT_DC_LICENSE="$(
    awk '
      /^defaults:/ { in_def=1; next }
      in_def && /^ *dc_license:/ {
        sub(/^ *dc_license:[ \t]*/, "", $0)
        gsub(/"/, "", $0)
        print $0
        exit
      }
    ' "$file"
  )"

  # Scalar dc_rights_holder
  DEFAULT_DC_RIGHTS_HOLDER="$(
    awk '
      /^defaults:/ { in_def=1; next }
      in_def && /^ *dc_rights_holder:/ {
        sub(/^ *dc_rights_holder:[ \t]*/, "", $0)
        gsub(/"/, "", $0)
        print $0
        exit
      }
    ' "$file"
  )"
}

load_defaults "${DEFAULTS_FILE}"

echo "Loaded default metadata:"
echo "  Author:           ${DEFAULT_AUTHOR:-<none>}"
echo "  DC_Creator:       ${DEFAULT_DC_CREATOR:-<none>}"
echo "  License:          ${DEFAULT_LICENSE:-<none>}"
echo "  DC_License:       ${DEFAULT_DC_LICENSE:-<none>}"
echo "  DC_RightsHolder:  ${DEFAULT_DC_RIGHTS_HOLDER:-<none>}"
echo

########################################
# Helper: extract a YAML scalar from front matter
########################################

extract_yaml_field() {
  local key="$1"
  local file="$2"

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
      sub("^" k ":[ \t]*", "", $0)
      gsub(/"/, "", $0)
      print $0
      exit
    }
  ' "$file"
}

########################################
# Walk Markdown files and show diffs
########################################

while IFS= read -r -d '' file; do
  rel="${file#${ARCHIVE_ROOT}/}"

  existing_author="$(extract_yaml_field "Author" "$file" || true)"
  existing_license="$(extract_yaml_field "License" "$file" || true)"
  existing_dc_creator="$(extract_yaml_field "DC_Creator" "$file" || true)"
  existing_dc_license="$(extract_yaml_field "DC_License" "$file" || true)"
  existing_dc_rights_holder="$(extract_yaml_field "DC_RightsHolder" "$file" || true)"

  echo "FILE: ${rel}"

  # Author
  if [[ -z "${DEFAULT_AUTHOR}" ]]; then
    echo "  Author:      (no default configured)"
  else
    if [[ -z "${existing_author}" ]]; then
      echo "  Author:      (none) -> \"${DEFAULT_AUTHOR}\""
    else
      echo "  Author:      \"${existing_author}\" (unchanged)"
    fi
  fi

  # DC_Creator
  if [[ -z "${DEFAULT_DC_CREATOR}" ]]; then
    echo "  DC_Creator:  (no default configured)"
  else
    if [[ -z "${existing_dc_creator}" ]]; then
      echo "  DC_Creator:  (none) -> \"${DEFAULT_DC_CREATOR}\""
    else
      echo "  DC_Creator:  \"${existing_dc_creator}\" (unchanged)"
    fi
  fi

  # License
  if [[ -z "${DEFAULT_LICENSE}" ]]; then
    echo "  License:     (no default configured)"
  else
    if [[ -z "${existing_license}" ]]; then
      echo "  License:     (none) -> \"${DEFAULT_LICENSE}\""
    else
      echo "  License:     \"${existing_license}\" (unchanged)"
    fi
  fi

  # DC_License
  if [[ -z "${DEFAULT_DC_LICENSE}" ]]; then
    echo "  DC_License:  (no default configured)"
  else
    if [[ -z "${existing_dc_license}" ]]; then
      echo "  DC_License:  (none) -> \"${DEFAULT_DC_LICENSE}\""
    else
      echo "  DC_License:  \"${existing_dc_license}\" (unchanged)"
    fi
  fi

  # DC_RightsHolder
  if [[ -z "${DEFAULT_DC_RIGHTS_HOLDER}" ]]; then
    echo "  DC_RightsHolder: (no default configured)"
  else
    if [[ -z "${existing_dc_rights_holder}" ]]; then
      echo "  DC_RightsHolder: (none) -> \"${DEFAULT_DC_RIGHTS_HOLDER}\""
    else
      echo "  DC_RightsHolder: \"${existing_dc_rights_holder}\" (unchanged)"
    fi
  fi

  echo

done < <(find "${ARCHIVE_ROOT}" -type f -name '*.md' \
           ! -path "${ARCHIVE_ROOT}/tools/*" \
           ! -path "${ARCHIVE_ROOT}/config/*" \
           -print0)
```

## Usage

From the archive root:

```bash
./tools/sat-fill-default-metadata
```

Or explicitly:

```bash
./tools/sat-fill-default-metadata \
  --archive-root ~/archives/wellbeing-mvp \
  --defaults ~/archives/wellbeing-mvp/config/metadata_defaults.yml
```

Sample output:

```text
sat-fill-default-metadata v0.1 (read-only)
Archive root : /home/you/archives/wellbeing-mvp
Defaults file: /home/you/archives/wellbeing-mvp/config/metadata_defaults.yml

Loaded default metadata:
  Author:           Christopher Steel
  DC_Creator:       Christopher Steel
  License:          CC BY-SA 4.0
  DC_License:       https://creativecommons.org/licenses/by-sa/4.0/
  DC_RightsHolder:  Christopher Steel

FILE: en-ca/resources/practices/basic-grounding.md
  Author:      (none) -> "Christopher Steel"
  DC_Creator:  (none) -> "Christopher Steel"
  License:     (none) -> "CC BY-SA 4.0"
  DC_License:  (none) -> "https://creativecommons.org/licenses/by-sa/4.0/"
  DC_RightsHolder: (none) -> "Christopher Steel"
```

No changes are made to files. This lets you safely inspect how defaults will apply across the archive.

## Next Steps

Future versions of `sat-fill-default-metadata` might:

- Add a `--apply` or `--write` flag to actually update front matter
- Respect `allow_overwrite_existing` rules
- Integrate with overrides from `metadata_scopes.yml`
- Support multi-author lists and more complex structures

For now, v0.1 provides a safe, inspectable foundation for the **Defaults** layer of the SAT metadata system.

## License

This document, *Implementing sat-fill-default-metadata v0.1 for Archive-Wide Identity and Rights Defaults*, by **Christopher Steel**, with AI assistance from **ChatGPT-5.1 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)