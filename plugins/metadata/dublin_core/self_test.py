from pathlib import Path
import yaml

from core.plugin_loader import load_plugin, load_plugin_config  # type: ignore


REPO_ROOT = Path(__file__).resolve().parents[3]
EXAMPLES_DIR = REPO_ROOT / "plugins" / "metadata" / "dublin_core" / "examples"


REQUIRED_FIELDS = ["DC_Title", "DC_Creator", "DC_Language", "DC_License"]


def run_self_tests() -> bool:
    plugin_id = "metadata.dublin-core"
    plugin_info = load_plugin(plugin_id)
    config = load_plugin_config(plugin_info)
    apply_fn = plugin_info["callable"]

    example_files = [
        "minimal.yml",
        "defaults.yml",
        "custom.yml",
        "complete.yml",
    ]

    all_ok = True

    for name in example_files:
        path = EXAMPLES_DIR / name
        if not path.exists():
            print(f"[FAIL] Example missing: {path}")
            all_ok = False
            continue

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        updated = apply_fn(data, config)

        # Basic checks: required fields present and not placeholder
        for field in REQUIRED_FIELDS:
            value = updated.get(field)
            if value in (None, "", "__REQUIRED_FIELD_MISSING__"):
                print(f"[FAIL] {name}: field {field} invalid ({value!r})")
                all_ok = False

        if all_ok:
            print(f"[OK] {name}")

    return all_ok


def main():
    ok = run_self_tests()
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
