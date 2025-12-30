#!/usr/bin/env python3
"""
sat-bootstrap: Establish SAT identity if missing.

Contract:
- Creates sat/meta/sat.manifest.yml if it does not exist.
- Never modifies existing identity files.
- Fails if identity exists but conflicts with VERSION.
- Uses sat/VERSION as the single source of truth for versioning.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional
import sys

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

BIN_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BIN_DIR.parent

VERSION_FILE = PROJECT_ROOT / "VERSION"
SAT_MANIFEST = PROJECT_ROOT / "meta" / "sat.manifest.yml"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_version() -> str:
    if not VERSION_FILE.exists():
        sys.exit(f"Error: VERSION file not found at {VERSION_FILE}")
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def parse_sat_manifest(path: Path) -> tuple[Optional[str], Optional[str]]:
    sat_id = None
    sat_version = None

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("sat_id:"):
            sat_id = stripped.split(":", 1)[1].strip().strip('"')
        elif stripped.startswith("sat_version:"):
            sat_version = stripped.split(":", 1)[1].strip().strip('"')

    return sat_id, sat_version


def write_sat_manifest(version: str) -> None:
    SAT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    content = (
        'sat_id: "sat"\n'
        'sat_label: "Source Archive Tools"\n'
        f'sat_version: "{version}"\n'
    )
    SAT_MANIFEST.write_text(content, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    version = read_version()

    if SAT_MANIFEST.exists():
        sat_id, manifest_version = parse_sat_manifest(SAT_MANIFEST)

        if sat_id != "sat":
            sys.exit(
                "Error: Existing sat.manifest.yml has invalid sat_id\n"
                f"  Expected: sat\n"
                f"  Found:    {sat_id}"
            )

        if manifest_version != version:
            sys.exit(
                "Error: SAT identity already exists but version mismatch detected\n"
                f"  meta/sat.manifest.yml: {manifest_version}\n"
                f"  VERSION:               {version}\n\n"
                "Refusing to modify existing identity.\n\n"
                "For users:\n\n"
                "  See the upgrade documentation or use a dedicated SAT upgrade tool.\n\n"
                "For developers:\n\n"
                "  If you want to update to match the latest SAT version you can delete\n"
                "  meta/sat.manifest.yml and it will be recreated by running this again\n\n"
                "  If you want to manually change the (backdate?) the SAT version you can\n"
                "  editing the version directly in meta/sat.manifest.yml and review any\n"
                "  managed archives for compatibility.\n"
            )

        print("SAT identity already established and valid.")
        return 0

    write_sat_manifest(version)

    print("SAT identity established.")
    print(f"  sat_id: sat")
    print(f"  sat_version: {version}")
    print(f"  location: {SAT_MANIFEST}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
