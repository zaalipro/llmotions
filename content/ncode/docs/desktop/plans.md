---
title: Plans you approve
description: Use Plan mode to get a read-only, step-by-step plan, then approve it for one agent or a swarm, revise it, or decline it.
---

When a change is big or risky, ask for a plan first. In Plan mode the agent can only read and search; it answers with a step-by-step plan and changes nothing until you approve it.

## Asking for a plan

1. Switch the composer to **Plan**: pick it in the mode pill, press [[Shift]]+[[Tab]], or type `/plan`.
2. Describe what you want, as you would in Build mode.

The run's top agent is called the **Planner**. It reads the code it needs and writes the plan into its card.

## Approve, revise or decline

A finished plan carries three buttons at the foot of its card (also in the side chat and on its row in the agents pane):

- **✓ Approve** asks one question: who implements it?
  - **Assistant**: one agent, full access, in this chat.
  - **Swarm**: a lead that fans the work out to workers.
- **✎ Revise** lets you write what to change; the Planner produces a new plan as a follow-up.
- **✕ Decline** keeps the plan on the record and runs nothing.

After **Approve**, the implementation starts at once with the plan as its instructions: follow the steps in order, do not re-plan, verify the work the way the plan says, and finish with what changed, file by file. The composer switches back to Build.

<!-- shot: desktop/plans-gate.png | a finished Planner card with ✓ Approve, ✎ Revise and ✕ Decline at its foot, and the Assistant / Swarm chooser open above Approve -->

Each plan can be decided once. Clicking a button on a plan that was already approved, revised or declined says the plan is no longer open.

## Following the implementation

The implementation hangs under its plan: in the transcript its card sits inside the plan's card, and in the agents pane it appears directly under the Planner with a **↳ implements plan** mark. The plan's card shows **↳ implemented by …** with the implementation's state.

## A plan with a second opinion

To have another model check the plan before anything is implemented, use [Consensus](/docs/desktop/consensus/): a judge reviews the planner's plan, round by round, until it approves.

<!-- source: D:lib/swarm_code_web/components/chat.ex:3229,3416-3510,5705-5718,5783, D:lib/swarm_code/engine.ex:19-31, D:CHANGELOG.md:2112-2160 -->
