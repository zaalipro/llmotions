---
title: Watching agents work
description: Read the agents pane: agent cards, tree and grid, progress and cost, the timeline inspector, the Changes view, pausing, stopping and resuming runs.
---

Every run in {{product}} is a small team: one top agent, the agents it starts, and every tool call each of them makes. The agents pane on the right of the window shows all of it while it happens, so you always know what is going on and what it costs.

## Agent cards

The **Agents** view shows one card per agent: its name and task, its status (running, waiting for you, done, failed, stopped), a progress bar, the model it uses, the tokens it has used and what they cost. Under each agent, its tool calls appear as rows: the file it read, the command it ran, the search it made.

- **Tree** shows who started whom: the lead at the top, its sub-agents below it, their own sub-agents below them.
- **Grid** lays the same cards side by side, which is easier to scan when many agents run at once.
- **Full cards** show everything; **Compact cards** show one line per agent.

<!-- shot: desktop/agents-tree.png | the Agents view as a Tree during a swarm in the seeded demo project: a lead with three sub-agents, progress bars partly filled, token and cost figures visible -->
<!-- shot: desktop/agents-grid.png | the same swarm in the Grid layout with Compact cards -->

Everything that waits for you (an approval, a question) is marked on its agent and in the transcript.

## The timeline

The **Timeline** view puts every step of every agent on a time axis, so you can see what ran in parallel, what waited and what took long. Click a step to open the inspector: the step whole, with its full input and output.

<!-- shot: desktop/agents-timeline.png | the Timeline view of a finished swarm with the inspector open on one run_command step -->

## Changes

The **Changes** view lists the files the conversation's agents changed, with a diff for each. From here you can restore a single file, or all the files of a turn, to how they were before (see [Rewind](/docs/desktop/rewind/)). Agents that worked in an isolated copy of the project show their work under **Branches** until it is merged (see [Limits and isolation](/docs/desktop/limits/)).

<!-- shot: desktop/agents-changes.png | the Changes view with two changed files and one diff expanded -->

## Pause, continue, stop, resume

Each run's card has the controls that fit its state:

| Button | When | What it does |
|---|---|---|
| **Pause** | running | holds every agent before its next step; nothing is killed |
| **Continue** | paused | lets the held agents take their next step |
| **Stop** | running or paused | stops the run and every agent in it |
| **Resume** | stopped, failed or interrupted | starts a new run that continues from where the old one ended |

A resumed swarm tells its new lead what the old workers finished, and a resumed consensus run carries on with its rounds. `/stop` stops everything in the conversation; `/resume` resumes its last stopped run.

## Commands left running

A command an agent starts may keep running after the step ends: a dev server, a file watcher, a long build. Such commands appear in a **Still running** strip at the top of the agents pane, with their process id. Click **Stop** to end one together with everything it started.

## Talking to a running run

Use **↠ Steer** on a running run's card to add a message to it: its top agent reads it before its next step. Use **↩ Reply** to send a follow-up about a run that has finished.

<!-- source: D:lib/swarm_code_web/components/swarm_pane.ex:1-30,117,212-295,520-575,3482, D:lib/swarm_code_web/components/chat.ex:3318-3385,2930-2945,3185-3200, D:lib/swarm_code/engine.ex:1145-1180,666-678, D:lib/swarm_code_web/live/workspace_live/workspace.html.heex:582-590, D:lib/swarm_code/tools/background_procs.ex:1-30, D:lib/swarm_code/checkpoints.ex:500-600 -->
