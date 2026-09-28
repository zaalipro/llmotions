---
title: Modes and run types
description: The six conversation modes, and the kinds of run you can start - chat, plan, goal, consensus, swarm, review, workflow and compact - plus model and effort.
---

A conversation has a **mode** that shapes what your next message does, and each message you send starts a **run**. Several runs of one conversation can work side by side; each has its own tab above the transcript.

## The six modes

| Mode | What your next message does |
|---|---|
| Build | the default: the assistant reads, writes and runs commands to do the task |
| Plan | the assistant uses read-only tools and answers with a step-by-step plan |
| Goal | the message sets a goal the conversation pursues |
| Ultra | big tasks become workflows the assistant writes and runs |
| Workflow | the message authors and launches a workflow |
| Consensus | a second model judges the plan before anything changes |

`/plan` and `/ultra` turn their mode on and off, and `/consensus` alone switches to Consensus. **Mode** in Settings → Models & effort sets Build, Plan, Consensus, Ultra or Workflow (shown as "Writing a workflow") for this conversation. Goal has no switch in the terminal: `/goal <text>` sets a goal and starts on it at once.

## Plan

`/plan` turns plan mode on or off. `/plan <task>` plans that task right now, as a read-only run beside whatever else is running, without changing the mode.

## Goal

`/goal <text>` sets the conversation's goal, which every agent keeps in mind. `/goal` alone shows the current goal and its report; [[PgUp]] / [[PgDn]] and [[Home]] / [[End]] scroll a long one.

## Ultra and Workflow

`/ultra` turns Ultra on or off: the assistant handles big tasks by writing and running [workflows](/docs/cli/workflows/). `/create-workflow <what it should do>` writes one with you, once.

## Consensus

`/consensus` alone switches the conversation to Consensus mode. `/consensus <task>` runs that one turn as a judged plan without changing the mode: a planner writes a plan, a judge model checks it against a list of checks over one or more rounds, and only then an implementer carries it out. In Settings, per conversation:

| Setting | Default |
|---|---|
| Consensus checks | 7 of the 12 checks are on; tick them on or off in Settings |
| Consensus rounds | 2 |
| Judge model | the sub-agent model |
| Implementer model | the planner implements |

<!-- capture: cli/consensus-verdict | a consensus run in the transcript: the plan, the judge's verdict per check, and the panel showing the round section | 120x40 -->

## Swarm

`/swarm <task>` starts a team: a lead agent splits the task and starts workers, and you follow them in the [side panel](/docs/cli/agents/). A swarm starts at once, beside any running turn.

## Review

`/review` reviews the uncommitted changes in the project and reports problems.

## Compact

`/compact` summarises the conversation so far and continues from the summary. `/compact <focus>` tells it what to keep. Sent while a turn runs, it waits until the turn ends.

## Model and effort {#model-and-effort}

| Command | Changes |
|---|---|
| `/model` | this conversation's chat model; alone, it opens a picker with the model in use first |
| `/model <model>` | set it directly |
| `/swarm_model …` | the model the conversation's sub-agents use |
| `/effort <level>` | how hard the chat model thinks: `low`, `medium`, `high`, `max`; `none`, `minimal` and `xhigh` where the model offers them |
| `/swarm_effort <level>` | the same for the sub-agents |

`/model` also accepts `<provider_id>|<model>` to name the provider as well. `/effort` accepts only the levels the conversation's model offers. To try another model for one session without changing the conversation, start `{{cmd}} --model <model>` (or `--model provider/model`); nothing is written, and an explicit `/model` ends it. [Providers and models](/docs/cli/providers/) covers the defaults per role.

<!-- source: C:apps/swarm_code_core/lib/swarm_code/commands.ex:4-34, C:apps/swarm_code_core/lib/swarm_code/commands.ex:68-78,200-224,245-296, C:apps/swarm_code_core/lib/swarm_code/settings/registry/session.ex:9-22,91-105,130-142, C:apps/swarm_code_daemon/lib/swarm_code/daemon/service/command_dispatcher.ex:143-165, C:README.md:155-158, C:README.md:223-228, C:AGENTS.md:45-51, C:AGENTS.md:241-245, C:docs/settings.md:15-37, C:docs/research/2026-09-23-pass70-outcome.md:31-32 -->
