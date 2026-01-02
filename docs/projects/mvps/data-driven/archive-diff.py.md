# archive-diff.py

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

    expected_paths = set()

    for lang in languages:
        lang_id = lang["id"]
        for domain in domains:
            domain_id = domain["id"]
            expected_paths.add(root / lang_id / domain_id)

    return {
        "archive_id": archive_id,
        "root": root,
        "expected_paths": expected_paths,
    }


def collect_existing_paths(root: Path) -> set[Path]:
    existing = set()

    if not root.exists():
        return existing

    for path in root.rglob("*"):
        if path.is_dir():
            existing.add(path)

    return existing


def diff(interpreted: dict) -> None:
    root = interpreted["root"]
    expected = interpreted["expected_paths"]
    existing = collect_existing_paths(root)

    expected_missing = sorted(p for p in expected if not p.exists())
    expected_present = sorted(p for p in expected if p.exists())
    # Build full set of declared paths including parents
    declared = set()

    for path in expected:
        declared.add(path)
        parent = path.parent
        while parent != root and parent not in declared:
            declared.add(parent)
            parent = parent.parent

    extra = sorted(
        p for p in existing
    if p not in declared and p != root
    )

    print(f"Archive: {interpreted['archive_id']}")
    print(f"Root: {root}")
    print()

    if expected_missing:
        print("Expected but missing:")
        for path in expected_missing:
            print(f"- {path}")
    else:
        print("Expected but missing: none")

    print()

    if expected_present:
        print("Expected and present:")
        for path in expected_present:
            print(f"- {path}")
    else:
        print("Expected and present: none")

    print()

    if extra:
        print("Present but not declared:")
        for path in extra:
            print(f"- {path}")
    else:
        print("Present but not declared: none")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: archive-diff.py <archive.definition.yml>")
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
    diff(interpreted)


if __name__ == "__main__":
    main()
```

