---
title: Approvals and trust
description: How ncode decides what agents may do on their own, how to trust a project, answer approval cards and questions, and remember or forget commands.
---

Agents in {{product}} can write files and run commands on your Mac. Two things keep you in control: the project's **approval mode**, and **approval cards** that ask you before a step the mode does not allow on its own.

## Choosing the mode

The approval control in the composer shows the current project's mode. Click it to switch:

| Mode | In the menu |
|---|---|
| Read-only | agents can only read and search |
| Auto | write & run safe commands |
| Full access | everything, no prompts |

Even in Full access, a command {{product}} classifies as dangerous still asks. The mode belongs to the project, so every conversation in it follows the same mode.

{{> shared/approvals}}

## Trusting a new project

When you add a folder, a banner above the composer says the project is read-only until you trust it. Click **Trust and allow edits** to trust it and switch it to Auto. Until then, agents can read and search but not write or run anything, and the project's `AGENTS.md` and hooks are ignored.

Only trust folders you know: a repository you just downloaded can contain instructions and hooks written by someone else.

## Answering an approval card

When a step needs your approval, a card appears in the transcript and on the agent in the agents pane, with the exact command or change:

| Button | What it does |
|---|---|
| **Approve** | allows this one step |
| **Deny** | refuses it; the agent is told and carries on |
| **Deny & stop** | refuses it and stops the run |
| **Always allow "…"** | allows it and remembers the command family (for example `mix test`) for this project |
| **Allow all … this run** | shown instead when there is no command family: allows every call of that tool until the run ends |

![A run card waiting on an approval for the command mix test test/ailogic/rate_limiter_test.exs, with Approve, Deny, Deny & stop and Always allow “mix test”.](/assets/shots/desktop/quickstart-approval.webp)

An approval nobody answers expires after 10 minutes, and the agent is told it timed out. A conversation with an open approval shows a waiting dot in the sidebar, and the menu bar icon lists it under **Waiting for you**.

## Missions

When you approve an Ultra mission's plan, its workers and validators may run commands without asking for that mission only. Dangerous commands still ask, and Read-only mode still blocks them. See [Ultra missions](/docs/desktop/missions/#the-approval-card).

## Forgetting remembered commands

Open **Settings → Limits** and scroll to **Approved commands**. It lists, per project, every command family you allowed with **Always allow**. Click the **×** on one to forget it, or **Clear all** to forget every one of a project.

## Questions from agents

Sometimes the assistant or a lead agent asks you instead of guessing: an unclear request, two valid approaches, a destructive choice. A question card shows one to four questions, each with a few options; pick one or type your own answer. A question waits up to 30 minutes for an answer.

<!-- source: D:lib/swarm_code_web/components/chat.ex:746-830,5632-5644,5690, D:lib/swarm_code_web/live/workspace_live/workspace.html.heex:118-130, D:lib/swarm_code/projects.ex:175-189, D:lib/swarm_code/engine/questions.ex:10-14, D:lib/swarm_code/engine/operation.ex:310-311, D:lib/swarm_code/engine/run_server.ex:976,1985-2008, D:lib/swarm_code/tools/ask_user.ex:15-20, D:lib/swarm_code/tools.ex:38, D:lib/swarm_code_web/live/settings_live.html.heex:1622-1655, D:lib/swarm_code/tray_menu.ex:52-57 -->
