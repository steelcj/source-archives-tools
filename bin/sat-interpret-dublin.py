#!/usr/bin/env python3

print(">>> sat-interpret starting <<<")

import sys
from pathlib import Path
import argparse
from argparse import ArgumentParser
import yaml
from datetime import datetime
import uuid

# =========================
# CONFIGURATION
# =========================
TEMPLATE_PATH = Path("satellites/dublin-core-example.yml")
CONFIG_PATH = Path("config.yml")

# =========================
# HELPERS
# =========================
def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def get_context(filepath: Path, config: dict) -> dict:
    parts = filepath.parts

    try:
        docs_idx = parts.index('docs')
    except ValueError:
        raise ValueError(f"File {filepath} must be under a 'docs' directory")

    locale = parts[docs_idx + 1]
    domain = parts[docs_idx + 2]
    category = parts[docs_idx + 3] if len(parts) > docs_idx + 3 else None
    basename = filepath.stem
    relative_path = filepath.relative_to(filepath.anchor).as_posix().replace("archives/euria-generated/", "")

    base_url = config.get('base_url', 'https://universalcake.com')

    return {
        'basename': basename,
        'domain': domain,
        'category': category,
        'locale': locale,
        'relative_path': relative_path,
        'base_url': base_url,
        'now': datetime.now().strftime("%Y-%m-%d")
    }

# =========================
# MAIN
# =========================
def main():
    parser = argparse.ArgumentParser(description="Interpret document context to generate SAT-compliant metadata.")
    parser.add_argument("filepath", help="Path to the Markdown document")
    parser.add_argument("--config", required=True, help="Path to config.yml")
    parser.add_argument("--no-changes", action="store_true", help="Dry run — show sidecar, don't write or inject")
    parser.add_argument("--inject", action="store_true", help="Inject sidecar into document front matter")

    args = parser.parse_args()

    filepath = Path(args.filepath).resolve()
    config_path = Path(args.config).resolve()

    # Validate file is .md
    if filepath.suffix != '.md':
        print(f"Error: {filepath} is not a .md file")
        sys.exit(2)

    # Validate file is under 'docs'
    if 'docs' not in filepath.parts:
        print(f"Error: {filepath} must be under a 'docs' directory")
        sys.exit(2)

    # Validate config exists
    if not config_path.exists():
        print(f"Error: Config file {config_path} does not exist")
        sys.exit(2)

    # Load config
    config = load_yaml(config_path)

    # Get context
    context = get_context(filepath, config)

    # Augment model
    model = load_yaml(TEMPLATE_PATH)
    model['dc:title'] = context['basename'].replace('-', ' ').replace('_', ' ').title()
    model['dc:description'] = f"Initial draft of {model['dc:title']}."
    model['dc:language'] = context['locale']
    model['dc:date'] = context['now']
    model['dc:source'] = f"{context['base_url']}/{context['relative_path']}"
    model['dc:identifier'] = f"urn:uuid:{uuid.uuid4()}"

    # Project: Write sidecar
    sidecar_path = filepath.with_suffix(".sidecar.dublin-core.yml")
    sidecar_path.write_text(yaml.dump(model, sort_keys=False), encoding="utf-8")
    print(f"Sidecar written to: {sidecar_path}")

    # Inject? (if --inject)
    if args.inject:
        inject_frontmatter(filepath, model)

if __name__ == "__main__":
    main()
