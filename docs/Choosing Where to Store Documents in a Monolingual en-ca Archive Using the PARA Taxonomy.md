# Choosing Where to Store Documents in a Monolingual en-ca Archive Using the PARA Taxonomy

resources

**Suggested slug:** `choosing-document-location-in-monolingual-en-ca-para-archive`

## Introduction

This guide explains how to decide where to place a document inside a monolingual `en-ca` SAT archive that uses the PARA taxonomy.

It relies entirely on the SAT Structure Vocabulary and describes only the physical structure of the archive.

No semantic, metadata, or workflow meaning is implied.

The goal is to provide a clear way to determine which PARA directory becomes the content_root for your document.

## Monolingual en-ca Archive Structure

A monolingual SAT archive that supports only Canadian English has a single language_root:

```bash
archive_root/en-ca/
```

Inside the language_root, the PARA taxonomy defines four top-level taxonomy roots:

```bash
archive_root/en-ca/projects/
archive_root/en-ca/areas/
archive_root/en-ca/resources/
archive_root/en-ca/archives/
```

Every document will live in one of these directories or in a subdirectory of one of them.
Any directory inside these roots becomes a content_root when it contains or is intended to contain human-authored content.

## Choosing a PARA Directory

When deciding where a document should be placed, you choose one of the four PARA taxonomy roots.
PARA provides four physical namespaces:

```bash
projects/
areas/
resources/
archives/
```

Since SAT vocabulary avoids semantics, the choice of namespace is a matter of physical organization.
Below are descriptions to help guide that choice without implying meaning.

### projects

Use `projects/` when the document belongs to a directory that contains a collection of related content under active development.
A project directory becomes a content_root immediately once you place a document such as:

```bash
archive_root/en-ca/projects/my-project/index.md
```

### areas

Use `areas/` when the document is part of a directory that maintains or groups ongoing content that may extend over time.
A directory such as:

```bash
archive_root/en-ca/areas/topic-group/my-document.md
```

is a content_root as soon as a document is placed there.

### resources

Use `resources/` when the document is intended to be physically stored in a place offering reusable, reference, or stable content.
This is often the simplest and most neutral choice in a system that does not yet apply semantic rules.

Example:

```bash
archive_root/en-ca/resources/guides/sat-markdown-style-and-generation-rules/index.md
```

### archives

Use `archives/` when the document belongs to a directory that contains older, historical, or versioned materials.
This directory becomes a content_root when content is placed inside it.

Example:

```bash
archive_root/en-ca/archives/2024/notes.md
```

## Creating a Content Root for a New Document

To create a content_root for your document:

1. Choose one of the PARA taxonomy roots.
2. Create a directory inside it to hold your document.
3. Place your document inside that directory.

For example, creating a content_root for a writing guide:

```bash
archive_root/en-ca/resources/writing-guides/
archive_root/en-ca/resources/writing-guides/index.md
archive_root/en-ca/resources/writing-guides/index.md.assets/
```

The directory `writing-guides/` becomes a content_root as soon as it contains the `index.md`.

## Summary

When storing a document in a monolingual `en-ca` archive using PARA:

- The document must be placed under one of the four PARA roots.
- Any directory inside a PARA root becomes a content_root when content is placed inside it.
- The physical directory structure determines placement.
- The SAT vocabulary does not assign meaning to PARA namespaces; it only describes the structure.

This document provides guidance for choosing a stable and predictable location for your files within the defined SAT framework.
