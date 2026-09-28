---
title: Composer, modes and goals
description: Send messages, pick a mode, use slash commands, set goals, attach images and compact a long conversation in the ncode message box.
---

The composer is the message box under the transcript. Everything you ask {{product}} to do starts here: a plain message, a mode, a slash command or a goal.

## Sending

- [[Return]] sends; [[Shift]]+[[Return]] starts a new line. The box grows up to eight lines, then scrolls.
- A message always starts a new turn, even while another run is going. To talk to a running run instead, use the buttons on its card:
  - **↠ Steer** adds your message to the running run; its agent reads it before its next step.
  - **↩ Reply** makes your next message a follow-up of that run, shown under it.
- Stop everything running in the conversation with the **Stop** button or `/stop`.

## Modes

The mode pill at the left of the composer sets how your next message is handled. [[Shift]]+[[Tab]] switches between Build and Plan.

| Mode | What happens |
|---|---|
| 🛠 Build | the assistant reads, writes and runs (the default) |
| ▤ Plan | read-only tools; the result is a step-by-step plan you approve ([Plans you approve](/docs/desktop/plans/)) |
| ◎ Goal | your next message sets a goal to pursue (see below) |
| ⧉ Ultra | big tasks become workflows the assistant runs ([Workflows](/docs/desktop/workflows/)) |
| ⧉ Workflow | your next message authors and launches a workflow |
| ⚖ Consensus | a second model judges the plan first ([Consensus](/docs/desktop/consensus/)) |

<!-- shot: desktop/composer-mode-menu.png | the composer with the mode menu open, listing Build, Plan, Goal, Ultra, Workflow and Consensus with their hints -->

## Model and effort

The model chooser in the composer sets this conversation's two models: the chat model for its own turns and the sub-agent model for the agents it starts. New conversations start with the defaults from Settings. The effort control sets how hard each model thinks. `/effort <level>` and `/swarm_effort <level>` do the same from the keyboard; they accept the levels the current model offers, and a wrong level answers with the valid ones. See [Providers, models and web search](/docs/desktop/providers/).

## Slash commands

Type `/` at the start of the message to open the command list, then keep typing to filter it.

| Command | What it does |
|---|---|
| `/swarm <task>` | start a swarm of agents on a task ([Swarms](/docs/desktop/swarms/)) |
| `/goal <text>` | set a goal every agent keeps in mind |
| `/plan` | switch plan mode on or off |
| `/consensus [task]` | run this turn as a judged plan: planner and judge take turns until the judge approves |
| `/review` | review the uncommitted changes and report problems |
| `/effort <level>` | reasoning effort of this conversation's chat model |
| `/swarm_effort <level>` | reasoning effort of its sub-agent model |
| `/compact [focus]` | summarise the conversation so far and continue from the summary (see below) |
| `/rewind` | restore files to how they were before an earlier turn ([Rewind](/docs/desktop/rewind/)) |
| `/stop` | stop everything running in this conversation |
| `/resume` | resume the last stopped run of this conversation |
| `/workflow <name> [key=value…]` | launch a workflow; `/workflow pause`, `resume`, `stop` or `save` with a run controls one |
| `/workflows` | open the workflow dashboard |
| `/create-workflow [what it should do]` | write a new workflow with the assistant |
| `/ultra` | switch Ultra mode on or off |
| `/deep_research [id]` | attach a finished deep research to this message ([Deep research](/docs/desktop/research/)) |
| `/profile <name>` | switch this conversation to a profile from the project file ([Instructions, memory and project config](/docs/desktop/instructions/)); type it in full, it is not in the list |

Saved workflows and your own commands appear in the same list. If two share a name, a built-in command wins over a workflow, and a workflow over a custom command. See [Commands, agents and skills](/docs/desktop/extend/).

## Goals

A goal is something the conversation keeps working towards across turns. Send `/goal <text>`, or pick Goal mode and type it. {{product}} starts a run that pursues the goal until it is achieved, reports progress and stops when done. The goal is saved with the conversation, so later turns and the agents they start keep it in mind; a conversation can hold more than one open goal.

```text
/goal every public function in lib/ has a doc comment and the docs build without warnings
```

## Images

Paste an image into the composer or drop it on the window. PNG, JPEG, GIF and WebP are accepted, up to 5 MB each and 4 per message. The model needs to support images.

## Compacting a long conversation

Every turn sends the conversation so far to the model. When a conversation gets long, `/compact` has one agent, without tools, write a structured summary: the goal, the decisions made, the files touched, the open threads and the last request. Later turns start from that summary instead of the full history.

- Add a focus to steer the summary: `/compact keep the database migration details`.
- Nothing is deleted. The earlier messages stay in the transcript and in the database; only what the model reads moves.
- A divider card, **⊟ Context compacted**, marks the point and shows how much smaller the context became.

<!-- shot: desktop/composer-compacted.png | the "⊟ Context compacted" divider card in a long seeded conversation -->

<!-- source: D:assets/js/hooks.js:880-882, D:lib/swarm_code_web/components/chat.ex:49-102,119-131,5705-5718,5759,5783,6367-6380, D:lib/swarm_code_web/live/workspace_live.ex:3179-3193,7460-7492,7494-7536,7844-7847, D:lib/swarm_code/engine.ex:14-44,270-288,666-678, D:lib/swarm_code/engine/project_context.ex:37-60, D:lib/swarm_code/conversations/run.ex:155, D:lib/swarm_code/attachments.ex:1-28, D:lib/swarm_code_web/live/settings_live.html.heex:202-205, D:CHANGELOG.md:2071-2084 -->
