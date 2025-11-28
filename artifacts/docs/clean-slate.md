# Clean Slate


## Move "everything" to artifacts

```bash
mkdir artifacts
mv * artifacts/.
ls -al
git status
git add .
git commit -a 'moved entire project to artifacts dir'
git commit -m 'moved entire project to artifacts dir'
git status
git push
git status
```

### Interpretation

* artifacts/ was created.
* Everything (including directories like core/, plugins/, docs/, etc.) was moved into artifacts/, except for the artifacts/ directory itself (because you moved * into inside artifacts).
* You staged and committed the new structure.
* You pushed it to the remote.

### Result

Your repo root is now empty, containing only:

    artifacts/
    
    .git/
    
    maybe .gitignore, .gitattributes, etc.

This is exactly what a “fresh iteration start” looks like.

# Starting a New Version After Creating a Clean Slate

You have moved the entire project into the `artifacts/` directory and pushed that state to the remote repository. This marks a natural boundary between the previous iteration and the new one. The repository root is now empty and ready for fresh development. This is the ideal moment to begin a new version.

## Tag the Previous Version (Optional but Recommended)

Before declaring the new version, you can tag the final commit of the previous iteration so you can always locate it later.

To inspect recent commits:

```bash
git log --oneline -5
```

Identify the commit just before the “moved entire project to artifacts dir” commit and tag it as version 0.0.3:

```bash
git tag v0.0.3 <commit-hash>
git push --tags
```

This establishes a clear historical boundary for the completion of version 0.0.3.

## Declare the New Version (0.0.4)

The clean-slate commit represents the beginning of the new architecture. Set the repository version to 0.0.4 by creating a new `VERSION` file at the root.

```bash
echo "0.0.4" > VERSION
git add VERSION
git commit -m "Set VERSION to 0.0.4 for new clean-slate iteration"
git push
```

The repository is now marked as version 0.0.4. Any new directories, tools, or plugin architectures you add will be part of this iteration.
