---
title: Agents: panel, hints, overlay
description: Follow every agent of a run in the side panel, jump to one with hint letters, open it full screen, steer it alone or stop it.
---

A big task is split across agents: the assistant or a swarm's lead starts workers, each with its own brief, and every tool call of every agent is its own step. The side panel shows them all at once, and the agent overlay shows one of them in full.

## The side panel

[[Ctrl]]+[[B]] cycles the panel through three sizes:

| Size | What you see |
|---|---|
| full | one row per agent with its name, a status line and one figure |
| compact | a narrower panel |
| hidden | no panel; the transcript takes the width |

Under 120 columns the panel becomes a one-line strip at the edge, or is off. `/panel full`, `/panel compact` and `/panel hidden` set the size directly; your choice is kept for the next session.

Workflow and consensus runs also draw their own sections in the panel: the phases of a workflow, the rounds of a judged plan.

<!-- capture: cli/panel-full | the side panel full during a swarm: five agents sorted by attention, one waiting for an approval at the top, AI status lines, one cost figure | 120x40 -->

<!-- capture: cli/panel-compact | the same swarm with the panel compact | 120x40 -->

## Reading an agent row

Rows are sorted by attention. Each row has:

- **a name** the model gave the agent when it started it (for example "Audit the auth tests");
- **a status line**, a short sentence written by a model about what the agent is doing right now;
- **one figure**; a `$` amount appears only when the agent's cost is known (a price is set for its model).

An agent stopped because it used up its turns is shown as such, not as a finished report.

### AI status lines

The status lines are written by a model. Turn them off with `/panel summaries off` (and back on with `/panel summaries on`), or with **AI status lines** in Settings → Layout & transcript.

## Hint mode

[[Ctrl]]+[[F]] (or [[Ctrl]]+[[Space]]) puts a letter badge before every agent in the panel:

- press an agent's letter to open its overlay;
- press a digit to show one run, `0` for all runs;
- press [[Ctrl]]+[[F]] again to jump to the next approval or question, like [[Ctrl]]+[[N]];
- [[Esc]] cancels.

Hint letters never answer an approval. Hint mode also works over an approval card: the letter opens the overlay of the agent that asked. The letters used for badges can be changed under **Hint letters** in Settings → Keys & input.

<!-- capture: cli/panel-hints | hint mode: letter badges s f g h before five agents in the panel and the footer hint | 120x40 -->

## The agent overlay

A badge letter, or [[Enter]] on an agent row in select mode, opens that agent full screen:

- its request, if it is waiting for you, with the approval keys;
- its life on a time axis;
- its brief and its findings;
- what it did, grouped; `o` lists every raw operation;
- where it sits in the run;
- a composer that steers **only this agent**: a message you send here goes to it, not to the whole run.

| Key | Does |
|---|---|
| `[` / `]` | previous / next agent of the run |
| [[Tab]] | move between the request, the activity and the composer |
| `o` | every raw operation |
| `x` | stop this agent |
| [[Esc]] | back to the chat, at the same scroll and with the same draft |

The approval letters and `o`, `[`, `]` act only while the overlay's composer is empty.

<!-- capture: cli/agent-overlay | the overlay of a worker: brief, time axis, grouped activity with three edits and one command, its composer empty | 120x40 -->

## Runs dashboard and run palette

A conversation can have several runs at once: a chat turn, a swarm, a workflow, a plan. The run tabs above the transcript switch between them ([[Alt]]+[[1]] … [[Alt]]+[[4]]); [[Ctrl]]+[[G]] opens the runs dashboard and [[Ctrl]]+[[R]] the run palette, to find and open a run. `/stop` stops everything running in the conversation.

## What an agent can do

{{> shared/tools}}

## Limits

How many agents may run at once, how deep they may start sub-agents, how many turns each may take and how long a sub-agent may run are settings in **Agents & limits** (by default: 4 at once, depth 2, 60 turns, 30 minutes). Sub-agents work in isolated copies of the project by default, and their changes are merged back when the lead integrates them.

<!-- source: C:README.md:89-101, C:AGENTS.md:217-227, C:docs/keybindings.md:31-38,55-56, C:docs/settings.md:88-98,142,154, C:apps/swarm_code_core/lib/swarm_code/commands.ex:14 -->
