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
