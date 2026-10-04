---
title: Settings
description: One full-screen layer for every setting of ncode and of this terminal: open it, find a setting, see where its value comes from, change it and undo.
---

Every setting the desktop app has, and this terminal's own, are in one full-screen layer. Changes you make here are the same ones the desktop app sees, because both use the same database.

## Opening Settings

| From | How |
|---|---|
| a session | [[F2]], or `/settings` (also `/config`, `/prefs`) |
| a session, at one place | `/settings <what>`, for example `/settings theme` |
| the palette | **Settings** in [[Ctrl]]+[[P]]; `>settings:theme` lists single settings |
| a shell | `{{cmd}} settings`, or `{{cmd}} settings <what>` |

`<what>` is a section, a key (`limits.max_agent_depth`), a label or a synonym; Settings opens with the cursor on that row. `{{cmd}} settings providers` opens at Providers even when no provider is set up yet, which makes it the place to start on a new Mac.

`{{cmd}} settings` needs a terminal. From a script, use [`{{cmd}} config`](/docs/cli/config/) instead.

![Providers in Settings, with the section rail, Anthropic and OpenRouter providers, masked keys, model counts and footer shortcuts.](/assets/shots/cli/settings-overview.webp)

## Sections

22 sections hold about 170 settings:

- **Overview**
- **Models & effort**, **Providers** (presets, pasted keys, fetching model lists, effort levels), **Pricing**
- **Search & web** (engines in fallback order, readers), **Deep research**, **MCP servers**, **Language servers**
- **Agents & limits**, **Approvals & trust**, **Project file**, **Memory & instructions**, **Library** (commands, agents, skills, workflows)
- **Appearance**, **Layout & transcript**, **Keys & input** (rebind any action), **Session & startup**
- **Storage** (measure, clean up, vacuum, retention), **Budget & usage**
- **Desktop app**, **Files & environment** (the doctor), **Import & export**

The [settings reference](/docs/cli/settings-reference/) lists every key with its default.

## Moving around

| Key | Does |
|---|---|
| `[` / `]` | previous / next section |
| `/` | search every setting, provider, server and key |
| `?` | the keys of this page |
| [[Esc]] | back one level; on a section page, close Settings |
| `q` | close Settings from anywhere |

The footer lists only the letters the focused row answers to, in its own words, such as `t test the connection`.

Under 120 columns the section rail becomes a strip across the top; at 80 × 24 the pages drill down one level at a time, and [[Esc]] goes back up.

## Where a value comes from

Every row says which layer its value comes from:

| Source | Meaning |
|---|---|
| `default` | nobody changed it |
| `global` | set in the shared database; the desktop app sees the same value |
| `project` | set for this project |
| `this conversation` | set for the open conversation only |
| `cli` | this terminal's own setting, kept in `cli.json` beside the database |
| `flag` | a command-line flag of this session, such as `--model` |
| `env` | an environment variable wins while it is set, for example `{{env_prefix}}THEME=light` |

## Changing and undoing

- **Writes are compare-and-set.** If the value was changed elsewhere since you opened the page (in the desktop app, or by a `{{cmd}} config` command), the row shows `changed elsewhere` instead of overwriting it.
- **`u` undoes** the last change of this session, also after you closed and reopened Settings.

## Keys are never shown

Provider and search keys are pasted, never typed out or shown. The row reads `●●●●●●●● set · ends 4f2a`. A new or replaced key is tested against its endpoint before it is saved; if the test fails, `s` saves it anyway. Keys never reach the screen, the logs, undo, search results or exports.

## Slow work

Testing a key, fetching a model list, probing an MCP server and measuring storage run as a task with its seconds shown. `c` cancels it, and leaving the page cancels what it started.

<!-- source: C:README.md:231-263, C:README.md:276-281, C:rel/overlays/bin/swarmcode:19-27,146-162,248-257, C:docs/keybindings.md:740-748, C:docs/settings.md:1-9, C:AGENTS.md:261-264 -->
