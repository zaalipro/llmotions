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

![The full side panel during a five-agent swarm, with Verify changes waiting for approval first, followed by Ticket flow, Regression audit, Docs polish and the Lead; short model-written status lines, turn counts, and $0.05 spent are visible.](/assets/shots/cli/panel-full.webp)

![The same five-agent swarm with the compact side panel: the pending verification command above compact rows for Verify changes, Ticket flow, Regression audit, Docs polish and the Lead, with $0.05 spent and the Panel compact confirmation in the status line.](/assets/shots/cli/panel-compact.webp)

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
- press a digit to show one run, or `0` to open the runs dashboard (every run);
- press [[Ctrl]]+[[F]] again to jump to the next approval or question, like [[Ctrl]]+[[N]];
- [[Esc]] cancels.

Hint letters never answer an approval. Hint mode also works over an approval card: the letter opens the overlay of the agent that asked. The letters used for badges can be changed under **Hint letters** in Settings → Keys & input.

![Hint mode in the full swarm panel, with orange s, f, g, h and j badges for Verify changes, Ticket flow, Regression audit, Docs polish and the Lead, a 1 run badge, and the footer s-j open, 1 run, Ctrl-F again needs you, Esc.](/assets/shots/cli/panel-hints.webp)

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
| `x` | stop this agent (asks first) |
| [[Esc]] | back to the chat, at the same scroll and with the same draft |

The approval letters and `o`, `[`, `]`, `x` act only while the overlay's composer is empty. Here `a` is a second key for "allow once", beside `y`.

![The Ticket flow worker overlay with its life timeline and brief, grouped activity showing three documentation-file writes and git status --short, the run's agent tree, three changed files, token and turn counts, and an empty composer that steers only Ticket flow.](/assets/shots/cli/agent-overlay.webp)

## Runs dashboard and run palette

A conversation can have several runs at once: a chat turn, a swarm, a workflow, a plan. The run tabs above the transcript switch between them ([[Alt]]+[[1]] … [[Alt]]+[[4]]); [[Ctrl]]+[[G]] opens the runs dashboard and [[Ctrl]]+[[R]] the run palette, to find and open a run. `/stop` stops everything running in the conversation.

## What an agent can do

{{> shared/tools}}

## Limits

How many agents may run at once, how deep they may start sub-agents, how many turns each may take and how long a sub-agent may run are settings in **Agents & limits** (by default: 4 at once, depth 2, 60 turns, 30 minutes). Sub-agents work in isolated copies of the project by default, and their changes are merged back when the lead integrates them.

<!-- source: C:README.md:89-101, C:AGENTS.md:217-227, C:docs/keybindings.md:31-38, C:docs/keybindings.md:660-661,706, C:apps/swarm_code_cli/lib/swarm_code_cli/ui/keymap/bindings.ex:225-233,55-56, C:docs/settings.md:88-98,142,154, C:apps/swarm_code_core/lib/swarm_code/commands.ex:14 -->
