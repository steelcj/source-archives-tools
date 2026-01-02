## MVP 3— Compare Intent vs Reality

## Key takeaway (worth writing down)

> **Archive definitions declare intent at a semantic level, not a literal directory listing.**

### What this MVP is

> **Given an archive definition and a real filesystem, show where reality diverges from declared intent.**

Nothing more.

------

## What it will do (only)

- Reuse the **same interpreter**
- Look at the **actual filesystem**
- Compare:
  - expected paths (from interpretation)
  - existing paths (on disk)
- Report the difference to a human

No fixing.
No creating.
No deleting.

------

## What it will report

At minimum, three buckets:

1. **Expected but missing**
   - Paths declared by the definition
   - Not present on disk
2. **Present and expected**
   - Paths that match the definition
3. **Present but not declared**
   - Extra directories under the archive root

That’s the whole comparison.

------

## Conceptual flow (clean and familiar)

```
archive.definition.yml
        ↓
   interpreter
        ↓
interpreted structure
        ↓
filesystem inspection
        ↓
diff-style report
```

Still:

- one-shot
- human-invoked
- no automation loop

------

## Why this MVP is high value

This answers questions you *will* ask repeatedly:

- “Did this archive drift?”
- “Is this structure still intentional?”
- “What changed since last time?”

And it does so **without enforcing anything**.

------

## Minimal completion criteria

MVP 3 is complete when:

- Running it on a freshly bootstrapped archive:
  - reports “no differences”
- Running it after manual edits:
  - clearly shows what’s missing and what’s extra
- Output is understandable without reading code

That’s a clean stop.

------

## Naming (provisional, consistent)

Examples that read well:

- `archive-diff.py`
- `archive-compare.py`
- `archive-status.py`

My recommendation: **`archive-diff.py`**
It signals comparison without implying action.

------

## Next concrete step (choose one)

To keep momentum without design sprawl, pick how you want to proceed:

1. **Code it now** (same style as bootstrap, minimal)
2. **Define expected output format first** (what should the report look like?)
3. **Write a short MVP document** (like the bootstrap one)

Say **1**, **2**, or **3** and we’ll do exactly that — nothing extra.