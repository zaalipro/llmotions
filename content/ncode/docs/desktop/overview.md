---
title: ncode for Mac
description: ncode is a native Mac app where AI agents read, write and run code in your projects, and every run, agent and step shows its progress.
---

{{product}} is a coding assistant that lives in a window on your Mac. You open a project folder, say what you want, and agents read the code, edit files and run commands to get it done. Nothing is hidden: every run, every agent and every step it takes appears on screen with its own progress bar, and you approve what matters before it happens.

<!-- shot: desktop/overview-window.png | the full window, Carbon dark theme, seeded demo project open, a swarm running: transcript on the left, agents pane on the right showing the agent tree with progress bars -->

## What you can do with it

- **Chat about your code.** Ask questions, get explanations, and let the assistant make changes you can review.
- **Plan first.** Plan mode uses read-only tools to write a step-by-step plan you approve before anything changes.
- **Run a team of agents.** A swarm splits a big task between several agents working at the same time, and a lead checks their work.
- **Get a second opinion.** Consensus has a second model judge the plan before any code changes.
- **Automate.** Workflows run agents in a fixed, repeatable order; scheduled tasks run prompts on their own every morning or every Monday.
- **Research the web.** A deep research sends a team of agents to answer one question from many sources and writes a report.
- **Undo.** Every file an agent changes is snapshotted first, so you can rewind a turn.

## How a run works

When you send a message, {{product}} starts a **run**. A run has one top agent: the assistant, a planner or a swarm lead. That agent works in steps: it thinks, then calls tools (read a file, edit a file, run a command, search the web), then thinks again. A lead can start more agents for parts of the task, and they can start their own, a few levels deep.

Every agent and every tool call is its own item in the agents pane, with its status, its progress, the tokens it used and what it cost. You can pause, stop or resume a run at any time.

## Your keys, your models

{{product}} does not come with a model or an account. You bring an API key for Anthropic or for any OpenAI-compatible endpoint (OpenAI, OpenRouter, DeepSeek, a local Ollama or LM Studio server, and others). The [Quickstart](/docs/desktop/quickstart/) walks you through adding one.

Everything else stays on your Mac: conversations, settings and keys live in a local database. See [Data and privacy](/docs/desktop/privacy/).

## Requirements

- A Mac with {{arch}}.
- macOS {{min_macos}} or later.
- An API key for a model provider.

## Also in the terminal

The same engine is available as a terminal app, `{{cmd}}`, which shares the app's projects, conversations and settings. See [Using with the CLI](/docs/desktop/cli/), [Install the CLI](/docs/cli/install/) and the [CLI docs](/docs/cli/).

## Next steps

1. [Install {{product}}](/docs/desktop/install/).
2. [Add your key and send a first message](/docs/desktop/quickstart/).
3. [Take a tour of the window](/docs/desktop/tour/).

<!-- source: D:README.md:1-5, D:lib/swarm_code/engine/run_supervisor.ex, D:lib/swarm_code/engine/agent_server.ex, D:lib/swarm_code/providers/provider.ex:20, D:lib/swarm_code/checkpoints.ex:1-7, D:lib/swarm_code/settings/setting.ex:33-56; requirements: owner decision (plan §3: macOS 15+ on Apple silicon) -->
