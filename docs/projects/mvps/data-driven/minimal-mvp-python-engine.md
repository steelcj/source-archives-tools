# Minimal MVP Python Engine

## MVP engine (Python)

### File: `sat_interpret.py`

```
#!/usr/bin/env python3

print(">>> sat-interpret starting <<<")

import sys
from pathlib import Path

import yaml


def load_definition(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def interpret(definition: dict) -> dict:
    archive = definition.get("archive", {})
    structure = definition.get("structure", {})

    archive_id = archive.get("id")
    root = Path(archive.get("root", ""))

    languages = structure.get("languages", [])
    domains = structure.get("domains", [])

    expected_paths = []

    for lang in languages:
        lang_id = lang["id"]
        for domain in domains:
            domain_id = domain["id"]
            expected_paths.append(root / lang_id / domain_id)

    return {
        "archive_id": archive_id,
        "root": root,
        "expected_paths": expected_paths,
    }


def render(interpreted: dict) -> None:
    print(f"Archive: {interpreted['archive_id']}")
    print(f"Root: {interpreted['root']}")
    print()
    print("Expected structure:")
    for path in interpreted["expected_paths"]:
        print(f"- {path}")

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: sat-interpret.py <archive.definition.yml>")
        sys.exit(1)

    definition_path = Path(sys.argv[1])

    definition = load_definition(definition_path)

    if not isinstance(definition, dict):
        print("Error: archive definition is empty or invalid YAML")
        sys.exit(2)

    if "schema_version" not in definition:
        print("Error: missing required key 'schema_version'")
        sys.exit(2)

    interpreted = interpret(definition)
    render(interpreted)

if __name__ == "__main__":
    main()

```

------

## How to run it

```

python sat_interpret.py archive.definition.yml
```

Example output:

```

Archive: example-archive
Root: /archives/example

Expected structure:
- /archives/example/en/projects
- /archives/example/en/areas
- /archives/example/en/resources
- /archives/example/en/archives
- /archives/example/fr/projects
- /archives/example/fr/areas
- /archives/example/fr/resources
- /archives/example/fr/archives
```

------

## Why this **is** the MVP engine

- It **reads a definition**
- It **interprets it once**
- It **shows what the archive is supposed to look like**
- It exits

No automation loop.
 No background behavior.
 No rules encoded beyond basic traversal.

This is already **data-driven archive behavior** in executable form.

------

## Important: we stop here on purpose

Do **not** add:

- validation
- enforcement
- filesystem writes
- safety checks
- schema logic

Run it.
 Look at the output.
 Feel where it’s awkward or unclear.

That friction tells us what actually matters next.

When you’re ready, the only sensible next questions are:

- “What feels missing?”
- “What feels wrong?”
- “What do I want to *see* differently in the output?”

Say the word, and we iterate **only where the engine pushes back**.