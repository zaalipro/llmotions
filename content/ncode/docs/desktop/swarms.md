---
title: Swarms
description: Split a big task between several agents working in parallel, with a lead that plans, delegates, checks the work and reports.
---

A swarm is a team of agents for one task. A **lead** agent breaks the task into parts, hands each part to a **sub-agent**, the sub-agents work at the same time, and the lead checks their work and reports back to you.

> **Tip** For big work that you want planned, approved and checked by validators, use Ultra mode instead: [Ultra missions](/docs/desktop/missions/).

## Starting a swarm

Type `/swarm` followed by the task:

```text
/swarm add unit tests for every module in lib/billing and make them pass
```

The assistant can also start a swarm on its own when a request is big enough; it uses the same machinery and you see the same cards.

![A swarm run card in the transcript (running, 1/4 sub-agents, 62 ops) beside the agents pane Tree: the Lead waiting for sub-agents above ratelimiter-edge, done, and templates-edge, macros-edge and coreerror-edge with partly filled bars.](/assets/shots/desktop/swarms-running.webp)

## Who does what

- The **lead** plans and delegates. It has no file-editing tools of its own: it reads, starts sub-agents, messages them, waits for their results and verifies.
- **Sub-agents** do the work: they read, edit and run commands under the project's approval mode, like the assistant.
- A sub-agent can be started in the background, so the lead keeps working and gets the result when it arrives.
- Agents can message each other while they work.

Every agent appears in the agents pane with its own progress, tokens and cost; the swarm's card sums them up.

## Models and effort

Sub-agents use the conversation's **Worker model** and its worker effort (`/swarm_effort <level>`). Pick a faster, cheaper model for sub-agents and keep a stronger one for the chat, or the other way round. See [Providers, models and web search](/docs/desktop/providers/).

## Limits

Swarms are bounded so they cannot run away:

| Limit | Default |
|---|---|
| Agents running at once | 4 per run |
| How deep agents may start agents | 2 levels |
| Turns per agent | 60 |
| Time per sub-agent | 30 minutes |

Change them under **Settings → Limits**. See [Limits and isolation](/docs/desktop/limits/).

## Isolated sub-agents

In a git project, sub-agents can each work in their own copy of the project, so parallel edits do not collide. Their changes stay on a branch until the lead merges them. Turn this on or off under **Settings → Limits → Isolate sub-agents in git worktrees**.

## Stopping and resuming

**Stop** on the swarm's card, or `/stop`, stops the lead and every sub-agent. **Resume** starts a new lead that is told what the old workers already finished. See [Watching agents work](/docs/desktop/agents/).

<!-- source: D:README.md:23-26, D:lib/swarm_code/tools.ex:12-50, D:lib/swarm_code/engine.ex:1170-1176, D:CHANGELOG.md:286-292, D:lib/swarm_code/settings/setting.ex:33-56,42,124, D:lib/swarm_code_web/live/settings_live.html.heex:1440-1560, D:lib/swarm_code/engine/isolation.ex:1-25 -->
