# close up shop workflow



In the root of your tools repo:

```bash
git status
```

Confirm the README you edited shows as modified.

Then:

```bash
git add README.md
git commit -m "Add KISS wellbeing archive walkthrough and automation script reference"
git push
```

If you’re on a feature branch:

```bash
git push -u origin <your-branch-name>
```

If you’re committing straight to `dev` (totally fine for this stage):

```bash
git push
```

That’s it — development session safely wrapped.

Sleep mode engaged.