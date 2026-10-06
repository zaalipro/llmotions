---
title: Workflows
description: Run built-in and saved workflows, launch them with arguments, pause, resume and stop them, write new ones with the assistant, and let Ultra mode use them.
---

A workflow runs agents in a fixed, repeatable order: review from four angles, then verify each finding, then write a report. Unlike a swarm, where a lead decides the plan as it goes, a workflow's steps are written down in advance, so the same workflow runs the same way every time and a stopped run can resume exactly where it stopped.

## Where to find them

Click **Workflows** in the rail. The sidebar becomes the workflow cockpit:

- four counters at the top: **Live** (runs going now), **Need you** (runs waiting at a question or paused), **Week** (runs started since Monday) and **Spend** (what this month's workflow runs cost);
- the runs, newest first, each with its phase and progress;
- the library of workflows you can run, grouped by where they come from, for the project you pick at the top;
- a **+** button to create a new one.

The main area shows the selected run as a board of phases and agents, or the selected workflow's details: its description, arguments, the shape the smoke check found, and its source.

![The Workflows panel: the counters LIVE 1, NEED YOU 0, WEEK 3 and SPEND $1.69, the phase board and the library, three runs (review-changes-3 live in Review, review-changes-2 done, an earlier one stopped), and review-changes-3's phase board with a Review panel of three agents and Verify and Report pending.](/assets/shots/desktop/workflows-cockpit.webp)

## Built-in workflows

| Workflow | What it does |
|---|---|
| `review-changes` | reviews the uncommitted changes from several angles (correctness, security, performance, maintainability, one agent each), keeps only findings that survive a second agent's attempt to refute them, and writes `review.md` |
| `research` | a one-pass research inside the conversation: sweeps a few angles, reads the best pages and writes `research.md` into the project |

## Running a workflow

From the library: select a workflow and click **Run ▸**. A form asks for its arguments, with their defaults filled in; click **Run ▸** again.

From a conversation: type `/workflow <name>`, with arguments as `key=value`:

```text
/workflow review-changes base=main
```

Saved workflows also appear in the `/` list under their own name.

A workflow run shows as a card in the conversation and in the cockpit. Its agents appear in the agents pane like any others.

## Pause, resume, stop

A running workflow's card has **Pause** and **Stop**; a paused one has **Resume**. From the composer, `/workflow pause <run>`, `/workflow resume <run>` and `/workflow stop <run>` do the same.

Every read a workflow makes is recorded, so resuming replays the finished part instantly and continues with the next step. A workflow can also stop on purpose to ask you something; it waits under **Need you** until you answer.

Quitting {{product}} pauses running workflows; they resume where they stopped.

## Writing a new workflow

You do not need to write code yourself:

- Type `/create-workflow` followed by what it should do, pick **Workflow** in the mode pill, or click **+** (New workflow) in the cockpit. The assistant writes the workflow, checks it and launches it.
- To start from a skeleton instead, use the new-workflow menu on the Workflows page and choose **Blank template** (its other choice, **Describe it to the assistant**, is the same as above).
- `/workflow save <run> as <new-name>` saves the workflow of a run you liked under a new name, in this project; add `scope=user` to save it for every project instead.

Before any workflow is saved or run, a smoke check parses it and runs it once with stand-in agents, so mistakes show up before they cost anything. See [Workflow language](/docs/desktop/workflow-language/).

## Ultra mode

In **Ultra** mode (pick it in the mode pill or type `/ultra`), the assistant handles big requests as **missions**: it plans them, you approve the plan, and workers and validators carry it out. It no longer writes workflows on its own in this mode; use `/create-workflow` or `/workflow` for that. See [Ultra missions](/docs/desktop/missions/). The built-in mission is not in the Library.

## Where workflows live

| Scope | Folder | Seen in |
|---|---|---|
| Built-in | inside the app | every project; cannot be edited, but **Duplicate to project** makes an editable copy |
| Yours | `workflows` inside `{{data_dir}}` | every project |
| Project | `{{project_dir}}/workflows/` in the project | that project; commit it to share with your team |

If two workflows share a name, the built-in one wins, then the project's, then yours: pick a new name for your own. Reports a run writes go to `{{project_dir}}/workflows/runs/<run>/` in the project.

## Budgets

A workflow's `budget` sets how many agents one run may start in total (the built-in `review-changes` allows 48), and its `max_live` how many work at the same time. A workflow that sets neither uses **Workflow agent budget** (128) and **Max live workflow agents** (16) from **Settings → Limits**.

<!-- source: D:lib/swarm_code_web/components/frame.ex:1625-1740,1951-1993, D:lib/swarm_code_web/live/workflows_live.html.heex:50-100,320-436, D:priv/workflows/review-changes.exs:1-10, D:priv/workflows/research.exs:1-3, D:lib/swarm_code_web/components/chat.ex:65-81,130-142,3318-3340, D:lib/swarm_code/workflows.ex:24-37,86-96, D:lib/swarm_code/workflows/api.ex:337-353,434-452, D:lib/swarm_code/workflows/smoke.ex:1-12, D:lib/swarm_code_web/components/quit_modal.ex:84-88,118-120, D:lib/swarm_code/settings/setting.ex:51-52, D:lib/swarm_code/workflows.ex:639-642, D:priv/workflows/review-changes.exs:5, D:lib/swarm_code_web/live/workspace_live/workflows_panel.ex:383-418 -->
