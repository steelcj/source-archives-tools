---
Title: "Language Plugin MVP: Creation Guide"
Description: "A complete step-by-step guide for creating the Language/Locale metadata plugin MVP for Source Archive Tools, including directory structure, plugin manifest, configuration, implementation, tests, and integration with a language-root test archive."
Author: "Christopher Steel"
Date: "2025-11-27"
Last_Modified_Date: "2025-11-27"
License: "CC BY-SA 4.0"
Version: "0.1.0"
Tags:
  - "plugin"
  - "language"
  - "locale"
  - "metadata"
  - "source-archives-tools"
  - "mvp"
Keywords:
  - "language-plugin"
  - "locale"
  - "bcp47"
  - "metadata"
  - "source-archives"
URL: "https://github.com/steelcj/source-archives-tools/blob/dev/plugins/language/docs/language-plugin-mvp.md"
Path: "plugins/language/docs/language-plugin-mvp.md"
Canonical: "https://github.com/steelcj/source-archives-tools/blob/dev/plugins/language/docs/language-plugin-mvp.md"
Sitemap: "false"
DC_Title: "Language Plugin MVP: Creation Guide"
DC_Creator: "Christopher Steel"
DC_Subject: "A guide for creating the language/locale metadata plugin MVP for SAT, including implementation, configuration, tests, and integration workflow."
DC_Description: "Instructions for constructing the first version of the language/locale metadata plugin used by Source Archive Tools, including file structure, plugin manifest, plugin code, test design, and integration with a language-rooted archive."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
DC_Contributor: "ChatGPT-5.1 (OpenAI)"
DC_RightsHolder: "Christopher Steel"
OG_Title: "Language Plugin MVP: Creation Guide"
OG_Description: "A complete, self-contained guide for creating the Language/Locale metadata plugin MVP for SAT."
OG_URL: "https://github.com/steelcj/source-archive-tools/blob/dev/plugins/language/docs/language-plugin-mvp.md"
OG_Image: ""
Schema:
  "@context": "https://schema.org"
  "@type": "TechArticle"
  "headline": "Language Plugin MVP: Creation Guide"
  "author": "Christopher Steel"
  "inLanguage": "en"
  "license": "https://creativecommons.org/licenses/by-sa/4.0/"
  "contributor": "ChatGPT-5.1 (OpenAI)"
Video_Metadata: ""
---

# Language Plugin MVP — Creation Guide

This document defines the **minimum viable version** of the `language` plugin for Source Archive Tools (SAT).  
It mirrors the structure and philosophy of the `dublin_core` plugin, including:

- plugin directory structure  
- plugin manifest (`plugin.yml`)  
- config directory  
- testing directory  
- plugin implementation  
- self-tests  
- integration testing using a **language-root test archive**

The primary objective:

> **Automatically determine document language from the top-level archive directory (e.g., `en-ca/`, `fr-qc/`) and insert the appropriate BCP-47 language tag into the document’s YAML metadata.**

No advanced translation, locale negotiation, or metadata merging is included at this stage.

## Plugin Directory Structure (MVP)

From inside your cloned `tools/` directory:

```bash
mkdir -p plugins/language/{config,standard,tests/md,docs}
```

Resulting structure:

```bash
plugins/language/
├── config/
├── standard/
├── tests/
│   └── md/
├── docs/
├── plugin.py
└── plugin.yml
```

This matches SAT’s expected plugin model and mirrors `dublin_core`.

## Plugin Manifest (`plugin.yml`)

Create:

```bash
nano plugins/language/plugin.yml
```

Content:

```yaml
id: "language"
name: "Language Detection Plugin"
version: "0.1.0"

entrypoints:
  apply:
    run: "plugin.py"
    callable: "apply_language"

paths:
  config: "config"
  standard: "standard"
```

The `apply` entrypoint defines the callable executed when SAT applies metadata.

