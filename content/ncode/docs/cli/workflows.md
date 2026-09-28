---
title: Workflows
description: Run, control and write workflows - small programs that run agents in fixed phases - from the terminal session.
---

A workflow turns a job you do again and again into a program: review the changes from four angles, verify each finding, write a report. It runs agents in fixed phases, records every step so a stopped run can resume exactly where it was, and shows its phases in the side panel while it works.

## Built-in workflows

| Name | What it does |
|---|---|
| `review-changes` | reviews the uncommitted changes from several angles (Review → Verify → Report) and keeps only the findings that survive an adversarial check |
| `research` | one-pass research inside the conversation: sweeps a few angles, reads the best pages and writes `research.md` into the project |

For a multi-round research with an HTML report, use [Deep research](/docs/cli/research/) instead.

## Running a workflow

```text
/workflow review-changes
/workflow summarize-changes base=main
```

`/workflow <name>` starts a workflow (the second line runs one of your own); arguments follow as `key=value`. A workflow run starts at once, beside any turn that is running. Saved workflows also appear in the `/` list as commands of their own.

You can also start one from the library: `/workflows`, or **Workflows** in the [[Ctrl]]+[[P]] palette, lists every workflow and its runs. A row opens a form for the workflow's arguments: arrow keys cycle choices and switches, [[Enter]] starts it, [[Esc]] cancels. A value the workflow does not accept stays in the form with the error next to it.

<!-- capture: cli/workflow-run | a review-changes run: the transcript with the phase headings and the side panel showing the Review phase with four agents and the Verify phase waiting | 120x40 -->

## Controlling a run

```text
/workflow pause <run>
/workflow resume <run>
/workflow stop <run>
/workflow save <run>
```

`pause` and `resume` hold and continue a run, and `stop` ends it. Because every step is recorded, a run that resumes picks up where it was instead of starting over.

## Letting the assistant write one

- `/create-workflow <what it should do>` writes a new workflow with the assistant.
- A message that talks about a *workflow* is sent as `/create-workflow` by itself; [[Ctrl]]+[[S]] sends it as a plain message instead (see [Composer](/docs/cli/composer/#messages-that-name-a-workflow)).
- In **Workflow** mode, your next message authors and launches a workflow.
- In **Ultra** mode (`/ultra`), the assistant turns big tasks into workflows on its own.

## Where workflows live

| Scope | Folder |
|---|---|
| This project | `{{project_dir}}/workflows/` in the project (commit it to share with your team) |
| You, in every project | `workflows/` inside `{{data_dir}}` |
| Built in | shipped with {{product}} |

Reports a workflow writes go under `{{project_dir}}/workflows/runs/<run>/` in the project.

## The workflow language

{{> shared/workflows}}

<!-- source: C:apps/swarm_code_core/lib/swarm_code/commands.ex:26-31,140, C:README.md:223-227, C:README.md:300-303, C:AGENTS.md:227, C:AGENTS.md:241-243, C:AGENTS.md:188-190, C:apps/swarm_code_daemon/lib/swarm_code/domain/workflows.ex:24-49,90-97, C:apps/swarm_code_daemon/priv/workflows/research.exs:1-4, C:apps/swarm_code_daemon/priv/workflows/review-changes.exs:1-4, D:lib/swarm_code/workflows/api.ex:353, D:lib/swarm_code_web/components/chat.ex:128-142 -->
