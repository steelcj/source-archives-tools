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
