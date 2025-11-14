#!/usr/bin/env bash
set -euo pipefail

show_help() {
  cat <<EOF
Usage: $(basename "$0") --root-dir PATH --canonical LANG [--also LANGS] [--taxonomy ID]

Initialise (plan-only) a new source archive.

Required:
  --root-dir PATH      Absolute or ~-expanded path to the archive root
  --canonical LANG     Canonical language (BCP 47), e.g. fr-CA, en-CA

Optional:
  --also LANGS         Comma-separated list of additional languages (BCP 47), e.g. en-CA,es-419
  --taxonomy ID        Taxonomy identifier, e.g. example-civic-lattice (default: example-civic-lattice)

This script is currently PLAN-ONLY:
  - It prints what it *would* create (directories + config files)
  - It does NOT write to disk yet
EOF
}

ROOT_DIR=""
CANONICAL=""
ALSO=""
TAXONOMY_ID="example-civic-lattice"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root-dir|--racine)
      ROOT_DIR="${2:-}"
      shift 2
      ;;
    --canonical|--canonique)
      CANONICAL="${2:-}"
      shift 2
      ;;
    --also|--aussi)
      ALSO="${2:-}"
      shift 2
      ;;
    --taxonomy|--taxonomie)
      TAXONOMY_ID="${2:-}"
      shift 2
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Argument inconnu: $1" >&2
      show_help
      exit 1
      ;;
  esac
done

if [[ -z "$ROOT_DIR" || -z "$CANONICAL" ]]; then
  echo "Erreur: --root-dir et --canonical sont obligatoires." >&2
  show_help
  exit 1
fi

# Expand ~ to home
ROOT_DIR="${ROOT_DIR/#\~/$HOME}"

# Normalise extra languages list
IFS=',' read -r -a EXTRA_LANGS <<< "${ALSO:-}"

echo "=== PLAN D'INITIALISATION D'UNE ARCHIVE-SOURCE ==="
echo
echo "  Racine de l'archive : $ROOT_DIR"
echo "  Langue canonique    : $CANONICAL"
if [[ ${#EXTRA_LANGS[@]} -gt 0 && -n "${EXTRA_LANGS[0]}" ]]; then
  echo "  Autres langues      : ${EXTRA_LANGS[*]}"
else
  echo "  Autres langues      : (aucune)"
fi
echo "  Taxonomie           : $TAXONOMY_ID"
echo
echo "Cette version est PLAN-ONLY : aucune écriture sur disque."
echo
echo "Elle créerait (au minimum) :"
echo "  - Dossiers :"
echo "      $ROOT_DIR/"
echo "      $ROOT_DIR/config/"
echo "      $ROOT_DIR/taxonomy/"
echo
echo "  - Fichiers de configuration :"
echo "      $ROOT_DIR/config/project.yml"
echo "      $ROOT_DIR/config/languages.yml"
echo "      $ROOT_DIR/config/structure.yml"
echo
echo "  - Lien ou copie de taxonomie :"
echo "      $ROOT_DIR/taxonomy/$TAXONOMY_ID.yml (ou répertoire équivalent)"
echo
echo "  - Racines de locales (selon langues) :"
echo "      $ROOT_DIR/<slug locale>/"
echo
echo "Prochaine étape :"
echo "  - Ajouter un mode --apply pour réellement créer ces dossiers/fichiers."
echo