## Plugin Configuration (`config/languages.yml`)

This file defines the language slugs and their BCP-47 tags.

Create:

```bash
nano plugins/language/config/languages.yml
```

Content:

```yaml
version: "0.1.0"

languages:
  - bcp_47_tag: "en-CA"
    slug: "en-ca"
    canonical: true

  - bcp_47_tag: "fr-QC"
    slug: "fr-qc"
    canonical: false
```

Meaning:

- `en-ca` is the **default language**  
- `fr-qc` is available, non-default  
- Slugs are directory names at archive root  
- Plugins insert `DC_Language: <bcp_47_tag>`

## Plugin Implementation (`plugin.py`)

Create:

```bash
nano plugins/language/plugin.py
```

Content:

```python
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
      ../test-archive/en-ca/file.md -> slug = en-ca -> bcp_47 -> en-CA
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
```

This is the **core MVP**.

## Creating Plugin-Local Test Markdown Files

```bash
mkdir -p plugins/language/tests/md/{minimal,override}
```

### Minimal Test

Create:

```bash
nano plugins/language/tests/md/minimal/language-minimal.md
```

```markdown
# Language Minimal Test

This document contains no metadata.
```

### Override Test

* Do not overwrite current language setting - The plugin should NOT change current DC_Language setting in documents metadata.

```bash
nano plugins/language/tests/md/override/language-with-existing.md
```

```markdown
---
DC_Language: fr-QC
---

# Language Override Test

Plugin should NOT overwrite this language value.
```

## Self-Test Module (`self_test.py`)

* Mirrors the Dublin Core self-test design.

Create:

```bash
nano plugins/language/self_test.py
```

Content:

```python
from pathlib import Path

def run_self_tests():
    print("[language] Running self-tests...")

    root = Path(__file__).resolve().parent
    test_dir = root / "tests" / "md"

    if not test_dir.exists():
        print("[WARN] No test directory found.")
        return True

    for f in test_dir.rglob("*.md"):
        print(f"[OK] Found test file: {f}")

    print("[language] Self-tests completed.")
    return True
```

## Integration Testing With a Language-Rooted Archive

Create the archive using your regional language slugs:

```bash
mkdir -p ../test-archive/{en-ca,fr-qc}/{areas,docs,projects,resources}
```

Copy tests:

```bash
cp -r plugins/language/tests/md/* ../test-archive/en-ca/
```

Apply the plugin:

```bash
./cli/sat-apply-metadata ../test-archive/en-ca/minimal/language-minimal.md
```

### Confirm content changes:

```bash
cat ../test-archive/en-ca/minimal/language-minimal.md
```

Expected output:

```yaml
---
DC_Language: en-CA
---
# Language Minimal Test
```

### Run override test:

```bash
./cli/sat-apply-metadata ../test-archive/en-ca/override/language-with-existing.md
```

Confirmation:

```bash
cat ../test-archive/en-ca/override/language-with-existing.md
```

Expected:

```yaml
---
DC_Language: fr-QC   # preserved, NOT overwritten
DC_Title: __REQUIRED_FIELD_MISSING__
DC_Creator: Christopher Steel
DC_License: https://creativecommons.org/licenses/by-sa/4.0/
DC_Contributor: ChatGPT-5.1 (OpenAI)
---

# Language Override Test

Plugin should NOT overwrite this language value.
```

## Future Enhancements (Upcoming Work)

- Add verbose mode (`--verbose`, `--dry-run`)
- Add profile-based overrides (matching Dublin Core)
- Add expected-output testing in plugin self-tests
- Add “translation scaffolding” plugin interoperability
- Add language inheritance metadata
- Add directory-level language overrides

## License

This document, *Language Plugin MVP: Creation Guide*, by **Christopher Steel**, with AI assistance from **ChatGPT-5.1 (OpenAI)**, is licensed under the Creative Commons Attribution-ShareAlike 4.0 License.

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
