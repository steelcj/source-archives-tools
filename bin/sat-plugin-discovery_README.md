# sat-build-config

## Overview

**`sat-build-config`** is a SAT utility that **builds a resolved configuration view** by discovering available plugins and combining their configuration data into a single, explicit result.

It is designed to support SAT’s goals of **explicit structure**, **inspectability**, and **predictable behavior**, without relying on implicit environment state or hidden defaults.

This tool does not create archives and does not modify archive content.

---

## Purpose

`sat-build-config` exists to answer a simple question:

> *Given the current SAT installation and its available plugins, what does the effective configuration look like?*

It does this by:
- discovering plugins under the SAT `plugins/` directory
- loading plugin-provided configuration fragments
- merging configuration data in a deterministic and inspectable way

---

## Scope and Non-Goals

### In scope

- Plugin discovery
- Configuration loading
- Explicit configuration merging
- Producing a resolved configuration structure

### Out of scope

- Archive creation or modification
- Implicit environment inspection
- Side effects beyond configuration resolution
- Enforcing archive identity or attachment rules

---

## How It Works (High Level)

- The tool determines the **SAT root directory** based on its own location.
- It discovers plugins located under the SAT `plugins/` directory.
- Configuration fragments provided by plugins are loaded.
- Configuration data is merged using explicit, predictable rules.
- The resulting configuration represents the **effective SAT configuration** for the current installation.

All behavior is driven by **declared files and directories**, not by assumptions about the user’s workspace or environment.

---

## Configuration Merging

Configuration values are merged using a **deep merge strategy**:

- Dictionary values are merged recursively.
- Non-dictionary values override earlier values.
- Later configuration sources take precedence over earlier ones.

This ensures:
- local overrides are possible
- defaults remain visible
- no hidden or implicit mutation occurs

---

## Usage

Typical usage:

```bash
sat-build-config