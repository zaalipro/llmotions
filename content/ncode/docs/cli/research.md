---
title: Deep research
description: Ask a question of the web and get a sourced report from a team of research agents, started and followed from the terminal.
---

Deep research answers one question from the web with its own team of agents and writes a report with sources. It runs in the background: you keep working in the conversation while it does.

{{> shared/research}}

## Starting a research

1. Open **Deep Research** from the [[Ctrl]]+[[P]] palette, or type `/deep_research` with no argument.
2. Choose **New research**. Type the question (it is required) and pick a level: `low` (called **Fastest** in Settings and in the table above), `medium` (the default), `high` or `ultra`.
3. Choose **Start**, or **Cancel**.

The library lists your researches. From it you can open one, and stop, retry or pin it.

> **Note** A research needs at least one [web search engine](/docs/cli/search/) with your key. Set one up first under Settings → Search & web.

![The New research form asking about durable job queues for a local-first Elixir application, with medium selected and Start below.](/assets/shots/cli/research-form.webp)

## Where the reports are

Each research writes a folder with the answer as Markdown (`result.md`) and an HTML report you can open in a browser. The folder is named after the research's id and sits in your home folder (see [Names you may still see](/docs/cli/privacy/#names-you-may-still-see)).

## Using a research in a chat

```text
/deep_research 12
```

attaches finished research number 12 to your next message, so the assistant can work from its findings.

## Research settings in the terminal

The settings above live in Settings → Deep research, and every key is in the [settings reference](/docs/cli/settings-reference/).

<!-- source: C:apps/swarm_code_core/lib/swarm_code/commands.ex:32, C:README.md:223-227, C:apps/swarm_code_cli/lib/swarm_code_cli/ui/library.ex:282,436, C:apps/swarm_code_cli/lib/swarm_code_cli/ui/projector/dialog.ex:878-902, C:apps/swarm_code_core/lib/swarm_code/settings/registry/research.ex:10-22, C:apps/swarm_code_daemon/lib/swarm_code/domain/feature_catalog.ex:158-209, C:docs/settings.md:45-64, C:README.md:237-242, D:lib/swarm_code/research.ex:17,34-47, D:lib/swarm_code/search.ex:145-151,236-247 -->
