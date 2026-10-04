---
title: Consensus
description: Run a turn as a judged plan, where a planner and a second model take turns until the judge approves, with checks you choose.
---

Consensus gives a plan a second opinion before any code changes. A **planner** writes a plan, a **judge** (ideally a different model) reviews it against the checks you pick, and they take turns until the judge approves. Then the plan is implemented, or waits for you.

## Starting a judged turn

- Pick **⚖ Consensus** in the mode pill and send your request, or
- type `/consensus <task>`.

## The consensus settings

In Consensus mode the composer shows a settings popover for the conversation:

| Setting | Meaning |
|---|---|
| Planner model | the model that writes the plan |
| Judge model | the model that reviews it; if unset, the sub-agent model |
| Implementer model | the model that carries out the approved plan; by default the planner implements |
| Rounds | 1, 2 or 3 review rounds (2 by default) |
| Judge for | the checks below |

## The checks

Seven checks are on in a new conversation; five more are available:

| Check | On by default |
|---|---|
| Avoid over-engineering | yes |
| Judge the plan before any change | yes |
| Keep changes minimal | yes |
| Compare against the codebase | yes |
| Scope guard | yes |
| Missing requirements & edge cases | yes |
| Ask me before implementing | yes |
| Judge the changes after implementing | no |
| Risk & safety review | no |
| Require verification | no |
| Propose a simpler alternative | no |
| No open questions left | no |

With **Ask me before implementing** on, the run pauses after the judge approves and asks you: **Implement**, **Plan only** or **Revise**. With it off, the approved plan is implemented right away.

The planner model is the conversation's chat model.

## How a round ends

Each round, the judge either approves the plan or sends findings back, and the planner revises. If the rounds run out, the planner goes on with its best plan and the card says so. The agents pane shows the rounds, the verdicts and each finding.

![The finished Consensus Scales card: R1 plan and R2 revised plan sent back with REVISE, R3 changes REVISE, and R4 changes APPROVED with all five checks passed; four rounds in 26m 48s.](/assets/shots/desktop/consensus-scales.webp)

## Card layouts

The judged turn's card in the agents pane has four layouts: **Scales** (the default), **Rail** (the checks on a rail), **Spine** and **Scorecard**. Set the default under **Settings → Appearance**; a conversation can switch its own from the pane.

![One consensus turn in the Rail, Spine and Scorecard layouts side by side: planner claude-sonnet-5, judge gpt-6-luna, two rounds each judged REVISE with a mark per check, waiting for your go.](/assets/shots/desktop/consensus-layouts.webp)

<!-- source: D:lib/swarm_code/engine/consensus.ex:23-200,260-265,325-329, D:lib/swarm_code_web/components/chat.ex:84-89,5860-5970, D:lib/swarm_code/providers.ex:198-212, D:lib/swarm_code_web/components/consensus_components.ex:1186-1192, D:lib/swarm_code/settings/setting.ex:90-92,201-202, D:lib/swarm_code_web/live/settings_live.html.heex:680-700 -->
