---
Title: "Supporting SAT Users Who Do Not Use Linux"
Description: "A technical response to the SAT user story addressing usage on Windows systems, clarifying supported environments, boundaries, and design decisions."
Author: "Christopher Steel"
Date: "2025-12-31"
License: "CC BY-SA 4.0"
Slug: "user-does-not-use-linux--user-story-response"
---

# Supporting SAT Users Who Do Not Use Linux  
_User Story Response: Technical Boundaries and Windows Considerations_

## Purpose

This document responds to the SAT user story:

> *Alex is in charge of web content and would like to use SAT to create well-formed web content.*

Specifically, it addresses **technical considerations and boundaries** when Alex is working on **Windows** rather than Linux or macOS.

The goal is not to make SAT Windows-native at all costs, but to ensure that:

- SAT behaves predictably on Windows  
- Limitations are explicit and documented  
- Users understand which environments are supported and why  

SAT prioritizes clarity and correctness over silent compatibility hacks.

---

## Design Principle

**SAT is cross-platform, not platform-indifferent.**

SAT tools are written in Python and designed to run anywhere Python runs, but they intentionally rely on **POSIX-like filesystem and execution semantics**. Where Windows differs materially, SAT documents the boundary rather than obscuring it.

This keeps SAT:

- Auditable  
- Maintainable  
- Aligned with professional infrastructure tooling norms  

---

## Python on Windows

### Expectations

SAT requires:

- Python **3.10 or newer**
- A working Python interpreter available to the user

On Windows, Python availability is not guaranteed and is often misconfigured.

### Common Issues

- Python installed but not on `PATH`
- `python` versus `py` command ambiguity
- Microsoft Store Python aliases shadowing real installs
- Multiple Python versions with unclear precedence

### SAT Position

- SAT tools should fail fast if the Python version is unsupported  
- SAT does not attempt to install or manage Python for the user  

### Documentation Requirement

SAT documentation must clearly explain:

- How to verify Python installation
- Which Python versions are supported
- That Microsoft Store Python aliases may need to be disabled

---

## Command Invocation and PATH Semantics

### Current Invocation Model

SAT tools are typically invoked as:

```bash
./bin/sat-tree
```

This assumes:

- Executable file semantics  
- A shell that respects shebangs  

### Windows Reality

This invocation does not work in:

- Windows CMD  
- Default PowerShell configurations  

It does work in:

- WSL  
- Git Bash  
- MSYS2  

### SAT Position

SAT does not support native CMD execution.

This is an explicit boundary, not an oversight.

### Acceptable Windows Environments

- **WSL (preferred)**
- **Git Bash (acceptable)**

These environments provide the filesystem and execution semantics SAT relies on.

---

## Paths, HOME, and Filesystem Differences

### Known Differences

- Linux/macOS use `$HOME` and `/home/user`
- Windows uses `%USERPROFILE%` and drive-letter paths

### SAT Behavior

SAT tools:

- Use `pathlib.Path` for filesystem operations
- Expand user paths explicitly using `expanduser()`

### Configuration Files

- Paths may be relative or absolute
- `~` is supported only because SAT expands it
- No assumption is made about `/home/*` paths

SAT does not attempt to infer platform-specific directory conventions beyond what Python provides.

---

## Line Endings and Text Encoding

### Risk Areas on Windows

- Automatic conversion to CRLF line endings
- Editors saving YAML files as UTF-16
- BOM markers breaking YAML parsing

### Mitigations

- SAT repositories should enforce LF line endings for scripts
- YAML files are expected to be UTF-8 without BOM
- Parsing errors should clearly indicate encoding issues when detected

This is primarily a documentation and tooling hygiene concern.

---

## Executable Permissions

### Constraint

Windows filesystems do not support POSIX executable bits.

### SAT Position

- SAT does not emulate executable permissions
- Execution semantics are delegated to the user’s environment

This reinforces the recommendation to use WSL or Git Bash.

---

## WSL as the Recommended Path

For Windows users, **WSL is the reference environment**.

### Why WSL Works Well

- Native Linux filesystem semantics
- Predictable shell behavior
- Correct handling of permissions, paths, and shebangs
- No Windows-specific branching required in SAT code

This mirrors established practice across many infrastructure tools.

---

## What SAT Explicitly Does Not Do

SAT does not:

- Support native Windows CMD execution
- Introduce Windows-specific code paths
- Hide filesystem or execution differences
- Modify user environments automatically

These are conscious design decisions.

---

## Summary for the User Story

For Alex, a web content manager working on Windows:

- SAT can be used successfully
- A POSIX-like environment (WSL or Git Bash) is required
- Python must be installed and correctly configured
- SAT provides structure and validation, not platform abstraction

This preserves SAT’s core promise:

**SAT enforces structure only where structure is real.**