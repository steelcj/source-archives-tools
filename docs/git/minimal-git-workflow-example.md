# Minimal git workflow example

Here is a clean, safe, minimal **git workflow** to set your repository to **version 0.0.1**, commit everything, tag it properly, and push to the **dev** branch.

This assumes:

- You are **inside the tools repo** (`~/projets/archives-sources/outils` or similar)
- You have a working Git remote (GitHub / GitLab)
- You want a clean versioned checkpoint before further development
- You already created a *dev* branch earlier (if not, I give the commands)

------

# ✔ Step 1 — Ensure You're on the `dev` Branch

```bash
git checkout dev
```

If the branch does not exist yet:

```bash
git checkout -b dev
```

------

# ✔ Step 2 — Check What Will Be Committed

```bash
git status
```

Make sure you see:

- `scripts/init-archive.sh`
- updated `README.md`
- the early `standards/` directory
- any other files you added

If anything should **not** be committed, ignore it now:

```bash
echo "filename-or-dir" >> .gitignore
```

------

# ✔ Step 3 — Add All New/Modified Files

```bash
git add -A
```

------

# ✔ Step 4 — Commit With a Versioned Message

```bash
git commit -m "v0.0.1 - Initial KISS tooling, init script, README, minimal standards structure"
```

------

# ✔ Step 5 — Tag the Release

This is optional, but HIGHLY recommended.

```bash
git tag -a v0.0.1 -m "Initial development version 0.0.1"
```

------

# ✔ Step 6 — Push Both the Branch and Tag to the Remote

```bash
git push origin dev
git push origin v0.0.1
```

If your remote uses another name instead of **origin**, just adjust accordingly.

------

# ✔ Step 7 — (Optional) Confirm Everything

List local tags:

```bash
git tag
```

List remote tags:

```bash
git ls-remote --tags
```

Confirm dev branch is up-to-date:

```bash
git log --oneline --decorate --graph -n 10
```

------

# If You Want, I Can Produce:

- A **CHANGELOG.md** with entry for `0.0.1`
- A **semantic versioning plan**
- A **README badge** for versioning (no icons if you prefer)
- A **GitHub release text** for the v0.0.1 tag
- A **pre-commit hook** for version bumping
- A **script bump-version.sh**

Just tell me what you want next.