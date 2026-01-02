# archive-diff.py--cross-platform-compatible-report

**Your `archive-diff.py` script is cross-platform and will work on Windows, macOS, and Linux — with one critical dependency note.**

---

## Why It Works Cross-Platform

### 1. **Shebang (`#!/usr/bin/env python3`)**
- Ignored on Windows — fine.
- Works on macOS/Linux.
- No change needed.

### 2. **`pathlib.Path`**
- Fully cross-platform — handles `/` vs `\` automatically.
- Safe.

### 3. **`yaml.safe_load()`**
- Uses `PyYAML`, which is cross-platform.
- Works everywhere — **but requires `PyYAML` to be installed**.

> **Critical**: This script depends on `PyYAML` — **not in the Python standard library**.

You must install it:
```bash
pip install PyYAML
```

This is true on **all platforms** — Windows, macOS, Linux.

### 4. **`path.open(..., encoding="utf-8")`**
- Explicit encoding — avoids platform-specific default encoding issues.
- Safe.

### 5. **`path.rglob("*")`**
- Cross-platform — recursively finds all files/dirs.
- Safe.

### 6. **`path.is_dir()`**
- Cross-platform — works on all OSes.
- Safe.

### 7. **No OS-specific calls**
- No `os.system`, `subprocess`, `ctypes`, or file permissions — all safe.
- No issues.

### 8. **CLI via `sys.argv`**
- Works on all platforms.
- Fine.

---

## Optional Improvements (Not Required)

### 1. **Add `PyYAML` to `requirements.txt` (recommended)**
Create a `requirements.txt` file:
```
PyYAML>=6.0
```

Then users can install with:
```bash
pip install -r requirements.txt
```

### 2. **Handle Windows line endings (optional)**
Not needed — YAML doesn’t care about line endings.

### 3. **On Windows: Use `py` launcher**
Run it via:
```cmd
py archive-diff.py archive.definition.yml
```

### 4. **Make executable on macOS/Linux**
```bash
chmod +x archive-diff.py
```

---

## Testing

Test on each platform by:
1. Install `PyYAML`:
   ```bash
   pip install PyYAML
   ```
2. Create a sample `archive.definition.yml`:
   ```yaml
   schema_version: "1.0.0"
   archive:
     id: "my-archive"
     root: "./content"
   structure:
     languages:
       - id: "en"
       - id: "fr"
     domains:
       - id: "docs"
       - id: "media"
   ```
3. Create some directories manually under `./content/` (e.g., `./content/en/docs`, `./content/en/extra`).
4. Run:
   ```bash
   ./archive-diff.py archive.definition.yml
   ```
5. Verify output shows:
   - Expected but missing
   - Expected and present
   - Present but not declared

---

## Final Verdict

> **Your script is cross-platform — but requires `PyYAML` to be installed.**

It will work on **Windows, macOS, and Linux** with Python 3.7+ and `PyYAML` installed.

---

## Critical Note

If you distribute this script, **always include a `requirements.txt`** or document the dependency:

> **Dependency**: `PyYAML` — install with `pip install PyYAML`

Without it, the script will fail with:
```
ModuleNotFoundError: No module named 'yaml'
```

---

You’re good to go — just remind users to install `PyYAML`!

Let me know if you want to:
- Add error handling for missing `PyYAML`.
- Add a `--quiet` or `--json` output mode.
- Bundle it with a `setup.py` or `pyproject.toml`.

Happy diffing!