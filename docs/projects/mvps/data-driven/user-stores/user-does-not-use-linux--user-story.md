Here’s a clean, well-formed **SAT user story**, written in a way that fits both agile conventions *and* the philosophy you’re developing around SAT.

------

## SAT User Story — Web Content Creation

**Title:** Create well-formed web content using SAT

**User:** Alex (Web Content Manager)

**Story:**

> **As a** web content manager,
> **I want** to use Source Archive Tools (SAT) to create well-formed web content,
> **so that** the content is structurally consistent, metadata-complete, and ready for publication across supported web platforms.

------

## Context

Alex is responsible for creating and maintaining web content. Their priorities include:

- Clear, predictable structure
- Correct and complete metadata
- Minimal manual formatting errors
- Confidence that content is publication-ready

Alex is **not** trying to design the entire site architecture or enforce linguistic equivalence across languages. They want reliable tooling that supports good content practices without over-constraining meaning or creativity.

------

## Acceptance Criteria

- SAT provides a clear, guided way to create new content items
- Required structural elements (paths, filenames, directories) are validated
- Required metadata fields are present or sensibly defaulted
- Content can be written in plain Markdown without generator-specific lock-in
- Output is compatible with common static-site workflows (e.g., MkDocs)
- Errors are reported clearly and early, without destructive side effects

------

## Out of Scope (Explicit)

- Automatic semantic equivalence across languages
- Forced structural identity between translated content
- Opinionated editorial voice or content meaning

SAT supports *well-formedness*, not *authorship*.

------

## Notes (Design Alignment)

This user story intentionally frames SAT as:

- A **content integrity tool**, not a CMS
- A **human-first system** that assists rather than dictates
- A tool that enables *good defaults* while allowing informed deviation

This aligns directly with SAT’s core boundary:
**structure is enforced only where structure is real**.

------

If you’d like, next we can:

- Expand this into multiple user stories (author, reviewer, translator, publisher)
- Convert it into a full MVP epic
- Map this story directly to existing or planned SAT commands (`sat-init-archive`, `sat-tree`, metadata plugins)
