#!/usr/bin/env python3

print(">>> sat-inject-frontmatter starting <<<")

import os
import sys
from pathlib import Path
import yaml
from datetime import datetime
from jinja2 import Template

# =========================
# CONFIGURATION
# =========================

TEMPLATE_PATH = Path("satellites/euria/templates/sat-document-template.yml.j2")
MODEL_PATH = Path("satellites/euria/models/document-context.yml.j2")
CONFIG_PATH = Path("satellites/euria/config.yml")

# =========================
# HELPERS
# =========================

def load_yaml(path: Path) -> dict:
    """Load YAML file safely"""
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error loading {path}: {e}")
        sys.exit(2)

def get_context(filepath: Path) -> dict:
    """Extract context from file path"""
    filepath = filepath.resolve()
    parts = filepath.parts

    try:
        docs_idx = parts.index('docs')
    except ValueError:
        raise ValueError("File must be under a 'docs' directory")

    locale = parts[docs_idx + 1]
    domain = parts[docs_idx + 2]
    category = parts[docs_idx + 3] if len(parts) > docs_idx + 3 else None
    filename = filepath.name
    basename = filepath.stem  # ← This is what you want

    print(f"DEBUG: filename = {filename}")
    print(f"DEBUG: basename = {basename}")

    # Load config
    config = load_yaml(CONFIG_PATH)
    base_url = config.get('base_url', 'https://example.com')

    # Relative path (from archive root)
    relative_path = filepath.relative_to(filepath.anchor).as_posix().replace("archives/euria-generated/", "")

    return {
        'basename': basename,
        'domain': domain,
        'category': category,
        'locale': locale,
        'relative_path': relative_path,
        'base_url': base_url,
        'now': datetime.now().strftime("%Y-%m-%d")
    }

def render_model(context: dict) -> dict:
    """Render model template to produce model_data"""
    model_template_str = TEMPLATE_PATH.read_text(encoding="utf-8")
    model_template = Template(model_template_str)
    rendered_model = model_template.render(**context)

    try:
        model_data = yaml.safe_load(rendered_model)
    except Exception as e:
        print(f"Error parsing rendered model: {e}")
        sys.exit(2)

    # Ensure title is present
    if 'title' not in model_data:
        model_data['title'] = model_data.get('basename', '').replace('-', ' ').replace('_', ' ').title()

    print("DEBUG: model_data keys =", list(model_data.keys()))
    print("DEBUG: model_data['title'] =", model_data.get('title'))
    print("DEBUG: model_data['basename'] =", model_data.get('basename'))

    return model_data

def render_frontmatter(model_data: dict) -> str:
    """Render final front matter using template"""
    template_str = TEMPLATE_PATH.read_text(encoding="utf-8")
    template = Template(template_str)
    return template.render(**model_data)

def inject_frontmatter(filepath: Path, frontmatter: str):
    """Inject front matter into file"""
    content = filepath.read_text(encoding="utf-8")

    # Check if front matter already exists
    if content.startswith('---\n') and '\n---\n' in content:
        print(f"Front matter already exists in {filepath}. Skipping.")
        return

    # Write new content
    new_content = frontmatter + '\n' + content
    filepath.write_text(new_content, encoding="utf-8")
    print(f"SAT front matter generated for {filepath}")

# =========================
# MAIN
# =========================

def main():
    if len(sys.argv) != 2:
        print("Usage: sat-inject-frontmatter.py <filepath>")
        sys.exit(1)

    filepath = Path(sys.argv[1]).resolve()

    # Validate file exists
    if not filepath.exists():
        print(f"Error: {filepath} does not exist")
        sys.exit(2)

    # Get context
    context = get_context(filepath)

    # Render model
    model_data = render_model(context)

    # Render front matter
    frontmatter = render_frontmatter(model_data)

    # Inject into file
    inject_frontmatter(filepath, frontmatter)

if __name__ == "__main__":
    main()
