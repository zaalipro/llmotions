---
title: Scheduled tasks
description: Create, edit, switch on or off and run scheduled tasks from the terminal - and why they fire only while the desktop app is running.
---

A scheduled task runs a prompt by itself at the times you choose: a morning summary of new issues, a nightly `review-changes`, a weekly dependency check.

> **Warning** Scheduled tasks fire only while the {{product}} desktop app is running. `{{cmd}}` can create, edit, switch on or off and "run now" a task, but it never fires a schedule itself. If you use only the terminal, a task runs only when you run it by hand.

{{> shared/scheduled}}

## Managing tasks from the terminal

Open **Scheduled Tasks** from the [[Ctrl]]+[[P]] palette. The library lists your tasks; from it you can:

- create a task or edit one, in a form: arrow keys cycle the choices and switches, [[Enter]] saves, [[Esc]] cancels, and a value the form does not accept stays with the error next to it;
- switch a task on or off;
- run a task now, once, whatever its schedule;
- delete a task.

A task's runs are ordinary runs in their own conversation, so you can open them like any other conversation.

The model and effort that new tasks use by default are **Scheduled task model** and **Scheduled effort** in Settings → Models & effort.

<!-- source: C:apps/swarm_code_daemon/lib/swarm_code/daemon/boot.ex:14, C:apps/swarm_code_daemon/lib/swarm_code/domain/runtime.ex:4, C:apps/swarm_code_daemon/lib/swarm_code/domain/feature_catalog.ex:212-250, C:README.md:223-224, C:README.md:300-303, C:docs/settings.md:17,22, D:lib/swarm_code/scheduler.ex:1-19 -->
