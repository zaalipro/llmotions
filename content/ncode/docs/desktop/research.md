---
title: Deep research
description: Ask one question and let a team of agents search the web, read sources and write a cited report in the background, at four levels of depth.
---

Deep research is for questions that need many sources: comparing libraries, collecting the current state of a technology, checking what changed in an API. You ask once; a lead agent plans the angles, worker agents search and read, and a reporter writes an answer with its sources. It runs on its own: close the page and the rounds keep going.

> **Note** Research needs a web search engine. Set one up first under **Settings → Deep research → Search providers** (see [Providers, models and web search](/docs/desktop/providers/#web-search)). Without an enabled engine, every search fails with "web_search is not configured".

{{> shared/research}}

## Starting a research

1. Click **Deep research** in the rail.
2. Type your question in **What do you want to know?**
3. Pick a level, and optionally tag it with a project or pick a model for this research.
4. Click **Start research** or press [[⌘]]+[[Return]].

<!-- shot: desktop/research-running.png | the Deep research page mid-run at level High: the question, round 2 of 3 in progress, worker agents with progress bars and the headline of round 1 -->

## Following it

The list shows every research with its state. A running one shows its rounds and agents live, and a short headline after each round. You can **Stop** a running research. One that failed or stopped can be retried with **Retry**, or **Retry with…** another model; a research cannot be resumed from the middle.

Pin a research to keep it at the top of the list; delete the ones you no longer need.

## Reading the result

When a research is done:

- **Open report** shows the rendered report in the app, with its sources.
- **Download** saves it.
- The designed report, when it is built, is a richer page of the same answer.

Every research is also saved as files (`result.md`, `report.html` and, if built, `designed.html`) in its own folder; see the Names section of [Data and privacy](/docs/desktop/privacy/) for where.

<!-- shot: desktop/research-report.png | a finished designed research report opened in the app, headline, sections and numbered sources visible -->

## Using a research in a conversation

Type `/deep_research` in the composer to attach a finished research to your next message, or `/deep_research <id>` for a specific one. The assistant then works from what the research found.

## Research settings

**Settings → Deep research** holds the default level, the limits, domain filters, the models of the lead, the workers and the reporter, and when the designed report is built. The table above lists the defaults.

<!-- source: D:lib/swarm_code_web/live/research_live.html.heex:60-215,280-330,390-485, D:lib/swarm_code/research/levels.ex:14-45, D:lib/swarm_code/research.ex:15-47, D:lib/swarm_code/search.ex:144-158, D:lib/swarm_code/engine.ex:1170-1176, D:lib/swarm_code_web/components/chat.ex:90-94, D:lib/swarm_code_web/components/frame.ex:432-440, D:lib/swarm_code_web/live/settings_live.html.heex:211-600 -->
