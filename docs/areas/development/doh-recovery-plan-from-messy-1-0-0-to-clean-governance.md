# Recovery Plan: From “Messy 1.0.0” to Clean Governance

## Situation

## Situation

SAT reached **version 1.0.0**, establishing a stable, minimal contract for how archives are identified, validated, and interpreted.

Immediately after this milestone, active development continued on `main`, and a number of **unfinished and experimental features** were added directly into the same code path. These changes were made in good faith to preserve progress, but they violated the core assumption of semantic versioning:

> A released version number represents a finished, user-facing contract.

As a result, `main` temporarily contained a mixture of:
- stable 1.0.0 behavior,
- experimental or incomplete features,
- and partially designed future functionality.

This created several risks:
- the meaning of “1.0.0” became ambiguous,
- unfinished features appeared to be part of the stable contract,
- future version bumps became unclear,
- and rollback or migration paths were no longer obvious.

Importantly, **no data was lost and no irreversible damage occurred**.  
The issue is not technical failure, but a **process gap**: SAT crossed from exploratory development into contract-governed software without yet enforcing a separation between *stable guarantees* and *ongoing experimentation*.

The recovery work that follows is about restoring that separation:
- reasserting `main` as the stable, versioned contract,
- relocating experimental work into explicit development channels,
- and establishing clear developer rules so this situation does not repeat.

### Reassurances

You didn’t break anything beyond repair
What you did is *extremely normal* when a project crosses from “working code” into “governed system”.

The key point: **Git already has everything you need to recover cleanly without losing work.**
You do *not* need to delete history or panic-rewrite the repo.

Below is the **cleanest, least destructive recovery plan** that preserves trust **and** your work.

## Goal

- Preserve **all experimental work**
- Restore **`main` as a clean, honest 1.0.0**
- Move unfinished work into **`dev` / experimental containment**
- Avoid rewriting published history unless absolutely necessary

------

## Step 0 — Decide One Thing First (Important)

**Has 1.0.0 already been tagged and shared publicly?**

- **Yes** → *Do NOT rewrite history*
- **No** → *You may still rewrite, but it’s optional*

I’ll give you the **safe path** that works in *both* cases.

------

## Step 1 — Create a Safety Branch (Do This First)

This freezes your current state so nothing is lost.

```bash
git checkout -b rescue/experimental-2026-01
```

This branch is your **“nothing gets lost” guarantee**.

------

## Step 2 — Identify the Last Clean 1.0.0 Commit

Find the commit where 1.0.0 *actually* matched the contract.

```bash
git log --oneline --decorate
```

You are looking for:

- the commit where 1.0.0 behavior was correct
- or the tag `v1.0.0` if it exists

Let’s assume its hash is:

```
abc1234
```

------

## Step 3 — Reset `main` Back to Clean 1.0.0

### If 1.0.0 was published (recommended approach)

Do **not** rewrite history. Instead:

```bash
git checkout main
git revert abc1234..HEAD
```

This:

- creates explicit “undo” commits
- keeps history honest
- makes it obvious what happened

Then:

```bash
git tag -f v1.0.1
```

(1.0.1 = “clean-up patch, no new features”)

------

### If 1.0.0 was *not* published (optional shortcut)

You may hard reset:

```bash
git checkout main
git reset --hard abc1234
git tag v1.0.0
```

This is acceptable *only* if nobody depends on the history yet.

------

## Step 4 — Create a Proper `dev` Branch

Now create a real development branch:

```bash
git checkout -b dev
```

This branch is allowed to be chaotic.

------

## Step 5 — Reintroduce Experimental Work *Intentionally*

Now selectively bring work back from the rescue branch.

### Option A — Cherry-pick entire experimental commits

```bash
git cherry-pick rescue/experimental-2026-01
```

### Option B — Cherry-pick selectively (recommended)

```bash
git cherry-pick <commit1> <commit2> <commit3>
```

As you do this:

- Add `experimental.*` flags
- Rename tools to `sat-experimental-*`
- Add TODO / ROADMAP notes
- Remove anything user-visible by default

This is where you **turn chaos into intention**.

------

## Step 6 — Make the Rules Explicit in the Repo

Add these files to `main` immediately:

```
VERSIONING.md
DEVELOPMENT_VERSIONING.md
ROADMAP.md
```

This prevents future you from repeating this moment.

------

## Step 7 — Lock Down `main`

Adopt this rule (even solo):

- No experimental features on `main`
- No undocumented behavior
- No default changes without version bump
- Tags only from `main`

Mentally treat `main` as **immutable law**, not a workspace.

------

## What *Not* To Do

Do **not**:

- Copy files manually between directories
- Delete the repo and re-clone blindly
- Rewrite history if tags were shared
- Panic squash everything
- “Fix it later”

Git already has your safety net.

------

## The Philosophy Shift (This Is the Real Fix)

You didn’t fail at versioning.

You simply crossed this boundary:

> “SAT is no longer just code — it is a system with promises.”

Every serious project has this exact moment.

------

## One-Line Summary

> **Freeze the mess, restore `main`, move experiments to `dev`, then re-introduce them deliberately.**

If you want next, I can:

- Help you identify the *exact* clean 1.0.0 boundary
- Draft a `ROADMAP.md` that maps experiments → 1.1.0 / 2.0.0
- Propose CI checks to prevent this happening again
- Help design the experimental feature flag layout

You’re actually in a very strong position right now.