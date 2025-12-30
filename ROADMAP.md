## Next Step (Immediate): Phase 3 — SAT Identity Enforcement

### Goal

Make **every SAT tool refuse to run** unless SAT identity is valid.

### What this gives you

- No more “half-initialized” states
- Predictable behavior across tools
- A single mental model: *SAT exists → SAT is trusted*

### Minimal work

Create **one shared helper** and reuse it everywhere.

#### Example (conceptual)

```
from sat_identity import require_valid_sat_identity
require_valid_sat_identity()
```

**Rules enforced**

- `VERSION` exists
- `meta/sat.manifest.yml` exists
- `sat_version` matches `VERSION`
- Fail early, loudly, consistently

This is cheap and pays off forever.

## Phase 4 — Content Archive Contract Lock-in

### Goal

Define exactly what a **content archive must contain**.

Minimum invariants:

- `config/archive.yml`
- `meta/archive.manifest.yml`
- `archive_type: content`
- `sat_id` + `sat_version` present

Once locked:

- `sat-tree`
- `sat-validate`
- `sat-doctor`

## Phase 5 — Satellites Directory Formalization

(Keep Low Risk)

### ChatGTP wants nail things down now but I will not let it

But what I want is roughly this:

Right now:

- `satellites/` is **just a directory**
- Likely **top-level**
- Its role is **emergent**, not fixed
-  *directional intuition* is to enable the SAT to contact Archives

Time *will* be allowed to shape this.

### honest mental placeholder (not a rule)

Instead of a hard statement, hold this **working understanding**:

> For now, `satellites/` does not alter archive behavior,
>  but it is a candidate location for SAT-to-archive relationships.

That leaves room for:

- discovery
- indexing
- registry-like data
- egress or ingress of artifacts
- coordination metadata

…without pretending like we already know which ones are right.

## What has been decided

- Archives remain **self-contained**
- Their correctness does **not depend** on `satellites/` nor an "attached" SAT.

These are important invariants, other things can evolve. For the moment:

> Nothing in `satellites/` influences SAT behavior unless a tool is explicitly told to read it.

- ie. Never read from it with out considering the very loose coupling intended.
- Prevent “magical behavior” later.

## **When You’re Ready (Explicit Mutation Phase)**

Only *after* the above is stable:

- `sat-upgrade-version`
- `sat-migrate-archives`
- `sat-doctor --fix` (opt-in repairs)

These tools are safe *because* you delayed them.

------

## If you want a concrete next move

I recommend **Phase 3** next.

If you want, I can:

- write the shared `sat_identity.py` helper
- or refactor `sat-init-archive` to depend on it
- or sketch the exact error taxonomy for SAT tools

Just say the word.