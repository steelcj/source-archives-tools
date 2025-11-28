import yaml
from pathlib import Path

def load_language_config(plugin_root: Path):
    config_file = plugin_root / "config" / "languages.yml"
    if not config_file.exists():
        return None
    with config_file.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data or {}

def detect_language_from_path(file_path: Path, languages: list):
    """
    Detect language from the top-level directory.
    Example:
      ../test-archive/en-ca/docs/file.md -> slug = en-ca -> bcp_47 -> en-CA
    """
    parts = file_path.resolve().parts
    for part in parts:
        for lang in languages:
            if part == lang["slug"]:
                return lang["bcp_47_tag"]

    # fallback to canonical language
    for lang in languages:
        if lang.get("canonical"):
            return lang["bcp_47_tag"]

    return None

def apply_language(text: str, file_path: str, plugin_root: str):
    plugin_root = Path(plugin_root)
    file_path = Path(file_path)

    config = load_language_config(plugin_root)
    if not config:
        return text

    languages = config.get("languages", [])
    if not languages:
        return text

    detected = detect_language_from_path(file_path, languages)
    if not detected:
        return text

    # split YAML front matter if present
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        fm_data = yaml.safe_load(fm) or {}
    else:
        fm_data = {}
        body = text

    # do not overwrite existing explicit language
    if "DC_Language" not in fm_data:
        fm_data["DC_Language"] = detected

    new_fm = yaml.safe_dump(fm_data, sort_keys=False).strip()
    return f"---\n{new_fm}\n---\n{body.lstrip()}"
