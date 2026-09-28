---
title: The ncode CLI
description: ncode in your terminal: a full-screen coding session, a plain line mode and one-shot headless runs, on the same local data as the desktop app.
---

`{{cmd}}` is the terminal side of {{product}}, a local-first coding harness. You talk to an assistant about the project in the current folder; it reads, edits and runs things through tools you can watch, starts helper agents when a job is big, and asks you before it does anything your approval mode does not allow.

Everything stays on your Mac: conversations, runs, settings and your keys live in one local database that the {{product}} desktop app uses too. There is no account and no {{product}} server in the middle. You bring your own model provider key (Anthropic, or any OpenAI-compatible endpoint), and the requests go straight from your Mac to that provider.

<!-- capture: cli/hero | a swarm run in the full-screen session: transcript on the left, the side panel full with four agents, one approval waiting, the status line showing "auto" | 120x40 -->

## Three ways to run it

| How | Command | Use it for |
|---|---|---|
| The full-screen session | `{{cmd}}` or `{{cmd}} ~/dev/app` | everyday work: chat, watch agents, answer approvals and questions |
| One headless turn | `{{cmd}} -p "your prompt"` | a single task from a script; prints the answer and exits |
| Plain mode | `{{cmd}} --plain` | pipes, SSH and terminals where the full screen cannot draw; one command per line |

Two more entry points change settings: `{{cmd}} settings` opens the settings screen on its own, and `{{cmd}} config …` reads and writes settings from scripts.

## What you can do in a session

- **Chat and build.** Ask for a change; the assistant reads files, edits them and runs commands, each step shown as it happens.
- **Run many agents.** `/swarm <task>` starts a team of agents; the side panel shows each one, and you can open any agent and steer it alone.
- **Plan first.** Plan mode and `/plan <task>` produce a read-only plan; Consensus mode has a second model judge the plan before anything changes.
- **Automate.** Workflows are small programs that run agents in phases; deep research answers a question from the web with its own team.
- **Undo.** Every file an agent changes is snapshotted first, so `/rewind` restores the files of an earlier turn.

## How it relates to the desktop app

The CLI and the desktop app are two faces of the same engine and the same database. A conversation started in one can be continued in the other; settings, keys and projects are shared. Only one of them may use the database at a time, and a few background jobs (scheduled tasks, retention) run only in the app. See [Works with the desktop app](/docs/cli/desktop/).

## Requirements

- macOS {{min_macos}} or later on {{arch}}.
- A terminal. At 120 columns or more the side panel is drawn in full; narrower windows get a strip, and a small 80 × 24 window still works. A truecolor terminal such as Ghostty, kitty, WezTerm or iTerm2 draws the richest glyphs.
- A key for a model provider, or a local OpenAI-compatible server such as Ollama or LM Studio.

> **Note** {{product}} {{version}} is a developer preview. It is not notarized by Apple; the [install page](/docs/cli/install/) explains why the one-line installer still works.

## Next steps

1. [Install](/docs/cli/install/) the `{{cmd}}` command.
2. Follow the [Quickstart](/docs/cli/quickstart/): add your provider key and send a first message.
3. Learn [the session screen](/docs/cli/session/) and [approvals](/docs/cli/approvals/).

<!-- source: C:AGENTS.md:9-12, C:AGENTS.md:45-55, C:rel/overlays/bin/swarmcode:15-45, C:README.md:142-171, C:README.md:231-238, C:apps/swarm_code_core/lib/swarm_code/commands.ex:4-50, C:AGENTS.md:195-200, C:AGENTS.md:219-227, C:apps/swarm_code_core/lib/swarm_code/settings/registry/actions.ex:8-80 -->
