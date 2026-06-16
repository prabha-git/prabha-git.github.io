---
draft: true
date: 2026-06-06
slug: jargon-i-was-fuzzy-on
tags:
  - engineering
  - programming
  - learning-in-public
authors:
  - Prabha
---

# Jargon I Nodded Along To: Fundamentals I Was Quietly Fuzzy On

> DRAFT / running capture. Separate from the Claude Architect learning journal. This collects the small, foundational concepts I realized I did not actually know cold (the words you nod along to in meetings and docs). Each one is a candidate for a short explainer. Honest capture; the value is admitting the gap.

## Capture protocol

Each concept gets: the term, the moment it came up, what I assumed, the plain-English definition, the one detail that actually matters, and where it shows up. Appended as concepts surface, across any topic.

<!-- more -->

---

## Glob

- **Came up in:** Claude Code `.claude/rules/` `paths:` frontmatter (and Cursor's `globs:`).
- **What I assumed:** Vaguely "wildcard file matching", but not the exact rules.
- **Plain English:** A pattern for matching file paths using wildcards. The name comes from an old Unix command, `glob` (short for "global"), that expanded wildcard patterns in the 1970s. It is the `*.txt` style you already use in the shell.
- **Core wildcards:**
  - `*` = any characters, but NOT across `/` (one path segment). `*.ts` matches `a.ts`, not `src/a.ts`.
  - `**` = any characters INCLUDING `/` (recursive, cross-directory). `src/**/*.ts` matches `src/a.ts` and `src/api/v1/b.ts`.
  - `?` = exactly one character.
  - `[abc]` / `[0-9]` = one character from a set or range.
  - `{a,b}` = brace expansion (alternatives). `*.{ts,tsx}`.
- **The detail that actually matters:** `*` stops at `/`; `**` crosses `/`. That single difference is "this folder only" vs "everything under here". This is the thing people get wrong.
- **NOT regex:** glob is the friendly path-oriented subset. In glob, `.` is a literal dot, not "any char"; `*` is roughly regex `.*`. Do not mix the two syntaxes.
- **Shows up in:** `.gitignore`, shell (`ls *.log`), `.claude/rules/` and Cursor rules, `tsconfig` includes, CI path filters, build configs. Nearly the same syntax everywhere.

---

## Candidate framing for the blog

- Angle: "The foundational terms senior engineers quietly fuzz over." Self-deprecating, honest, useful.
- Each entry is short and standalone, so the post can grow over time or be sliced into a series.
