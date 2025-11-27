# init-archive MVP

- Keeping all existing behavior
- Adding:
  - `tools/` skeleton creation
  - `config/tools_manifest.yml` creation
  - Stub `sat-…` scripts

Here’s an updated MVP version of your script that does all of that in one place.

```bash
#!/usr/bin/env bash
set -euo pipefail

show_help() {
  cat <<EOF
Usage: $(basename "$0") --root-dir PATH --canonical LANG [--also LANGS] [--taxonomy ID] [--apply]

Initialize a new source archive (MVP version with tools skeleton).

Required:
  --root-dir PATH      Target path for the archive root (can include ~)
  --canonical LANG     Canonical language (BCP 47), e.g. fr-CA, en-CA

Optional:
  --also LANGS         Comma-separated list of additional languages, e.g. en-CA,es-419
  --taxonomy ID        Taxonomy identifier (default: example-civic-lattice)
  --apply              Actually create directories and config files
  -h, --help           Show this help

Without --apply, this script only prints what it would do (plan mode).
EOF
}

ROOT_DIR=""
CANONICAL=""
ALSO=""
TAXONOMY_ID="example-civic-lattice"
APPLY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root-dir)
      ROOT_DIR="${2:-}"
      shift 2
      ;;
    --canonical)
      CANONICAL="${2:-}"
      shift 2
      ;;
    --also)
      ALSO="${2:-}"
      shift 2
      ;;
    --taxonomy)
      TAXONOMY_ID="${2:-}"
      shift 2
      ;;
    --apply)
      APPLY=true
      shift 1
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

if [[ -z "$ROOT_DIR" || -z "$CANONICAL" ]]; then
  echo "Error: --root-dir and --canonical are required." >&2
  show_help
  exit 1
fi

# Expand ~ to $HOME
ROOT_DIR="${ROOT_DIR/#\~/$HOME}"

# Build languages array: canonical first, then extras
LANGS=("$CANONICAL")
if [[ -n "$ALSO" ]]; then
  IFS=',' read -r -a EXTRA <<< "$ALSO"
  for l in "${EXTRA[@]}"; do
    [[ -n "$l" ]] && LANGS+=("$l")
  done
fi

echo "=== Source Archive Initialization Plan ==="
echo
echo "  Archive root : $ROOT_DIR"
echo "  Canonical    : $CANONICAL"
if [[ ${#LANGS[@]} -gt 1 ]]; then
  echo "  Other langs  : ${LANGS[*]:1}"
else
  echo "  Other langs  : (none)"
fi
echo "  Taxonomy     : $TAXONOMY_ID"
echo
echo "This script will:"
echo "  - Create base directories:"
echo "      $ROOT_DIR/"
echo "      $ROOT_DIR/config/"
echo "      $ROOT_DIR/taxonomy/"
echo
echo "  - Create minimal config files:"
echo "      $ROOT_DIR/config/project.yml"
echo "      $ROOT_DIR/config/languages.yml"
echo "      $ROOT_DIR/config/structure.yml"
echo "      $ROOT_DIR/config/tools_manifest.yml"
echo
echo "  - Create locale roots for each language (using raw BCP 47 tags as placeholders):"
for lang in "${LANGS[@]}"; do
  slug="${lang,,}"
  echo "      $ROOT_DIR/$slug/"
done
echo
echo "  - Create tools runtime skeleton:"
echo "      $ROOT_DIR/tools/"
echo "      $ROOT_DIR/tools/docs/usage/"
echo "      $ROOT_DIR/tools/plugins/"
echo "      $ROOT_DIR/tools/lib/"
echo "      $ROOT_DIR/tools/sat-refresh-path-metadata"
echo "      $ROOT_DIR/tools/sat-apply-taxonomy"
echo "      $ROOT_DIR/tools/sat-check-archive"
echo

if ! $APPLY; then
  echo "PLAN ONLY: No changes have been made. Re-run with --apply to create these paths."
  exit 0
fi

echo "APPLY: Creating directories, minimal config, and tools skeleton..."

mkdir -p "$ROOT_DIR/config" "$ROOT_DIR/taxonomy"

# Create locale roots
for lang in "${LANGS[@]}"; do
  slug="${lang,,}"
  mkdir -p "$ROOT_DIR/$slug"
done

############################################
# Config files
############################################

# Minimal config/project.yml
cat > "$ROOT_DIR/config/project.yml" <<EOF
# config/project.yml
version: 0.1.0
root_dir: "$ROOT_DIR"
taxonomy: "$TAXONOMY_ID"
EOF

# Minimal config/languages.yml
{
  echo "# config/languages.yml"
  echo "version: 0.1.0"
  echo "languages:"
  for idx in "${!LANGS[@]}"; do
    lang="${LANGS[$idx]}"
    slug="${lang,,}"
    canonical_flag="false"
    [[ $idx -eq 0 ]] && canonical_flag="true"
    cat <<EOF2
  - bcp_47_tag: "$lang"
    slug: "$slug"
    canonical: $canonical_flag
EOF2
  done
} > "$ROOT_DIR/config/languages.yml"

# Minimal config/structure.yml
cat > "$ROOT_DIR/config/structure.yml" <<EOF
# config/structure.yml
version: 0.1.0
root_dir: "$ROOT_DIR"
taxonomy: "$TAXONOMY_ID"
languages_from: "config/languages.yml"

create:
  locale_roots: true
  taxonomy_roots: false  # taxonomy-specific builder logic comes later
EOF

# Minimal config/tools_manifest.yml (MVP stub)
cat > "$ROOT_DIR/config/tools_manifest.yml" <<EOF
# config/tools_manifest.yml
version: "0.1.0"

tools_origin:
  repo_url: "https://example.com/source-archive-tools.git"
  commit: "UNKNOWN"

plugins:
  taxonomy:
    - "$TAXONOMY_ID"
  metadata: []

runtime:
  tools_dir: "tools"
  tools_version: "0.1.0"
EOF

############################################
# Tools runtime skeleton
############################################

mkdir -p \
  "$ROOT_DIR/tools/docs/usage" \
  "$ROOT_DIR/tools/plugins/taxonomy" \
  "$ROOT_DIR/tools/plugins/metadata" \
  "$ROOT_DIR/tools/lib"

# Stub scripts (MVP: just echo behavior for now)
cat > "$ROOT_DIR/tools/sat-refresh-path-metadata" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "sat-refresh-path-metadata: MVP stub. Not implemented yet."
EOF

cat > "$ROOT_DIR/tools/sat-apply-taxonomy" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "sat-apply-taxonomy: MVP stub. Not implemented yet."
EOF

cat > "$ROOT_DIR/tools/sat-check-archive" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "sat-check-archive: MVP stub. Not implemented yet."
EOF

chmod +x \
  "$ROOT_DIR/tools/sat-refresh-path-metadata" \
  "$ROOT_DIR/tools/sat-apply-taxonomy" \
  "$ROOT_DIR/tools/sat-check-archive"

# Placeholder lib helpers (empty for now, but ready to grow)
cat > "$ROOT_DIR/tools/lib/__init__.py" <<'EOF'
# Sovereign Archive Toolkit (sat) library package (MVP stub).
EOF

cat > "$ROOT_DIR/tools/lib/io_utils.py" <<'EOF'
# MVP stub for I/O utilities used by sat tools.
EOF

cat > "$ROOT_DIR/tools/lib/metadata_utils.py" <<'EOF'
# MVP stub for metadata utilities used by sat tools.
EOF

echo "Done. Archive initialized at: $ROOT_DIR"
echo "A basic tools runtime skeleton and tools_manifest.yml have been created."
```

You can now:

- Run this in **plan mode**:

```bash
./init-archive.sh --root-dir ~/archives/wellbeing --canonical en-CA --taxonomy para
```

- Then **apply**:

```bash
./init-archive.sh --root-dir ~/archives/wellbeing --canonical en-CA --taxonomy para --apply
```

Next steps after this MVP:

- Flesh out `sat-refresh-path-metadata` to actually walk the tree and print computed paths.
- Later, add real write-back behavior.

If you’d like, next I can focus specifically on a v0.1 implementation of `sat-refresh-path-metadata` that only runs in “plan mode” (no file modifications) so you can start testing safely on a tiny pilot archive.