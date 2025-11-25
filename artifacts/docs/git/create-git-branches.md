# Create git branches

Create `dev`, `stage`, and `prod` Branches (From Existing `main`)

## Process outline

### Make sure your local repo is synced with GitHub

```bash
git checkout main
git pull origin main
```

------

### Create and push the `dev` branch

```bash
git checkout -b dev
git push -u origin dev
```

This creates the branch locally **and** publishes it on GitHub.

------

### Create and push the `stage` branch

```bash
git checkout main
git checkout -b stage
git push -u origin stage
```

------

### Create and push the `prod` branch

```bash
git checkout main
git checkout -b prod
git push -u origin prod
```

------

# What you now have

### Local branches:

- `main`
- `dev`
- `stage`
- `prod`

### GitHub branches:

- `main`
- `dev`
- `stage`
- `prod`

Everything is correctly connected via `-u` (upstream).

------

# Recommended optional setup

### Protect `prod` and `stage` in GitHub

In GitHub → Settings → Branches → Branch Protection Rules:

- **Prod branch**:
  - Require PR
  - Require approvals
  - Disallow direct pushes
  - Require passing checks (if applicable)
- **Stage branch**:
  - Require PR
  - Allow merges from dev or hotfixes
- **Dev branch**:
  - Optional protections; usually open for developers

------

# Typical workflow after this

```
main → dev → stage → prod
```

Recommended:

- work in feature branches (never directly in dev)
- merge feature → dev → stage → prod
- tag releases on prod

