---
title: Ultra missions
description: How Ultra mode plans big work as a mission with a validation contract, approval card, parallel workers, validators and fix rounds, and how to follow it.
---

**Ultra** mode turns big requests into **missions**. The assistant becomes the **orchestrator**: it answers small requests itself and runs work that needs several parts as a mission that workers build and validators check. Pick Ultra in the mode pill or type `/ultra` ([Composer, modes and goals](/docs/desktop/composer/)).

## When the orchestrator plans a mission

- **Answered directly.** Questions, explanations and small changes, such as one file or one clear fix, are handled inline in the chat, as in Build mode.
- **Run as a mission.** Several features, a change across many files, a refactor across modules, anything that needs more than one worker.

Before it plans, the orchestrator reads the code, the tests and your project instructions, and learns how the project builds and tests. If something cannot be found out from the code, such as scope, behaviour you care about or constraints, it asks you up to four multiple-choice questions first ([Approvals and trust](/docs/desktop/approvals/#questions-from-agents)). It skips the questions when the request is clear.

## The plan

The orchestrator writes the plan in this order:

1. A **validation contract**: behavioural assertions with ids such as `VAL-AUTH-001`. Each one is something observable, with a method (a test, a command, or reading the code) and the evidence a validator has to capture. The contract is written before the features and describes what you want, not how it is built.
2. **Features**: each one is self-contained for a worker that has never seen the conversation (what to build, which files, which tests to write first, how to run them), and each claims the assertions it satisfies. Every assertion is claimed by a feature.
3. **Milestones**: features grouped in dependency order, at most six. Features inside one milestone run at the same time, so they must not edit the same files; dependent work goes into a later milestone.
4. **Guidelines and knowledge**: the conventions, the exact test and build commands, files never to touch, and what the orchestrator learned about the project.

It then starts the mission and stops. It does not ask for approval itself; the approval card does.

## The approval card

The plan waits for you before any worker starts. A card directly above the composer shows its size, for example `3 milestones · 7 features · 14 assertions`, and two model pickers:

- **Worker model** builds each feature.
- **Validator model** checks every milestone; **Same as main model** means the orchestrator's model.

If the conversation has no worker model yet, the card is marked **Choose before approving** and the pickers are shown first. Your picks are saved for the conversation, so later missions do not ask again. If a worker model is already set, both appear as small chips (`Worker · …`, `Validator · …`) that open into the pickers.

| Button | What it does |
|---|---|
| **Approve and start** | saves the model picks and starts the build |
| **Cancel mission** | ends the mission; nothing was changed |

To change the plan, choose **Cancel mission** and tell the orchestrator what should change; it plans again and shows a new card.

> **Note** Approving lets this mission's workers and validators run commands without asking. Dangerous commands still ask, Read-only mode still blocks writes and commands, and the permission applies to this mission only. Tools from MCP servers that can write still ask ([Approvals and trust](/docs/desktop/approvals/)).

The card is the only place to approve. The workflow cockpit lists a waiting plan under **needs you** with a **Review plan** link that takes you to the card.

## How it runs

The mission goes through the phases Contract, Build, Validate, Fix and Report, one milestone at a time.

- **Workers.** The features of a milestone run as parallel workers, at most four at once. Each works in its own isolated copy of the project when worktrees are on (**Settings → Limits → Isolate sub-agents in git worktrees**) and the project is a git repository with at least one commit. Otherwise the features run one at a time in the project folder. Finished workers are merged back one by one ([Limits and isolation](/docs/desktop/limits/)).
- **Merge conflicts.** A conflict never leaves conflict markers in your files. The feature is redone once on the updated project; if it conflicts again, a card asks you to **Retry merge**, **Skip it** or **Stop**. If a merge cannot happen because of your own uncommitted changes, commit or stash them first and retry.
- **Validators.** Two validators check each milestone: a **scrutiny** validator that reviews the code the workers wrote, and a **user-testing** validator that checks every assertion the way a user would, running tests and commands and quoting the evidence. Validators can read files and run commands, but they never write or fix anything.
- **Fix rounds.** Failed assertions and high-severity findings become fix features, up to four per round, and the milestone is validated again. There are two fix rounds by default. After that a card asks you to choose **Fix again**, **Next milestone** or **Stop**.
- **Questions.** When a fix needs your decision, the mission halts and asks you instead of guessing.
- **Report.** At the end the orchestrator tells you what passed, what failed and why, and what it suggests next.

You can keep talking to the orchestrator while the mission runs. It does not write the features itself while a mission is going.

## Mission Control

While a mission runs, the agents pane shows **Mission Control** in place of the generic workflow view:

- one star per milestone in a rail, with its feature lanes and their progress, role and model chips;
- the **Contract** grid of `VAL-` ids, each pass, fail or pending;
- the validators' verdicts per milestone, the fix rounds and the agent budget;
- **Waiting for your approval** with a **Review the plan** button while the plan waits.

A mission that did not finish reads as what it was, not as done: **Cancelled**, **Stopped**, **Revision requested** or **Partial**. Stop the mission with the Stop button or `/stop`; see [Watching agents work](/docs/desktop/agents/) and [Workflows](/docs/desktop/workflows/#ultra-mode).

## The models

Ultra uses three model slots, each with its own effort:

| Slot | Where it is set | Default |
|---|---|---|
| Orchestrator | the composer's model row, labelled **Orchestrator model** while Ultra is on | the conversation's main model |
| Worker | **Worker model** in the composer, Settings or the approval card | none: the card asks before the first mission |
| Validator | **Validator model** in the composer (Ultra only), Settings or the approval card | **Same as main model** |

See [Providers, models and web search](/docs/desktop/providers/#default-models). The sidebar's [speed monitor](/docs/desktop/tour/#speed-monitor) shows a row for each of the three while Ultra is on.

> **Tip** Use your strongest model as the orchestrator, a fast, cheaper one for the workers and a careful one as the validator.

## Good to know

- The built-in mission is not in the workflow Library or the `/` palette, and a mission run has no **Run again**: start a new mission from an Ultra conversation.
- A mission is limited by an agent budget worked out from the plan's size, with room for extra fix rounds. Workers and validators follow the same limits as other agents ([Limits and isolation](/docs/desktop/limits/)).
- To write your own workflows instead, use `/create-workflow` ([Workflows](/docs/desktop/workflows/)).

<!-- source: D:CHANGELOG.md (pass 71 entry, 9ef3dca4), D:lib/swarm_code/engine/prompts.ex:75-90, D:lib/swarm_code/tools/mission_start.ex:75-120, D:lib/swarm_code/missions.ex:15-45, D:priv/workflows/mission.exs:138-230,255-270,422-450,585-625, D:lib/swarm_code_web/components/mission_components.ex:13-125, D:lib/swarm_code_web/components/mission_control.ex:60-215, D:lib/swarm_code_web/mission_view.ex:54-72, D:lib/swarm_code_web/components/chat.ex:6085-6140 -->
