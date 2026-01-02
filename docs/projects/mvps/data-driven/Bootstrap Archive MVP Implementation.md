## Bootstrap Archive MVP Implementation

## Description

a **minimal bootstrap implementation** that builds directly on MVP engine, 
No refactors, no framework, no plugins system yet — just *working code*.

------

### New file: `bin/archive-bootstrap.py`

This **reuses the same interpretation logic** and adds one explicit step: directory creation.

```python
#!/usr/bin/env python3

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


def bootstrap(interpreted: dict) -> None:
    created = []
    existing = []

    for path in interpreted["expected_paths"]:
        if path.exists():
            existing.append(path)
        else:
            path.mkdir(parents=True, exist_ok=True)
            created.append(path)

    print(f"Archive: {interpreted['archive_id']}")
    print(f"Root: {interpreted['root']}")
    print()

    if created:
        print("Created directories:")
        for path in created:
            print(f"- {path}")
    else:
        print("No directories needed to be created.")

    if existing:
        print()
        print("Already existed:")
        for path in existing:
            print(f"- {path}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: archive-bootstrap.py <archive.definition.yml>")
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
    bootstrap(interpreted)


if __name__ == "__main__":
    main()
```

------

## Make it executable

```bash
chmod +x bin/archive-bootstrap.py
```

------

## Run it

```bash
./bin/archive-bootstrap.py satellites/archive.definition.yml
```

### Example output

```
Archive: example
Root: /home/initial/projects/sat/dev/sat/archives/example-archive

Created directories:
- /home/initial/projects/sat/dev/sat/archives/example-archive/en-ca/projects
- /home/initial/projects/sat/dev/sat/archives/example-archive/en-ca/areas
- /home/initial/projects/sat/dev/sat/archives/example-archive/fr-qc/projects
- /home/initial/projects/sat/dev/sat/archives/example-archive/fr-qc/areas

Already existed:
- /home/initial/projects/sat/dev/sat/archives/example-archive/en-ca/resources
```

(Rerunning it should create nothing.)

------

## Why this is *exactly* the right next step

- ✔ Reuses interpretation (single source of truth)
- ✔ Explicit execution
- ✔ Idempotent
- ✔ Human-readable report
- ✔ No policy, no guessing, no automation loop
- ✔ Zero commitment to future plugin architecture

This is **MVP 2 completed**.

------

## Stop point (important)

Do **not** add flags yet.
Do **not** merge scripts yet.
Do **not** generalize.

Run it once or twice and answer just this:

> **Did it create exactly what you expected — no more, no less?**

From there, the next pressure point will tell us what to do next (dry-run flag, shared interpreter module, execution plugin shape, etc.).

When you’re ready, tell me:

- **works**
- or **something feels off**